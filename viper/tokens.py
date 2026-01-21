from enum import Enum
from string import ascii_letters

from position import Position

# --------x--------x--------x--------
# $ Constants
DIGITS: list[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LETTERS: list[str] = list(ascii_letters)
# --------x--------x--------x--------

# --------x--------x--------x--------
# $ Token
class TokenFamily(Enum):
    LITERAL = 'LITERAL'
    ARITHMETICOP = 'ARITHMETICOP'
    COMPOP = 'COMPOP'
    ASSIGNOP = 'ASSIGN'
    LOGICALOP = 'LOGICALOP'
    KEYWORD = 'KEYWORD'
    PUNCTUATOR = 'PUNCTUATOR'
    IDENTIFIER = 'IDENTIFIER'

    @staticmethod
    def getTokenFamily(tokenType: Enum):
        return getattr(TokenFamily, tokenType.__class__.__name__.upper())

class Literal(Enum):
    NUM = 'NUM'
    STRING = 'STRING'
    BOOL = 'BOOL'

BOOLS = (('True', 'true', 'TRUE'), ('False', 'false', 'FALSE'))

class ArithmeticOp(Enum):
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    STAR = 'STAR'
    SLASH = 'SLASH'
    DOUBLESTAR = 'DOUBLESTAR'

class CompOp(Enum):
    LESS = 'LESS'
    GREATER = 'GREATER'
    LESSEQUAL = 'LESSEQUAL'
    GREATEREQUAL = 'GREATEREQUAL'
    EQEQUAL = 'EQEQUAL'
    NOTEQUAL = 'NOTEQUAL'

class AssignOp(Enum):
    EQUAL = 'EQUAL'
    PLUSEQUAL = 'PLUSEQUAL'
    MINUSEQUAL = 'MINUSEQUAL'
    STAREQUAL = 'STAREQUAL'
    SLASHEQUAL = 'SLASHEQUAL'
    DOUBLESTAREQUAL = 'DOUBLESTAREQUAL'

class LogicalOp(Enum):
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'

class Keyword(Enum):
    IF = 'IF'
    ELIF = 'ELIF'
    ELSE = 'ELSE'
    FOR = 'FOR'
    WHILE = 'WHILE'
    RETURN = 'RETURN'

# $ Keywords
KEYWORDS: dict[str, Keyword] = {
    'if': Keyword.IF,
    'elif': Keyword.ELIF,
    'else': Keyword.ELSE,
    'for': Keyword.FOR,
    'while': Keyword.WHILE,
    'return': Keyword.RETURN
}

# $ Operators
OPERATORS: dict[str, ArithmeticOp | CompOp | AssignOp | LogicalOp] = {
    '+': ArithmeticOp.PLUS,
    '-': ArithmeticOp.MINUS,
    '*': ArithmeticOp.STAR,
    '/': ArithmeticOp.SLASH,
    '**': ArithmeticOp.DOUBLESTAR,
    '^': ArithmeticOp.DOUBLESTAR,
    '<': CompOp.LESS,
    '>': CompOp.GREATER,
    '<=': CompOp.LESSEQUAL,
    '>=': CompOp.GREATEREQUAL,
    '==': CompOp.EQEQUAL,
    '!=': CompOp.NOTEQUAL,
    '=': AssignOp.EQUAL,
    '+=': AssignOp.PLUSEQUAL,
    '-=': AssignOp.MINUSEQUAL,
    '*=': AssignOp.STAREQUAL,
    '/=': AssignOp.SLASHEQUAL,
    '^=': AssignOp.DOUBLESTAREQUAL,
    'and': LogicalOp.AND,
    '&&': LogicalOp.AND,
    'or': LogicalOp.OR,
    '|': LogicalOp.OR,
    'not': LogicalOp.NOT,
    '!': LogicalOp.NOT
}

OPERATORFIRSTCHAR = ['&']

# $ Punctuators
class Punctuator(Enum):
    SEMI = 'SEMI'
    DOT = 'DOT'
    EOF = 'EOF'

PUNCTUATORS = {
    ';': Punctuator.SEMI,
    '.': Punctuator.DOT
}

class Separator(Enum):
    LPAR = 'LPAR'
    RPAR = 'RPAR'
    LSQB = 'LSQB'
    RSQB = 'RSQB'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    COMMA = 'COMMA'

SEPARATORS = {
    '(': Separator.LPAR,
    ')': Separator.RPAR,
    '[': Separator.LSQB,
    ']': Separator.RSQB,
    '{': Separator.LBRACE,
    '}': Separator.RBRACE,
    ',': Separator.COMMA,

}

class Identifier(Enum):
    FUNCDEF = 'FUNCDEF'
    FUNCCALL = 'FUNCCALL'
    INBUILTFUNC = 'INBUILTFUNC'
    VARIABLE = 'VARIABLE'
    DATATYPE = 'DATATYPE'

class Token:
    def __init__(
        self,
        familyType: TokenFamily,
        tokenType: Literal | ArithmeticOp | CompOp | AssignOp | LogicalOp | Keyword | Punctuator | Separator | TokenFamily,
        value: str,
        beginPos: Position,
        endPos: Position | None = None,
    ) -> None:
        self.familyType = familyType
        self.tokenType = tokenType
        self.value = value
        self.beginPos = beginPos
        if endPos == None: self.endPos = beginPos
        else: self.endPos = endPos
    
    def __repr__(self) -> str:
        return f'{self.value}'