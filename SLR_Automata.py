import json
from typing import Dict, List, Union

from rich.console import Console
from rich.table import Table

from Grammar import Grammar, Grammar_Production
from Scanner import Scanner
from Symbol_Table import Symbol_Table, item_type_translate
from Token import Token, Token_Type

console = Console()


class SLR_Automata:
    scanner: Scanner
    symbol_table: Symbol_Table
    grammar: Grammar
    action_table: List[Dict[str, str]] = list()
    goto_table: List[Dict[str, int]] = list()
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
        self.state_output = Table(
            show_header=True,
            header_style="bold",
        )

        self.state_output.add_column("Token", justify="center")
        self.state_output.add_column("Stack", justify="left")
        self.state_output.add_column("Action", justify="center")
        self.state_output.add_column("Production", justify="left")

        # init code output
        self.code_output = Table(
            show_header=True,
            header_style="bold",
        )

        self.code_output.add_column("Line", justify="center")
        self.code_output.add_column("Code", justify="left")

    def print_state(self) -> None:
        console.print("SLR State:", style="bold")
        console.print(self.state_output)

    def print_code(self) -> None:
        console.print("Code:", style="bold")
        console.print(self.code_output)

    def gen_code(self, code: str) -> None:
        self.code_output.add_row(str(self.current_line), code)
        self.current_line += 1

    def run(self) -> None:
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

            if action == "acc":
                self.state_output.add_row(token_string, str(stack), action, "")
                break

            action_type: str = action[0]
            action_value: int = int(action[1:])

            if action_type == "s":
                # shift in next state
                self.state_output.add_row(token_string, str(stack), action, "")

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
                self.state_output.add_row(token_string, str(stack), action, str(current_production))

                length: int = len(current_production.items)
                current_attribute = dict()

                # run generation code
                try:
                    exec(current_production.code)
                except Exception as e:
                    console.print("Execute Generation Faild!", style="bold red")
                    self.print_state()
                    console.print(f"stack:\n{stack}\n\n")
                    console.print(f"attributes:\n{attributes}\n\n")
                    print(f"code:\n\n{current_production.code}\n")
                    print(e)
                    exit(-1)

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
