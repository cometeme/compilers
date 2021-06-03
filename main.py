from rich import box
from rich.console import Console
from rich.table import Table

from Scanner import Scanner
from Symbol_Table import Symbol_Table
from Token import Token

if __name__ == "__main__":
    # init output
    console = Console()
    token_output = Table(
        show_header=True,
        header_style="bold",
    )

    token_output.add_column("Type", justify="center")
    token_output.add_column("Content", justify="center")

    token_output = Table(
        show_header=True,
        header_style="bold",
    )

    token_output.add_column("Type", justify="center")
    token_output.add_column("Content", justify="center")

    symbol_table_output = Table(
        show_header=True,
        header_style="bold",
    )

    symbol_table_output.add_column("Name", justify="center")
    symbol_table_output.add_column("Var/Const", justify="center")
    symbol_table_output.add_column("Type", justify="center")

    symbol_table = Symbol_Table()

    # run scanner
    with open("input.txt", "r") as f:
        s = Scanner(f.read(), symbol_table)

    while s.has_next():
        token: Token = s.get_next(output=True)
        token_output.add_row(token.token_type.name, "" if token.content is None else str(token.content))

    for item in symbol_table.table:
        symbol_table_output.add_row(
            item.name, "Var" if item.variable else "Const", "None" if item.item_type is None else item.item_type.name
        )

    # print results

    console.print("Tokens:")
    console.print(token_output)

    console.print("Symbol Table:")
    console.print(symbol_table_output)
