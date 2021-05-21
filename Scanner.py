from enum import Enum, auto
from string import ascii_letters, digits, printable

from Token import Token, Token_Type


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
    Scanner_State.NUMBER: Token_Type.CONSTANT,
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
    def __init__(self, code: str) -> None:
        """init the scanner

        Args:
            `code` (str): raw code that needs to be processed
        """
        self.pnt: int = 0
        self.code: str = code.replace("\n", "").replace("\r", "").strip(" ")  # erase line split
        self.code = self.code + "\0"  # add '\0' at the end for convenience
        self.len: int = len(self.code)

    def has_next(self) -> bool:
        """check whether the scanner has next token to output

        Returns:
            `bool`: `True` if the scanner have next token
        """
        return self.pnt < self.len - 1

    def get_next(self, output: bool = True) -> Token:
        """get next token

        Args:
            `output` (bool, optional): Set to `True` to show scan process. Defaults to `True`.

        Returns:
            `Token`: The next token
        """
        current_state: Scanner_State = Scanner_State.START
        temp: str = ""
        result: Token = Token()

        while True:
            cur: str = self.code[self.pnt]

            transition = SCANNER_TRANSITION[current_state]
            next_state: Scanner_State = Scanner_State.ERROR  # default is error

            # find next state
            for pattern, to_state in transition:
                if cur in pattern:
                    if to_state == Scanner_State.END:
                        result.set_token_type(STATE_TO_TOKEN[current_state])
                        result.set_content(temp)
                        return result

                    next_state = to_state
                    break

            if output:
                print(f"pnt = {self.pnt}, cur = {cur}\t{current_state} -> {next_state}")

            if next_state == Scanner_State.ERROR:
                print("ERROR WHEN GETTING NEXT TOKEN!")
                exit(-1)

            # step to next state
            current_state = next_state
            if cur != " ":
                temp += cur
            self.pnt += 1
