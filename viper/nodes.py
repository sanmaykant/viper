from __future__ import annotations

from position import Position
from tokens import BOOLS, Token

class Node:
    def __init__(self, beginPos: Position, endPos: Position | None = None) -> None:
        self.beginPos = beginPos
        if endPos == None: self.endPos = beginPos
        else: self.endPos = endPos

class NumberNode(Node):
    def __init__(self, num: Token) -> None:
        self.num = int(num.value) if num.value.isdigit() else float(num.value)
        super().__init__(num.beginPos, num.endPos)

    def __repr__(self) -> str:
        return f'{self.num}'

class StringNode(Node):
    def __init__(self, string: Token) -> None:
        self.str = string.value
        super().__init__(string.beginPos, string.endPos)
    
    def __repr__(self) -> str:
        return f"'{self.str}'"

class BoolNode(Node):
    def __init__(self, bool: Token):
        if bool.value in BOOLS[0]:
            self.bool = True
        elif bool.value in BOOLS[1]:
            self.bool = False
        
        super().__init__(bool.beginPos, bool.endPos)
    
    def __repr__(self) -> str:
        return f'{self.bool}'

class IdentifierNode(Node):
    def __init__(self, token: Token, chainedIdentifier: IdentifierNode | None = None) -> None:
        self.identifier = token.value
        self.chainedIdentifier = chainedIdentifier
        super().__init__(token.beginPos, token.endPos)
    
    def __repr__(self) -> str:
        return f"parent: {self.identifier} | chained: {self.chainedIdentifier}"

class AssignNode(Node):
    def __init__(
        self,
        identifier: Token | IdentifierNode,
        value: Node,
        assignOp: Token,
        dataType: Token | None = None,
    ) -> None:
        if isinstance(identifier, Token): self.varName = IdentifierNode(identifier)
        else: self.varName = identifier
        self.value = value
        self.assignOp = assignOp.tokenType
        if dataType is not None:
            self.dataType = dataType
            beginPos = dataType.beginPos
        else:
            self.dataType = None
            beginPos = identifier.beginPos
        super().__init__(beginPos, value.endPos)

    def __repr__(self) -> str:
        return f'<identifier: {self.varName} | value: {self.value} | assignOp: {self.assignOp} | dataType: {self.dataType}>'

class UnaryOpNode(Node):
    def __init__(self, operator: Token, elem: Node):
        self.operator = operator
        self.elem = elem
        super().__init__(operator.beginPos, elem.endPos)
    
    def __repr__(self) -> str:
        return f'{self.operator} {self.elem}'

class BinOpNode(Node):
    def __init__(self, leftElem: Node, operator: Token, rightElem: Node) -> None:
        self.leftElem = leftElem
        self.operator = operator
        self.rightElem = rightElem
        super().__init__(leftElem.beginPos, rightElem.endPos)
    
    def __repr__(self) -> str:
        return f'({self.leftElem} {self.operator} {self.rightElem})'

class CompOpNode(Node):
    def __init__(self, leftElem: Node, operator: Token, rightElem: Node) -> None:
        self.leftElem = leftElem
        self.operator = operator
        self.rightElem = rightElem
        super().__init__(leftElem.beginPos, rightElem.endPos)
    
    def __repr__(self) -> str:
        return f'({self.leftElem} {self.operator} {self.rightElem})'

class IfNode(Node):
    def __init__(self, condition: Node, body: list[Node]):
        self.condition = condition
        self.body = body

    def __repr__(self) -> str:
        return f'{self.condition} | {self.body}'

class ElifNode(Node):
    def __init__(self, ifNodes: list[IfNode] = []) -> None:
        self.ifNodes = ifNodes

    def __repr__(self) -> str:
        return f'{self.ifNodes}'

class  ElseNode(Node):
    def __init__(self, body: list[Node]):
        self.body = body
    
    def __repr__(self) -> str:
        return f'{self.body}'

class IfElseNode(Node):
    def __init__(self, ifNode: IfNode, elifNodes: list[IfNode], elseNode: ElseNode | None = None):
        self.ifNode = ifNode
        self.elifNodes = elifNodes
        self.elseNode = elseNode

    def __repr__(self) -> str:
        return f'<ifNode: {self.ifNode} elifNodes: {self.elifNodes} elseNodes: {self.elseNode}>'

class ForLoopNode(Node):
    def __init__(self, init: AssignNode, condition: Node, reAssign: AssignNode, body: list[Node]):
        self.init = init
        self.condition = condition
        self.reAssign = reAssign
        self.body = body

    def __repr__(self) -> str:
        return f'<init: {self.init} | condition: {self.condition} | reassign: {self.reAssign} | body: {self.body}>'

class FunctionNode(Node):
    dataType = 'func'
    def __init__(self, returnType: Token, funcName: Token, args: list[tuple[IdentifierNode, IdentifierNode]], body: list[Node]):
        self.returnType = returnType
        self.funcName = funcName
        self.args = args
        self.body = body
    
    def __repr__(self) -> str:
        return f'<args: {self.args} body: {self.body}>'

class ReturnNode(Node):
    def __init__(self, returnVal: Node | None = None):
        self.value = returnVal
    
    def __repr__(self) -> str:
        return f'{self.value}'

class CallableNode(Node):
    def __init__(self, callableName: Token | IdentifierNode, params: list[Node], beginPos: Position, endPos: Position):
        if isinstance(callableName, Token): self.callableName = IdentifierNode(callableName)
        else: self.callableName = callableName
        self.params = params
        # self.callableToken = callableName
        super().__init__(beginPos, endPos)
    
    def __repr__(self) -> str:
        return f'<name: {self.callableName} | params: {self.params}>'