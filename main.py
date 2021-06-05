from rich.console import Console

from Grammar import Grammar
from Scanner import Scanner
from SLR_Automata import SLR_Automata
from SLR_Table import SLR_Table, print_slr_table
from Symbol_Table import Symbol_Table

console = Console()

message = """
---------------------------------------------------
Enter a number to show detail, or enter 'q' to quit

0 - Grammar
1 - Input Code
2 - Scanner States
3 - SLR States
4 - Token Table
5 - Symbol Table
6 - First Set
7 - Follow Set
8 - Closure Set
9 - SLR Table (Action/Goto Table)
10 - Output Code
---------------------------------------------------
"""

if __name__ == "__main__":
    symbol_table = Symbol_Table()

    # init grammar
    grammar = Grammar()
    grammar.read("grammar.txt")

    # init scanner
    with open("input.txt", "r") as f:
        code = f.read()
    scanner = Scanner(code, symbol_table)

    # generate and print slr table
    slr_table = SLR_Table(grammar)
    slr_table.analysis_table()

    # init slr automata
    slr_automata = SLR_Automata(scanner, grammar)
    slr_automata.run(debug=False)

    # save result
    grammar.save()
    symbol_table.save()
    scanner.save()
    slr_table.save()
    slr_automata.save()

    # output result'
    while True:
        console.print(message)
        input_string = input("> ")
        print("")

        if input_string == "0":
            # Grammar
            console.print(f"Grammar:", style="bold")
            console.print(f"Terminal Symbols: {grammar.terminal_symbols}")
            console.print(f"Variable Symbols: {grammar.variable_symbols}")

            for production in grammar.production_list:
                console.print(f"{production.from_state} →", end="")

                for item in production.items:
                    if item.is_symbol:
                        console.print(f" {item.value}", style="bold red", end="")
                    else:
                        console.print(f" {item.value}", end="")

                console.print("")
        elif input_string == "1":
            # Input Code
            console.print(f"Input Code:", style="bold")
            print(code)
        elif input_string == "2":
            # Scanner States
            scanner.print_states()
        elif input_string == "3":
            # SLR States
            slr_automata.print_state()
        elif input_string == "4":
            # Token Table
            scanner.print_tokens()
        elif input_string == "5":
            # Symbol Table
            symbol_table.output()
        elif input_string == "6":
            # First Set
            slr_table.print_first_set()
        elif input_string == "7":
            # Follow Set
            slr_table.print_follow_set()
        elif input_string == "8":
            # Closure Set
            slr_table.print_closure_set()
        elif input_string == "9":
            # SLR Table (Action/Goto Table)
            print_slr_table(grammar)
        elif input_string == "10":
            # Output Code
            slr_automata.print_code()
        elif input_string == "q":
            # quit
            exit(0)
        else:
            console.print(f"Unknown input {input_string}!")
