from rich.console import Console

from Grammar import Grammar
from Scanner import Scanner
from SLR_Automata import SLR_Automata
from Symbol_Table import Symbol_Table

console = Console()

if __name__ == "__main__":
    symbol_table = Symbol_Table()

    # init grammar
    grammar = Grammar()
    grammar.read("grammar_test.txt")

    # init scanner
    with open("input_test.txt", "r") as f:
        scanner = Scanner(f.read(), symbol_table)

    # init slr automata
    slr = SLR_Automata(scanner, grammar)
    slr.run()
    slr.output()
