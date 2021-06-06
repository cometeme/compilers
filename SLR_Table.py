import csv
import json
from copy import deepcopy
from pprint import pformat
from typing import Dict, List

from rich.console import Console
from rich.table import Table

from Grammar import Grammar

console = Console()


class ItemSet:
    def __init__(self):
        self.index = 0
        self.closure_items = set()  # closure of one item
        self.transfer = dict()  # store transfer dict

    def get_index(self):
        return self.index

    def set_index(self, index: int):
        self.index = index

    def add_trans(self, symbol: str, next_index: int):
        self.transfer[symbol] = next_index

    def exists(self, item: tuple) -> bool:
        return item in self.closure_items

    def add(self, item: tuple) -> None:
        self.closure_items.add(item)

    def equal(self, other) -> bool:
        if len(self.closure_items) != len(other.closure_items):
            return False

        for item in self.closure_items:
            if item not in other.closure_items:
                return False

        return True


class ClosureFamily:
    def __init__(self):
        self.clourse_set = list()

    def exists(self, item: ItemSet) -> bool:
        contain = False
        for itemset in self.clourse_set:
            if itemset.equal(item):
                contain = True
                break

        return contain

    def indexOf(self, item: ItemSet) -> int:
        index = -1
        for itemset in self.clourse_set:
            if itemset.equal(item):
                index = itemset.get_index()
                break

        return index

    def add(self, item: ItemSet) -> None:
        self.clourse_set.append(item)


class SLR_Table:
    def __init__(self, grammar: Grammar) -> None:
        self.grammar = grammar

        self.start_symbol = grammar.start_symbol
        self.action_symbols = grammar.terminal_symbols
        self.goto_symbols = grammar.variable_symbols[1:]
        self.all_symbols = self.goto_symbols + self.action_symbols

        self.all_items = list()
        self.first_items = dict()  # item with first dot, key is from_state
        self.gen_all_items()

        self.C = self.gen_clourse_set([(0, 0)])  # clourse set

        self.first = self.first_set()
        self.follow = self.follow_set()

    def print_first_set(self) -> None:
        console.print("First Set:", style="bold")
        console.print(self.first)

    def print_follow_set(self) -> None:
        console.print("Follow Set:", style="bold")
        console.print(self.follow)

    def print_closure_set(self):
        console.print(f"Num of states: {len(self.C.clourse_set)}", style="bold")
        for index, clourse in enumerate(self.C.clourse_set):
            output_table = Table(
                show_header=True,
                header_style="bold",
            )
            output_table.add_column(f"I{clourse.index}", justify="left")
            for item in clourse.closure_items:
                output_table.add_row(self.get_item(item))
            # print(clourse.transfer)
            console.print(output_table)

    def save(self) -> None:
        with open("output/first_set.txt", "w") as f:
            for k in self.first:
                f.write(f"first({k}) = {self.first[k]}\n")

        with open("output/follow_set.txt", "w") as f:
            for k in self.follow:
                f.write(f"follow({k}) = {self.follow[k]}\n")

        with open("output/closure_set.txt", "w") as f:
            for index, clourse in enumerate(self.C.clourse_set):
                f.write(f"I{index}\n")
                for item in clourse.closure_items:
                    f.write(f"{self.get_item(item)}\n")
                f.write("\n")

        save_slr_table(self.grammar)

    def get_item(self, item: tuple) -> str:
        production = self.grammar.production_list[item[0]]
        right = [it.value for it in production.items]

        if "ε" in right:  # remove ε
            right.remove("ε")

        right.insert(item[1], ".")
        return f"{production.from_state} → {' '.join(right)}"

    def contain_varepsilon(self, symbol: str) -> bool:
        contain = False
        if self.first_items.get(symbol) is None:
            return False

        for indices in self.first_items.get(symbol):
            for index in indices:
                for item in self.grammar.production_list[index].items:
                    if item.value == "ε":
                        contain = True
                        break

        return contain

    def get_first(self, first: dict, symbol: str):
        indices = [production[0] for production in self.first_items[symbol]]  # production indices
        for index in indices:
            item = self.grammar.production_list[index].items[0]
            if not item.is_symbol and item.value != symbol:
                first[symbol] |= set(self.get_first(first, item.value))  # recurse

        return first.get(symbol)

    def first_set(self):
        first = dict()

        for item in self.action_symbols:
            first[item] = item

        for from_state in self.first_items.keys():
            indices = [production[0] for production in self.first_items[from_state]]  # production indices
            first[from_state] = set()

            for index in indices:
                item = self.grammar.production_list[index].items[0]
                if item.is_symbol:  # add end symbol to First(from_state)
                    first[from_state].add(item.value)

        for from_state in self.first_items.keys():
            indices = [production[0] for production in self.first_items[from_state]]  # production indices
            for index in indices:
                item = self.grammar.production_list[index].items[0]
                # add var symbol to First(from_state)
                if not item.is_symbol and item.value != from_state:
                    first[from_state] |= set(self.get_first(first, item.value))

        for from_state in self.first_items.keys():
            indices = [production[0] for production in self.first_items[from_state]]  # production indices
            add_varepsilon = False
            for index in indices:
                items = self.grammar.production_list[index].items
                length = len(items)
                if items[0].value == "ε":
                    add_varepsilon = True
                # solve ε production to First(from_state)
                cur = 0
                while cur < length and not items[cur].is_symbol:
                    if self.contain_varepsilon(items[cur].value):
                        add_varepsilon = True
                        if cur + 1 < length:
                            first[from_state] |= set(first[items[cur + 1].value])
                    cur += 1

            if add_varepsilon:
                first[from_state].add("ε")

        return first

    def follow_set(self):
        follow = dict()
        for from_state in self.first_items.keys():
            follow[from_state] = set()

        follow[self.start_symbol].add("$")  # for begin symbol, add '$'

        for production in self.grammar.production_list:
            items = production.items
            length = len(items)
            cur = 0
            while cur < length:
                if not items[cur].is_symbol:
                    if cur + 1 < length and items[cur + 1].is_symbol:  # B→αAa ,a is end symbol
                        follow[items[cur].value].add(items[cur + 1].value)
                    elif cur + 1 < length and not items[cur + 1].is_symbol:  # B→αAX ,X is not end symbol
                        first_of_next = deepcopy(self.first[items[cur + 1].value])
                        if "ε" in first_of_next:
                            first_of_next.remove("ε")
                        follow[items[cur].value] |= first_of_next
                cur += 1

        for production in self.grammar.production_list:
            items = production.items
            length = len(items)
            cur = 0
            while cur < length:
                if not items[cur].is_symbol:
                    if cur + 1 >= length:
                        follow[items[cur].value] |= follow[production.from_state]
                    elif cur + 1 < length and self.contain_varepsilon(items[cur + 1].value):
                        follow[items[cur].value] |= follow[production.from_state]
                cur += 1

        return follow

    def gen_all_items(self):
        for index, production in enumerate(self.grammar.production_list):

            # store item which dot at first
            if not self.first_items.get(production.from_state):
                self.first_items[str(production.from_state)] = [(index, 0)]
            else:
                self.first_items[str(production.from_state)].append((index, 0))

            for dot, item in enumerate(production.items):
                self.all_items.append((index, dot))

            if len(production.items) > 1 and production.items[0].value != "ε":  # except ε
                self.all_items.append((index, len(production.items)))

    def get_clourse(self, items: list) -> ItemSet:
        queue = [item for item in items]  # add items to queue
        close_set = ItemSet()  # clourse for items
        while queue:
            item = queue.pop(0)
            close_set.add(item)
            candidate = self.grammar.production_list[item[0]]  # all candidate production

            if len(candidate.items) != item[1]:  # dot not at end of production
                if not candidate.items[item[1]].is_symbol:
                    for it in self.first_items[candidate.items[item[1]].value]:
                        if not close_set.exists(it):  # item not in close_set
                            queue.append(it)
                            close_set.add(it)

        return close_set

    def goto(self, itemset: ItemSet, symbol: str):
        next_state = ItemSet()
        for item in itemset.closure_items:
            production = self.grammar.production_list[item[0]]

            if item[1] != len(production.items):  # dot not at the end
                if production.items[item[1]].value == symbol:  # match ,goto next state
                    next_state.add((item[0], item[1] + 1))

        return self.get_clourse([item for item in next_state.closure_items])

    def gen_clourse_set(self, start: list) -> ClosureFamily:
        C = ClosureFamily()
        C.add(self.get_clourse(start))

        queue = [clourse for clourse in C.clourse_set]
        index = 1
        while queue:
            clourse = queue.pop(0)

            for symbol in self.all_symbols:
                next = self.goto(clourse, symbol)
                if len(next.closure_items) != 0 and not C.exists(next):  # if next_state not in closure set
                    next.set_index(index)
                    index += 1

                    clourse.add_trans(symbol, next.get_index())
                    C.add(next)
                    queue.append(next)
                elif len(next.closure_items) != 0 and C.exists(next):  # if consists , add to transfer dict
                    clourse.add_trans(symbol, C.indexOf(next))

        return C

    def analysis_table(self):
        action = list()
        goto = list()

        # C = self.gen_clourse_set([(0, 0)])

        for i in range(len(self.C.clourse_set)):
            action.append(dict())
            goto.append(dict())

        for clourse in self.C.clourse_set:
            for item in clourse.closure_items:
                production = self.grammar.production_list[item[0]]

                if item[1] != len(production.items):  # dot not at the end
                    symbol = production.items[item[1]]

                    # solve A → ε
                    if symbol.is_symbol and symbol.value == "ε":
                        for f in self.follow[production.from_state]:
                            action[clourse.get_index()][f] = "r" + str(item[0])

                    # get next closure index
                    next_index = clourse.transfer.get(symbol.value)

                    if next_index is not None:
                        if symbol.is_symbol and symbol.value != "ε":
                            action[clourse.get_index()][symbol.value] = "s" + str(next_index)
                        else:
                            goto[clourse.get_index()][symbol.value] = next_index

                else:  # item[1] == len(production.items) , dot at the end
                    if production.from_state == self.start_symbol:
                        action[clourse.get_index()]["$"] = "acc"
                    else:
                        for f in self.follow[production.from_state]:
                            action[clourse.get_index()][f] = "r" + str(item[0])

        with open("action_table.json", "w") as f:
            f.write(json.dumps(action, indent=2))

        with open("goto_table.json", "w") as f:
            f.write(json.dumps(goto, indent=2))


def print_slr_table(grammar: Grammar) -> None:
    action_table_symbols: List[str] = grammar.terminal_symbols
    goto_table_symbols: List[str] = grammar.variable_symbols[1:]

    with open("action_table.json", "r") as f:
        action_table: List[Dict[str, str]] = json.loads(f.read())
    with open("goto_table.json", "r") as f:
        goto_table: List[Dict[str, int]] = json.loads(f.read())

    output_table = Table(
        show_header=True,
        header_style="bold",
    )

    output_table.add_column("State", justify="center")
    for action_table_symbol in action_table_symbols:
        output_table.add_column(action_table_symbol, justify="center")
    for goto_table_symbol in goto_table_symbols:
        output_table.add_column(goto_table_symbol, justify="center")

    for state, action_row, goto_row in zip(range(len(action_table)), action_table, goto_table):
        output_row: List[str] = [str(state)]
        for action_symbol in action_table_symbols:
            output_row.append(action_row.get(action_symbol, ""))
        for goto_symbol in goto_table_symbols:
            output_row.append(str(goto_row.get(goto_symbol, "")))
        output_table.add_row(*output_row)

    console.print("SLR Table (Action/Goto Table):", style="bold")
    console.print(output_table)


def save_slr_table(grammar: Grammar) -> None:
    action_table_symbols: List[str] = grammar.terminal_symbols
    goto_table_symbols: List[str] = grammar.variable_symbols[1:]

    with open("action_table.json", "r") as f:
        action_table: List[Dict[str, str]] = json.loads(f.read())
    with open("goto_table.json", "r") as f:
        goto_table: List[Dict[str, int]] = json.loads(f.read())

    with open("output/slr_table.csv", "w") as f:
        writter = csv.writer(f)
        header: List[str] = ["State"] + action_table_symbols + goto_table_symbols
        writter.writerow(header)

        for state, action_row, goto_row in zip(range(len(action_table)), action_table, goto_table):
            output_row: List[str] = [str(state)]
            for action_symbol in action_table_symbols:
                output_row.append(action_row.get(action_symbol, ""))
            for goto_symbol in goto_table_symbols:
                output_row.append(str(goto_row.get(goto_symbol, "")))
            writter.writerow(output_row)


if __name__ == "__main__":
    grammar = Grammar()
    grammar.read("grammar.txt")

    slr = SLR_Table(grammar)
    slr.analysis_table()

    print_slr_table(grammar)
