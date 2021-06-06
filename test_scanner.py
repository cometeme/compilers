from rich import box
from rich.console import Console
from rich.table import Table

from Scanner import Scanner
from Symbol_Table import Symbol_Table
from Token import Token

if __name__ == "__main__":
    # init output
    console = Console()
    symbol_table = Symbol_Table()

    # run scanner
    with open("input/input.txt", "r") as f:
        scanner = Scanner(f.read(), symbol_table)

    while scanner.has_next():
        token: Token = scanner.get_next()

    # print results
    scanner.print_states()
    scanner.print_tokens()

    symbol_table.save()
    scanner.save()
