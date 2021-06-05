import json
from typing import Dict, List

from rich.console import Console
from rich.table import Table

console = Console()


def print_action_and_goto(
    action_table_symbol_list: List[str],
    goto_table_symbol_list: List[str],
    action_table: List[Dict[str, str]],
    goto_table: List[Dict[str, int]],
):
    output_table = Table(
        show_header=True,
        header_style="bold",
    )

    output_table.add_column("State", justify="center")
    for action_table_symbol in action_table_symbol_list:
        output_table.add_column(action_table_symbol, justify="center")
    for goto_table_symbol in goto_table_symbol_list:
        output_table.add_column(goto_table_symbol, justify="center")

    for state, action_row, goto_row in zip(range(len(action_table)), action_table, goto_table):
        output_row: List[str] = [str(state)]
        for action_symbol in action_table_symbol_list:
            output_row.append(action_row.get(action_symbol, ""))
        for goto_symbol in goto_table_symbol_list:
            output_row.append(str(goto_row.get(goto_symbol, "")))
        output_table.add_row(*output_row)

    console.print("Action/Goto Table:", style="bold")
    console.print(output_table)


if __name__ == "__main__":
    with open("action_table_symbols.json", "r") as f:
        action_table_symbols: List[str] = json.loads(f.read())
    with open("goto_table_symbols.json", "r") as f:
        goto_table_symbols: List[str] = json.loads(f.read())
    with open("action_table.json", "r") as f:
        action_table: List[Dict[str, str]] = json.loads(f.read())
    with open("goto_table.json", "r") as f:
        goto_table: List[Dict[str, int]] = json.loads(f.read())

    print_action_and_goto(action_table_symbols, goto_table_symbols, action_table, goto_table)
