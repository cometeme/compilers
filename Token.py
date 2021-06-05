from enum import Enum, auto
from typing import Union


class Token_Type(Enum):
    ID = auto()  # identifier
    CONST = auto()  # constant (number)
    ASSIGN = auto()  # assign symbol '='
    ALOP = auto()  # arithmetic operator (+, -, *, /)
    RELOP = auto()  # relation operator (<, >, <=, >=, ==, !=)
    LBRACKET = auto()  # left bracket '('
    RBRACKET = auto()  # right bracket ')'
    SEMICOLON = auto()  # semicolon ';'
    IF = auto()  # if
    ELSE = auto()  # else
    WHILE = auto()  # while
    INT = auto()  # int
    FLOAT = auto()  # float


class Token:
    token_type: Union[Token_Type, None]
    content: Union[str, int, None]  # str for name, int for entry

    def __init__(self) -> None:
        self.token_type = None  # type of the token
        self.content = None  # detail content (like identifier name or operator type)

    def to_string(self) -> str:
        if self.token_type in [Token_Type.ALOP, Token_Type.RELOP]:
            return str(self.content)
        elif self.token_type == Token_Type.ASSIGN:
            return "="
        elif self.token_type == Token_Type.LBRACKET:
            return "("
        elif self.token_type == Token_Type.RBRACKET:
            return ")"
        elif self.token_type == Token_Type.SEMICOLON:
            return ";"
        return self.token_type.name.lower()

    def __str__(self) -> str:
        return f"{self.token_type.name}, {'' if self.content is None else self.content}"
