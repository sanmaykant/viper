from __future__ import annotations
from nodes import BoolNode, NumberNode, StringNode

class Primitive:
    def __init__(self, value: int | float | str | bool) -> None:
        self.value = value
        self.rectifyDataType()

    def deepCopy(self, value: int | float | str | bool | None = None) -> String | Number | Bool | Primitive:
        if value == None: value = self.value
        if isinstance(value, str):
            return String(value)
        if isinstance(value, bool):
            return Bool(value)
        if isinstance(value, int) or isinstance(value, float): # type: ignore
            return Number(value)
        copy = Primitive(value)
        copy.rectifyDataType()
        return copy

    def rectifyDataType(self):
        if isinstance(self.value, str):
            self.dataType = 'String'
        if isinstance(self.value, int) or isinstance(self.value, float): # type: ignore
            self.dataType = 'num'
        if isinstance(self.value, bool):
            self.dataType = 'bool'

    def __add__(self, other: Primitive):
        try:
            deepCopy = self.deepCopy()
            deepCopy.value += other.value # type: ignore
            deepCopy.rectifyDataType()
            return deepCopy
        except: raise TypeError

    def __sub__(self, other: Primitive):
        try:
            deepCopy = self.deepCopy()
            deepCopy.value -= other.value # type: ignore
            deepCopy.rectifyDataType()
            return deepCopy
        except: raise TypeError

    def __mul__(self, other: Primitive):
        try:
            deepCopy = self.deepCopy()
            deepCopy.value *= other.value # type: ignore
            deepCopy.rectifyDataType()
            return deepCopy
        except: raise TypeError

    def __truediv__(self, other: Primitive):
        try:
            deepCopy = self.deepCopy()
            deepCopy.value /= other.value # type: ignore
            deepCopy.rectifyDataType()
            return deepCopy
        except: raise TypeError

    def __pow__(self, other: Primitive):
        try:
            deepCopy = self.deepCopy()
            deepCopy.value **= other.value # type: ignore
            deepCopy.rectifyDataType()
            return deepCopy
        except: raise TypeError
    
    def __and__(self, other: Primitive):
        try:
            deepCopy = self.deepCopy()
            deepCopy.value &= other.value # type: ignore
            deepCopy.rectifyDataType()
            return deepCopy
        except: raise TypeError

    def __or__(self, other: Primitive):
        try:
            deepCopy = self.deepCopy()
            deepCopy.value |= other.value # type: ignore
            deepCopy.rectifyDataType()
            return deepCopy
        except: raise TypeError

    def __neg__(self):
        try:
            deepCopy = self.deepCopy()
            deepCopy.value = - deepCopy.value # type: ignore
            deepCopy.rectifyDataType()
            return deepCopy
        except: raise TypeError

    def __not__(self):
        try:
            deepCopy = self.deepCopy()
            deepCopy.value = not deepCopy.value
            deepCopy.rectifyDataType()
            return deepCopy
        except: raise TypeError
    
    def __lt__(self, other: Primitive):
        try:
            return Bool(self.value < other.value) # type: ignore
        except: raise TypeError
    
    def __gt__(self, other: Primitive):
        try:
            return Bool(self.value > other.value) # type: ignore
        except: raise TypeError
    
    def __le__(self, other: Primitive):
        try:
            return Bool(self.value <= other.value) # type: ignore
        except: raise TypeError
    
    def __ge__(self, other: Primitive):
        try:
            return Bool(self.value >= other.value) # type: ignore
        except: raise TypeError
    
    def __eq__(self, other: Primitive | None): # type: ignore
        if other == None: return False

        try:
            return Bool(self.value == other.value) # type: ignore
        except: raise TypeError

    def __ne__(self, other: Primitive | None): # type: ignore
        if other == None: return True

        try:
            return Bool(self.value != other.value) # type: ignore
        except: raise TypeError

    def __bool__(self):
        return self.value

    def __getattr__(self, item: str):
        return getattr(self.value, item)

    def __repr__(self) -> str:
        return f'{self.value}'

class String(Primitive):
    dataType = 'String'
    def __init__(self, value: StringNode | str) -> None:
        if isinstance(value, str): super().__init__(value)
        else: super().__init__(value.str)

class Number(Primitive):
    dataType = 'num'
    def __init__(self, value: NumberNode | int | float) -> None:
        if isinstance(value, int) or isinstance(value, float): super().__init__(value)
        else: super().__init__(value.num)

class Bool(Primitive):
    dataType = 'bool'
    def __init__(self, value: BoolNode | bool) -> None:
        if isinstance(value, bool): super().__init__(value)
        else: super().__init__(value.bool)

INBUILTTYPES = ['String', 'num', 'bool']

class InbuiltFunctions:
    printArgs = ['String']
    sumArgs = ['num']
    
    @staticmethod
    def print(*args: object):
        print(*args)
    
    @staticmethod
    def sum(*args: list[Number]):
        SUM = args[0]
        for num in args[1:]:
            SUM += num # type: ignore
        return SUM
    
    @staticmethod
    def inputExpr(out: str = ''):
        expr = input(out)
        return String(expr)

    @staticmethod
    def inputNum(out: str = ''):
        num = float(input(out))
        return Number(num)