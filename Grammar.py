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
    code: str

    def __init__(self, from_state: str) -> None:
        self.from_state = from_state
        self.items = list()
        self.code = ""

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

    def save(self) -> None:
        with open("output/grammar.txt", "w") as f:
            f.write(f"Start Symbol: {self.start_symbol}\n")
            f.write(f"Terminal Symbols: {' '.join(self.terminal_symbols)}\n")
            f.write(f"Variable Symbols: {' '.join(self.variable_symbols)}\n")
            f.write("Productions:\n")
            for production in self.production_list:
                f.write(f"{production}\n")

    def read(self, path: str) -> None:
        with open(path, "r") as f:
            blocks = f.read().split("\n@ ")

        symbol_lines: List[str] = blocks[0].split("\n")
        blocks: List[str] = blocks[1:]

        self.terminal_symbols = symbol_lines[0].split(" ")[1:]
        self.variable_symbols = symbol_lines[1].split(" ")[1:]
        self.start_symbol = self.variable_symbols[0]

        for block in blocks:
            lines = block.split("\n")
            production_line = lines[0]
            code_lines = lines[1:] if len(lines) > 1 else []
            from_state, production = production_line.split(" → ")

            current_grammar_production = Grammar_Production(from_state)
            current_grammar_production.code = "\n".join(code_lines)
            items = production.split(" ")

            for item in items:
                if item in self.terminal_symbols + ["ε"]:
                    current_grammar_production.add(True, item)
                elif item in self.variable_symbols:
                    current_grammar_production.add(False, item)
                else:
                    console.print(f"Unknown symbol '{item}' in grammar file", style="bold red")
                    exit(-1)

            self.production_list.append(current_grammar_production)
