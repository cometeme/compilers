from rich import box
from rich.console import Console
from rich.table import Table

from Scanner import Scanner
from Token import Token

if __name__ == "__main__":
    # init output
    console = Console()
    table = Table(
        show_header=True,
        header_style="bold",
    )

    table.add_column("Type", justify="center")
    table.add_column("Content", justify="center")

    # run scanner
    with open("input.txt", "r") as f:
        s = Scanner(f.read())

    while s.has_next():
        token: Token = s.get_next(output=True)
        table.add_row(token.get_token_type().name, token.get_content())

    console.print(table)
