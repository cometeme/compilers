import json
from typing import Dict, List

from rich.console import Console
from rich.table import Table

from Grammar import Grammar, Grammar_Production
from Scanner import Scanner
from Symbol_Table import Symbol_Table

console = Console()


class SLR_Automata:
    scanner: Scanner
    symbol_table: Symbol_Table
    grammar: Grammar
    action_table: List[Dict[str, str]] = list()
    goto_table: List[Dict[str, int]] = list()

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

    def run(self) -> None:
        stack: List[int] = [0]
        token: str = self.scanner.get_next().name() if self.scanner.has_next() else "$"
        current_line: int = 0

        # run automata
        while True:
            if token not in self.action_table[stack[-1]]:
                self.print_state()
                console.print(f"Current token: {token}")
                console.print(f"Current stack: {stack}")
                console.print(f"Action Table [{stack[-1]}]: {self.action_table[stack[-1]]}")
                print("SLR ERROR")
                exit(-1)

            action: str = self.action_table[stack[-1]][token]

            if action == "acc":
                self.state_output.add_row(token, str(stack), action, "")
                break

            action_type: str = action[0]
            action_value: int = int(action[1:])

            if action_type == "s":
                # shift in next state
                self.state_output.add_row(token, str(stack), action, "")

                stack.append(action_value)
                token = self.scanner.get_next().name() if self.scanner.has_next() else "$"
            elif action_type == "r":
                # reduced by production
                current_production: Grammar_Production = self.grammar.production_list[action_value]
                self.state_output.add_row(token, str(stack), action, str(current_production))

                length: int = len(current_production.items)

                # solve for not A → ε
                if not (current_production.items[0].is_symbol and current_production.items[0].value == "ε"):
                    stack = stack[:-length]

                reduce_state: str = current_production.from_state
                stack.append(self.goto_table[stack[-1]][reduce_state])

                # run generation code
                exec(current_production.code)
            else:
                self.print_state()
                print(f"Unknown action type {action_type}!")
                exit(-1)
