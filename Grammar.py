from typing import List

from Token import Token_Type


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


class Grammar:
    production_list: List[Grammar_Production]

    def __init__(self) -> None:
        self.production_list = list()

    def read(self, path: str) -> None:
        with open(path, "r") as f:
            lines = f.read().split("\n")

        for line in lines:
            from_state, production = line.split(" → ")
            from_state = from_state[1:]  # strip '#'

            current_grammar_production = Grammar_Production(from_state)
            items = production.split(" ")

            for item in items:
                if item.startswith("#"):
                    # variable
                    current_grammar_production.add(False, item[1:])
                else:
                    # symbol
                    current_grammar_production.add(True, item)

            self.production_list.append(current_grammar_production)
