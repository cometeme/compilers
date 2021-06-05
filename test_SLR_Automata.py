from rich.console import Console

from Grammar import Grammar
from Scanner import Scanner
from SLR_Automata import SLR_Automata
from Symbol_Table import Symbol_Table
from SLR_Table import SLR_Table, print_slr_table

console = Console()

if __name__ == "__main__":
    symbol_table = Symbol_Table()

    # init grammar
    grammar = Grammar()
    grammar.read("grammar.txt")

    # init scanner
    with open("input.txt", "r") as f:
        scanner = Scanner(f.read(), symbol_table)

    # generate and print slr table
    slr = SLR_Table(grammar)
    slr.analysis_table()

    print_slr_table(grammar)

    # init slr automata
    slr = SLR_Automata(scanner, grammar)
    slr.run()
    slr.output()
