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

        # init output table
        self.output_table = Table(
            show_header=True,
            header_style="bold",
        )

        self.output_table.add_column("Token", justify="center")
        self.output_table.add_column("Stack", justify="left")
        self.output_table.add_column("Action", justify="center")
        self.output_table.add_column("Production", justify="left")

    def output(self) -> None:
        self.scanner.output()
        console.print("SLR State:", style="bold")
        console.print(self.output_table)

    def run(self) -> None:
        stack = [0]
        token = self.scanner.get_next().name() if self.scanner.has_next() else "$"

        # run automata
        while True:
            if token not in self.action_table[stack[-1]]:
                self.output()
                print("SLR ERROR")
                exit(-1)

            action: str = self.action_table[stack[-1]][token]

            if action == "acc":
                self.output_table.add_row(token, str(stack), action, "")
                break

            action_type: str = action[0]
            action_value: int = int(action[1:])

            if action_type == "s":
                # shift in next state
                self.output_table.add_row(token, str(stack), action, "")

                stack.append(action_value)
                token = self.scanner.get_next().name() if self.scanner.has_next() else "$"
            elif action_type == "r":
                # reduced by production
                current_production: Grammar_Production = self.grammar.production_list[action_value]
                self.output_table.add_row(token, str(stack), action, str(current_production))

                length: int = len(current_production.items)
                reduce_state: str = current_production.from_state
                stack = stack[:-length]
                stack.append(self.goto_table[stack[-1]][reduce_state])
                # TODO, run generation code
            else:
                self.output()
                print(f"Unknown action type {action_type}!")
                exit(-1)
