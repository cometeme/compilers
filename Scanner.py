from enum import Enum, auto
from string import ascii_letters, digits, printable

from rich.console import Console
from rich.table import Table

from Symbol_Table import Symbol_Table, Table_Item, Table_Item_Type
from Token import Token, Token_Type

console = Console()


class Scanner_State(Enum):
    START = auto()
    # identifier
    ID = auto()
    # assign symbol '='
    ASSIGN = auto()
    # arithmetic operator (+, -, *, /)
    ALOP = auto()
    # relation operator
    L_G = auto()  # less '<' or greater '>'
    LE_GE = auto()  # less equal '<=' or greater equal '>='
    EQ = auto()  # equal '=='
    NOT = auto()  # not '!'
    NEQ = auto()  # not equal '!='
    # bracket
    LBRACKET = auto()  # left bracket '('
    RBRACKET = auto()  # right bracket ')'
    # semicolon
    SEMICOLON = auto()  # semicolon ';'
    # "if"
    I = auto()
    IF = auto()
    # "int"
    IN = auto()
    INT = auto()
    # "else"
    E = auto()
    EL = auto()
    ELS = auto()
    ELSE = auto()
    # "while"
    W = auto()
    WH = auto()
    WHI = auto()
    WHIL = auto()
    WHILE = auto()
    # float
    F = auto()
    FL = auto()
    FLO = auto()
    FLOA = auto()
    FLOAT = auto()
    # number
    NUMBER = auto()
    # end of the token
    END = auto()
    # not a vaild token
    ERROR = auto()


# map from scanner state to token type
STATE_TO_TOKEN = {
    Scanner_State.ID: Token_Type.ID,
    Scanner_State.ASSIGN: Token_Type.ASSIGN,
    Scanner_State.ALOP: Token_Type.ALOP,
    Scanner_State.L_G: Token_Type.RELOP,
    Scanner_State.LE_GE: Token_Type.RELOP,
    Scanner_State.EQ: Token_Type.RELOP,
    Scanner_State.NEQ: Token_Type.RELOP,
    Scanner_State.LBRACKET: Token_Type.LBRACKET,
    Scanner_State.RBRACKET: Token_Type.RBRACKET,
    Scanner_State.SEMICOLON: Token_Type.SEMICOLON,
    Scanner_State.I: Token_Type.ID,
    Scanner_State.IF: Token_Type.IF,
    Scanner_State.IN: Token_Type.ID,
    Scanner_State.INT: Token_Type.INT,
    Scanner_State.E: Token_Type.ID,
    Scanner_State.EL: Token_Type.ID,
    Scanner_State.ELS: Token_Type.ID,
    Scanner_State.ELSE: Token_Type.ELSE,
    Scanner_State.W: Token_Type.ID,
    Scanner_State.WH: Token_Type.ID,
    Scanner_State.WHI: Token_Type.ID,
    Scanner_State.WHIL: Token_Type.ID,
    Scanner_State.WHILE: Token_Type.WHILE,
    Scanner_State.F: Token_Type.ID,
    Scanner_State.FL: Token_Type.ID,
    Scanner_State.FLO: Token_Type.ID,
    Scanner_State.FLOA: Token_Type.ID,
    Scanner_State.FLOAT: Token_Type.FLOAT,
    Scanner_State.NUMBER: Token_Type.CONST,
}


DIGITS = digits  # 0~9

ID_START = ascii_letters + "_"  # a~z + A~Z + _
ID_APPEND = ID_START + digits  # a~z + A~Z + _ + 0~9

ALOPS = "+-*/"
RELOPS = "<>!="

SPACES = " \t\n\r\0"

ID_SEP = ALOPS + RELOPS + "();" + SPACES
NUMBER_SEP = ID_SEP

ANY_SEP = printable + SPACES


ID_TRANSITION_TEMPLATE = [(ID_APPEND, Scanner_State.ID), (ID_SEP, Scanner_State.END)]


SCANNER_TRANSITION = {
    Scanner_State.START: [
        ("i", Scanner_State.I),
        ("e", Scanner_State.E),
        ("w", Scanner_State.W),
        ("f", Scanner_State.F),
        ("(", Scanner_State.LBRACKET),
        (")", Scanner_State.RBRACKET),
        (";", Scanner_State.SEMICOLON),
        ("<>", Scanner_State.L_G),
        ("!", Scanner_State.NOT),
        ("=", Scanner_State.ASSIGN),
        (" ", Scanner_State.START),  # remove space
        (ALOPS, Scanner_State.ALOP),
        (DIGITS, Scanner_State.NUMBER),
        (ID_START, Scanner_State.ID),
    ],
    Scanner_State.ID: ID_TRANSITION_TEMPLATE,
    Scanner_State.ASSIGN: [
        ("=", Scanner_State.EQ),
        (ANY_SEP, Scanner_State.END),
    ],
    Scanner_State.ALOP: [
        (ANY_SEP, Scanner_State.END),
    ],
    Scanner_State.L_G: [
        ("=", Scanner_State.LE_GE),
        (ANY_SEP, Scanner_State.END),
    ],
    Scanner_State.LE_GE: [
        (ANY_SEP, Scanner_State.END),
    ],
    Scanner_State.EQ: [
        (ANY_SEP, Scanner_State.END),
    ],
    Scanner_State.NOT: [
        ("=", Scanner_State.NEQ),
    ],
    Scanner_State.NEQ: [
        (ANY_SEP, Scanner_State.END),
    ],
    Scanner_State.LBRACKET: [
        (ANY_SEP, Scanner_State.END),
    ],
    Scanner_State.RBRACKET: [
        (ANY_SEP, Scanner_State.END),
    ],
    Scanner_State.SEMICOLON: [
        (ANY_SEP, Scanner_State.END),
    ],
    Scanner_State.I: [
        ("f", Scanner_State.IF),
        ("n", Scanner_State.IN),
    ]
    + ID_TRANSITION_TEMPLATE,
    Scanner_State.IF: ID_TRANSITION_TEMPLATE,
    Scanner_State.IN: [
        ("t", Scanner_State.INT),
    ]
    + ID_TRANSITION_TEMPLATE,
    Scanner_State.INT: ID_TRANSITION_TEMPLATE,
    Scanner_State.E: [
        ("l", Scanner_State.EL),
    ]
    + ID_TRANSITION_TEMPLATE,
    Scanner_State.EL: [
        ("s", Scanner_State.ELS),
    ]
    + ID_TRANSITION_TEMPLATE,
    Scanner_State.ELS: [
        ("e", Scanner_State.ELSE),
    ]
    + ID_TRANSITION_TEMPLATE,
    Scanner_State.ELSE: ID_TRANSITION_TEMPLATE,
    Scanner_State.W: [
        ("h", Scanner_State.WH),
    ]
    + ID_TRANSITION_TEMPLATE,
    Scanner_State.WH: [
        ("i", Scanner_State.WHI),
    ]
    + ID_TRANSITION_TEMPLATE,
    Scanner_State.WHI: [
        ("l", Scanner_State.WHIL),
    ]
    + ID_TRANSITION_TEMPLATE,
    Scanner_State.WHIL: [
        ("e", Scanner_State.WHILE),
    ]
    + ID_TRANSITION_TEMPLATE,
    Scanner_State.WHILE: ID_TRANSITION_TEMPLATE,
    Scanner_State.F: [
        ("l", Scanner_State.FL),
    ]
    + ID_TRANSITION_TEMPLATE,
    Scanner_State.FL: [
        ("o", Scanner_State.FLO),
    ]
    + ID_TRANSITION_TEMPLATE,
    Scanner_State.FLO: [
        ("a", Scanner_State.FLOA),
    ]
    + ID_TRANSITION_TEMPLATE,
    Scanner_State.FLOA: [
        ("t", Scanner_State.FLOAT),
    ]
    + ID_TRANSITION_TEMPLATE,
    Scanner_State.FLOAT: ID_TRANSITION_TEMPLATE,
    Scanner_State.NUMBER: [
        (DIGITS, Scanner_State.NUMBER),
        (NUMBER_SEP, Scanner_State.END),
    ],
}


class Scanner:
    pnt: int
    code: str
    length: int
    symbol_table: Symbol_Table

    def __init__(self, code: str, symbol_table: Symbol_Table) -> None:
        """init the scanner

        Args:
            `code` (str): raw code that needs to be processed
            `symbol_table` (Symbol_Table): symbol table for storing variables and constants
        """
        self.pnt = 0
        self.code = code.replace("\n", "").replace("\r", "").strip(" ")  # erase line split
        self.code = self.code + "\0"  # add '\0' at the end for convenience
        self.length = len(self.code)
        self.symbol_table = symbol_table
        # init state output table
        self.state_output = Table(
            show_header=True,
            header_style="bold",
        )
        self.state_output.add_column("Pointer", justify="center")
        self.state_output.add_column("Current Character", justify="center")
        self.state_output.add_column("State Transfer", justify="left")
        # init token output table
        self.token_output = Table(
            show_header=True,
            header_style="bold",
        )
        self.token_output.add_column("Type", justify="center")
        self.token_output.add_column("Content", justify="center")

    def print_states(self) -> None:
        console.print("Scanner States:", style="bold")
        console.print(self.state_output)

    def print_tokens(self) -> None:
        console.print("Tokens:", style="bold")
        console.print(self.token_output)

    def has_next(self) -> bool:
        """check whether the scanner has next token to output

        Returns:
            `bool`: `True` if the scanner have next token
        """
        return self.pnt < self.length - 1

    def get_next(self) -> Token:
        """get next token

        Args:
            `output` (bool, optional): Set to `True` to show scan process. Defaults to `True`.

        Returns:
            `Token`: The next token
        """
        current_state: Scanner_State = Scanner_State.START
        content: str = ""
        result: Token = Token()

        while True:
            cur: str = self.code[self.pnt]

            transition = SCANNER_TRANSITION[current_state]
            next_state: Scanner_State = Scanner_State.ERROR  # default is error

            # find next state
            for pattern, to_state in transition:
                if cur in pattern:
                    if to_state == Scanner_State.END:
                        result.token_type = STATE_TO_TOKEN[current_state]

                        if result.token_type in [Token_Type.ID, Token_Type.CONST]:
                            # for identifier or constant, the content is the entry(index) in symbol table
                            entry: int = self.symbol_table.find_item_by_name(content)
                            if entry == -1:
                                # cannot find, create a new row in symbol table
                                new_item = Table_Item()
                                new_item.name = content
                                new_item.variable = result.token_type == Token_Type.ID
                                entry = self.symbol_table.add_item(new_item)

                            result.content = entry
                        elif result.token_type in [Token_Type.ALOP, Token_Type.RELOP]:
                            # arithmetic operator (+, -, *, /) or relation operator (<, >, <=, >=, ==, !=)
                            result.content = content
                        else:
                            result.content = None

                        self.token_output.add_row(
                            result.token_type.name, "" if result.content is None else str(result.content)
                        )
                        return result

                    next_state = to_state
                    break

            self.state_output.add_row(str(self.pnt), cur, f"{current_state.name} -> {next_state.name}")

            if next_state == Scanner_State.ERROR:
                self.print_tokens()
                self.print_states()
                print("ERROR WHEN GETTING NEXT TOKEN!")
                exit(-1)

            # step to next state
            current_state = next_state
            if cur != " ":
                content += cur
            self.pnt += 1
