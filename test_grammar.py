from Grammar import Grammar
from rich import console
from rich.console import Console

console = Console()

grammar = Grammar()
grammar.read('grammar.txt')

for production in grammar.production_list:
    console.print(f"{production.from_state} ->", end='')

    for item in production.items:
        if item.is_symbol:
            console.print(f" [bold red]{item.value}[/bold red]", end='')
        else:
            console.print(f" {item.value}", end='')
    
    console.print('')