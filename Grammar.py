from typing import List

from rich.console import Console

console = Console()


class Grammar_Item:
    is_symbol: bool  # True for terminal symbol, False for Variable
    value: str

    def __init__(self, is_symbol: bool, value: str) -> None:
        self.is_symbol = is_symbol
        self.value = value


class Grammar_Production:
    from_state: str
    items: List[Grammar_Item]

    def __init__(self, from_state: str) -> None:
        self.from_state = from_state
        self.items = list()

    def add(self, is_symbol: bool, value: str) -> None:
        self.items.append(Grammar_Item(is_symbol, value))

    def __str__(self) -> str:
        return f"{self.from_state} → " + " ".join([item.value for item in self.items])


class Grammar:
    start_symbol: str
    terminal_symbols: List[str]
    variable_symbols: List[str]
    production_list: List[Grammar_Production]

    def __init__(self) -> None:
        self.production_list = list()

    def read(self, path: str) -> None:
        with open(path, "r") as f:
            lines = f.read().split("\n")

        self.terminal_symbols = lines[0].split(" ")
        self.variable_symbols = lines[1].split(" ")
        self.start_symbol = self.variable_symbols[0]

        lines = lines[3:]

        for line in lines:
            from_state, production = line.split(" → ")

            current_grammar_production = Grammar_Production(from_state)
            items = production.split(" ")

            for item in items:
                if item in self.terminal_symbols:
                    current_grammar_production.add(True, item)
                elif item in self.variable_symbols:
                    current_grammar_production.add(False, item)
                else:
                    console.print(f"Unknown symbol '{item}' in grammar file", style="bold red")
                    exit(-1)

            self.production_list.append(current_grammar_production)
