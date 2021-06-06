import csv
import json
from typing import Dict, List, Union

from rich.console import Console
from rich.table import Table

from Grammar import Grammar, Grammar_Production
from Scanner import Scanner
from Symbol_Table import Symbol_Table, Table_Item, item_type_translate
from Token import Token, Token_Type

console = Console()


class SLR_Automata:
    scanner: Scanner
    symbol_table: Symbol_Table
    grammar: Grammar
    action_table: List[Dict[str, str]] = list()
    goto_table: List[Dict[str, int]] = list()
    state_output: List[List[str]]
    code_output: List[List[str]]
    current_line: int

    def __init__(self, scanner: Scanner, grammar: Grammar) -> None:
        self.scanner = scanner
        self.symbol_table = scanner.symbol_table
        self.grammar = grammar

        with open("action_table.json", "r") as f:
            self.action_table = json.loads(f.read())
        with open("goto_table.json", "r") as f:
            self.goto_table = json.loads(f.read())

        # init state output
        self.state_output = []
        self.code_output = []

    def print_state(self) -> None:
        output_table = Table(
            show_header=True,
            header_style="bold",
        )

        output_table.add_column("Token", justify="center")
        output_table.add_column("Stack", justify="left")
        output_table.add_column("Action", justify="center")
        output_table.add_column("Production", justify="left")

        for row in self.state_output:
            output_table.add_row(*row)

        console.print("SLR State:", style="bold")
        console.print(output_table)

    def print_code(self) -> None:
        output_table = Table(
            show_header=True,
            header_style="bold",
        )

        output_table.add_column("Line", justify="center")
        output_table.add_column("Code", justify="left")

        for row in self.code_output:
            output_table.add_row(*row)

        console.print("Code:", style="bold")
        console.print(output_table)

    def save(self) -> None:
        with open("output/slr_states.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Token", "Stack", "Action", "Production"])
            for row in self.state_output:
                writer.writerow(row)
        with open("output/code.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Line", "Code"])
            for row in self.code_output:
                writer.writerow(row)

    def gen_code(self, code: str) -> None:
        self.code_output.append([str(self.current_line), code])
        self.current_line += 1

    def gen_variable(self, name: str) -> int:
        item = Table_Item()
        item.name = name
        item.variable = True
        entry = self.symbol_table.add_item(item)
        return entry

    def make_list(self, inst: int) -> List:
        return [inst]

    def merge(self, l1: List, l2: List) -> List:

        l = list()
        l.extend(l1)

        for inst in l2:
            if inst not in l:
                l.append(inst)

        return l

    def back_patch(self, l: List, target: int) -> None:
        for inst in l:
            # back patch all blank field
            if inst < len(self.code_output) - 1 and not self.code_output[inst][1][-1].isdigit():
                if len(self.code_output[inst][1]) >= 5 and self.code_output[inst][1][-5:-1] == "goto":
                    self.code_output[inst][1] += str(target)

    def run(self, debug: bool = True) -> None:
        stack: List[int] = [0]
        attributes: List[Dict[str, Union[str, int]]] = [dict()]
        token: Union[Token, None] = self.scanner.get_next() if self.scanner.has_next() else None
        token_string: str = "$" if token is None else token.to_string()
        self.current_line = 0

        # run automata
        while True:
            assert len(stack) == len(attributes)

            if token_string not in self.action_table[stack[-1]]:
                self.print_state()
                console.print(f"Current token_string: {token_string}")
                console.print(f"Current stack: {stack}")
                console.print(f"Action Table [{stack[-1]}]: {self.action_table[stack[-1]]}")
                console.print("SLR ERROR", style="bold red")
                exit(-1)

            action: str = self.action_table[stack[-1]][token_string]

            if debug:
                console.print(f"\ntoken: {token_string}")
                console.print(f"stack: {stack}")
                console.print(f"attributes: {attributes}")
                console.print(f"action: {action}")

            if action == "acc":
                self.state_output.append([token_string, str(stack), action, ""])
                break

            action_type: str = action[0]
            action_value: int = int(action[1:])

            if action_type == "s":
                # shift in next state
                self.state_output.append([token_string, str(stack), action, ""])

                stack.append(action_value)

                if token.token_type in [Token_Type.ID, Token_Type.CONST]:
                    attributes.append({"entry": -1 if token.content is None else token.content})
                else:
                    attributes.append(dict())

                token: Union[Token, None] = self.scanner.get_next() if self.scanner.has_next() else None
                token_string: str = "$" if token is None else token.to_string()
            elif action_type == "r":
                # reduced by production
                current_production: Grammar_Production = self.grammar.production_list[action_value]
                self.state_output.append([token_string, str(stack), action, str(current_production)])

                if debug:
                    console.print(f"production: {current_production}")
                    print(f"code:\n{current_production.code}\n")

                length: int = len(current_production.items)
                current_attribute = dict()

                # run generation code
                try:
                    exec(current_production.code)
                except Exception as e:
                    console.print("Execute Generation Faild!", style="bold red")
                    self.print_state()
                    print(f"Production: {current_production}\n\n")
                    print(f"code:\n\n{current_production.code}\n")
                    exec(current_production.code)

                # solve for not A → ε
                if not (current_production.items[0].is_symbol and current_production.items[0].value == "ε"):
                    stack = stack[:-length]
                    attributes = attributes[:-length]

                reduce_state: str = current_production.from_state
                stack.append(self.goto_table[stack[-1]][reduce_state])
                attributes.append(current_attribute)

            else:
                self.print_state()
                console.print(f"Unknown action type {action_type}!", style="bold red")
                exit(-1)
