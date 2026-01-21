from __future__ import annotations

from inbuilt import Primitive
from nodes import FunctionNode
from tokens import Identifier

symbols: dict[str, tuple[Identifier | None, FunctionNode | Primitive | None]] = {
    'num': (Identifier.DATATYPE, None),
    'bool': (Identifier.DATATYPE, None),
    'String': (Identifier.DATATYPE, None),
    'print': (Identifier.INBUILTFUNC, None),
    'sum': (Identifier.INBUILTFUNC, None),
    'inputExpr': (Identifier.INBUILTFUNC, None),
    'inputNum': (Identifier.INBUILTFUNC, None),
}

class SymbolTable:
    def __init__(self, symbols: dict[str, tuple[Identifier | None, FunctionNode | Primitive | None]] = symbols, parentSymbols: SymbolTable | None = None) -> None:
        self.symbols = symbols
        self.parentSymbols = parentSymbols

    def add(self, identifier: str, type: Identifier | None, value: Primitive | FunctionNode):
        self.symbols[identifier] = (type, value)
    
    def update(self, identifier: str, value: Primitive):
        dataType = self.symbols[identifier][0]
        self.symbols[identifier] = (dataType, value)

    def get(self, identifier: str) -> Primitive | FunctionNode | None:
        if identifier in self.symbols:
            return self.symbols[identifier][1]
        else:
            if self.parentSymbols != None: return self.parentSymbols.get(identifier)
            else: raise KeyError

    def __contains__(self, identifier: 'str'):
        if identifier in self.symbols: return True
        if self.parentSymbols != None: return identifier in self.parentSymbols
        return False

    def __repr__(self) -> str:
        return f'{self.symbols}'