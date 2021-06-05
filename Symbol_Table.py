from enum import Enum, auto
from typing import List, Union

from rich.console import Console
from rich.table import Table

console = Console()


class Table_Item_Type(Enum):
    INT = auto()
    FLOAT = auto()


class Table_Item:
    name: Union[str, None]
    variable: Union[bool, None]  # True for variable, False for constant
    item_type: Union[Table_Item_Type, None]

    def __init__(self) -> None:
        self.name = None
        self.variable = None
        self.item_type = None

    def __str__(self) -> str:
        return f"{self.name}, {'var' if self.variable else 'const'}, {'' if self.item_type is None else self.item_type.name}"


class Symbol_Table:
    size: int
    table: List[Table_Item]

    def __init__(self) -> None:
        self.size = 0
        self.table = list()

    def output(self) -> None:
        output_table = Table(
            show_header=True,
            header_style="bold",
        )
        output_table.add_column("Name", justify="center")
        output_table.add_column("Var/Const", justify="center")
        output_table.add_column("Type", justify="center")

        for item in self.table:
            output_table.add_row(
                item.name, "Var" if item.variable else "Const", "" if item.item_type is None else item.item_type.name
            )

        console.print("Symbol Table:", style="bold")
        console.print(output_table)

    def get_size(self) -> int:
        return self.size

    def find_item_by_name(self, name: str) -> int:
        for idx, item in enumerate(self.table):
            if item.name == name:
                return idx

        return -1  # cannot find

    def add_item(self, item: Table_Item) -> int:
        self.size += 1
        self.table.append(item)
        return self.size - 1

    def get_item_by_index(self, idx: int) -> Table_Item:
        if idx < 0 or idx > self.size:
            print("Index out of range in Symbol Table")
            exit(-1)

        return self.table[idx]
