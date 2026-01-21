from errors import Error, InvalidAssignmentError, InvalidTypeError, UndefinedNameError
from inbuilt import INBUILTTYPES, Bool, InbuiltFunctions, Primitive, String, Number
from symbolTable import SymbolTable
from nodes import AssignNode, BinOpNode, BoolNode, CallableNode, CompOpNode, ForLoopNode, FunctionNode, IdentifierNode, IfElseNode, Node, NumberNode, ReturnNode, StringNode, UnaryOpNode
from tokens import ArithmeticOp, AssignOp, CompOp, Identifier, LogicalOp

class Interpreter:
    def __init__(self, nodes: list[Node], srcCode: str, symbolTable: SymbolTable = SymbolTable()) -> None:
        self.nodes = nodes
        self.srcCode = srcCode
        self.symbolTable = symbolTable
    
    def traverse(self, trees: list[Node] | None = None):
        if trees == None: trees = self.nodes
        returnVal = None
        for node in trees:
            returnVal = potentialError = self.handleNode(node)
            if isinstance(potentialError, Error): print(potentialError); break
        
        return returnVal

        # print(self.symbolTable)

    def handleNode(self, node: Node):
        handler = 'handle' + node.__class__.__name__
        return getattr(self, handler)(node)

    def handleAssignNode(self, node: AssignNode):
        dataType = node.dataType
        value = self.handleNode(node.value)
        if isinstance(value, Error): return value

        if dataType == None:
            if node.varName.identifier not in self.symbolTable:
                return UndefinedNameError(
                        f"Name {node.varName} is undefined",
                        self.errorLine(node),
                        node.varName.beginPos,
                        node.varName.endPos
                    )

            assignedDataType = self.symbolTable.get(node.varName.identifier)
            if assignedDataType is None: return
            if value.dataType != assignedDataType.dataType:
                return InvalidAssignmentError(
                        f"Type {value.dataType} can't be assigned to declared type {assignedDataType.dataType}",
                        self.errorLine(node),
                        node.beginPos, node.endPos
                    )

            match node:
                case AssignNode(assignOp=AssignOp.EQUAL):
                    self.symbolTable.update(node.varName.identifier, value)
                case AssignNode(assignOp=AssignOp.PLUSEQUAL):
                    currentVal = self.symbolTable.get(node.varName.identifier)
                    self.symbolTable.update(node.varName.identifier, currentVal + value)
                case AssignNode(assignOp=AssignOp.MINUSEQUAL):
                    currentVal = self.symbolTable.get(node.varName.identifier)
                    self.symbolTable.update(node.varName.identifier, currentVal - value)
                case AssignNode(assignOp=AssignOp.STAREQUAL):
                    currentVal = self.symbolTable.get(node.varName.identifier)
                    self.symbolTable.update(node.varName.identifier, currentVal * value)
                case AssignNode(assignOp=AssignOp.STAREQUAL):
                    currentVal = self.symbolTable.get(node.varName.identifier)
                    self.symbolTable.update(node.varName.identifier, currentVal / value)
                case AssignNode(assignOp=AssignOp.DOUBLESTAREQUAL):
                    currentVal = self.symbolTable.get(node.varName.identifier)
                    self.symbolTable.update(node.varName.identifier, currentVal ** value)
                case _:
                    return

            return
        else:
            if dataType.value not in self.symbolTable:
                return UndefinedNameError(
                        f"Type {dataType.value} is not defined",
                        self.errorLine(node),
                        dataType.beginPos,
                        dataType.endPos
                    )

        if value.dataType != dataType.value:
            return InvalidAssignmentError(
                    f"Type {value.dataType} can't be assigned to declared type {dataType.value}",
                    self.errorLine(node),
                    node.beginPos, node.endPos
                )
        
        self.symbolTable.add(node.varName.identifier, Identifier.VARIABLE, value)

    def handleBinOpNode(self, node: BinOpNode):
        leftElem = self.handleNode(node.leftElem)
        if isinstance(leftElem, Error): return leftElem

        rightElem = self.handleNode(node.rightElem)
        if isinstance(rightElem, Error): return rightElem

        try:
            if node.operator.tokenType == ArithmeticOp.PLUS:
                return leftElem + rightElem
            elif node.operator.tokenType == ArithmeticOp.MINUS:
                return leftElem - rightElem
            elif node.operator.tokenType == ArithmeticOp.STAR:
                return leftElem * rightElem
            elif node.operator.tokenType == ArithmeticOp.DOUBLESTAR:
                return leftElem ** rightElem
            elif node.operator.tokenType == ArithmeticOp.SLASH:
                return leftElem / rightElem
            elif node.operator.tokenType == LogicalOp.AND:
                return leftElem and rightElem
            elif node.operator.tokenType == LogicalOp.OR:
                return leftElem or rightElem
        except:
            return InvalidTypeError(
                f"Unsopported operand types for '{node.operator.tokenType.value}': {leftElem.dataType} and {rightElem.dataType}",
                self.errorLine(node),
                node.beginPos,
                node.endPos
            )
    
    def handleUnaryOpNode(self, node: UnaryOpNode):
        elem = self.handleNode(node.elem)
        if isinstance(elem, Error): return elem

        try:
            if node.operator.tokenType == LogicalOp.NOT:
                return elem.__not__()
            elif node.operator.tokenType == ArithmeticOp.MINUS:
                return -elem
        except:
            return InvalidTypeError(
                f"Unsupported operand type for '{node.operator.value}': {elem.dataType}",
                self.errorLine(node),
                node.beginPos,
                node.endPos
            )

    def handleCompOpNode(self, node: CompOpNode):
        leftElem = self.handleNode(node.leftElem)
        if isinstance(leftElem, Error): return leftElem

        rightElem = self.handleNode(node.rightElem)
        if isinstance(rightElem, Error): return rightElem

        try:
            if node.operator.tokenType == CompOp.LESS:
                return leftElem < rightElem
            elif node.operator.tokenType == CompOp.GREATER:
                return leftElem > rightElem
            elif node.operator.tokenType == CompOp.LESSEQUAL:
                return leftElem <= rightElem
            elif node.operator.tokenType == CompOp.GREATEREQUAL:
                return leftElem >= rightElem
            elif node.operator.tokenType == CompOp.EQEQUAL:
                return leftElem == rightElem
            elif node.operator.tokenType == CompOp.NOTEQUAL:
                return leftElem != rightElem
        except:
            return InvalidTypeError(
                f"Unsopported operand types for '{node.operator.tokenType.value}': {leftElem.dataType} and {rightElem.dataType}",
                self.errorLine(node),
                node.beginPos,
                node.endPos
            )
    
    def handleIfElseNode(self, node: IfElseNode):
        condition = self.handleNode(node.ifNode.condition)
        if isinstance(condition, Error): return Error

        if condition:
            potentialReturnVal = self.traverse(node.ifNode.body)
            if potentialReturnVal != None: return potentialReturnVal
        else:
            for elifNode in node.elifNodes:
                condition = self.handleNode(elifNode.condition)
                if isinstance(condition, Error): return condition

                if condition:
                    potentialReturnVal = self.traverse(elifNode.body)
                    if potentialReturnVal != None: return potentialReturnVal

        if not condition:
            if node.elseNode != None:
                potentialReturnVal = self.traverse(node.elseNode.body)
                if potentialReturnVal != None: return potentialReturnVal

    def handleFunctionNode(self, node: FunctionNode):
        for dataType, _ in node.args:
            if dataType.identifier in self.symbolTable: pass
            else: return UndefinedNameError(
                f"Name '{dataType.identifier}' is undefined",
                self.errorLine(dataType),
                dataType.beginPos, dataType.endPos
            )
        self.symbolTable.add(node.funcName.value, Identifier.FUNCDEF, node)

    def handleCallableNode(self, node: CallableNode):
        if node.callableName.identifier not in self.symbolTable: # type: ignore
            return UndefinedNameError(f"Name '{node.callableName}' is undefined", self.errorLine(node), node.beginPos, node.callableName.endPos)

        func = self.symbolTable.get(node.callableName.identifier)
        if func == None:
            try:
                # TODO properly declare args and remove type: ignore on args.append()
                args: list[Primitive] = []

                for param in node.params:
                    arg = self.handleNode(param)
                    if isinstance(arg, Error): return arg
                    args.append(arg)
                return getattr(InbuiltFunctions, node.callableName.identifier)(*args)
            except Exception as e:
                return Error('Error', f'{e}', self.errorLine(node), node.beginPos, node.endPos)
        elif func.dataType in INBUILTTYPES and not isinstance(func, FunctionNode):
            if node.callableName.chainedIdentifier != None:
                return func.deepCopy(getattr(func, node.callableName.chainedIdentifier.identifier)())
            return InvalidTypeError(f"Type {func.dataType} is not callable", self.errorLine(node), node.beginPos, node.endPos)
        elif not isinstance(func, FunctionNode):
            return InvalidTypeError(f"Type {func.dataType} is not callable", self.errorLine(node), node.beginPos, node.endPos) # type: ignore

        symbols = {}

        for param, (expectedType, varName) in zip(node.params, func.args):
            arg = self.handleNode(param)
            if isinstance(arg, Error): return arg

            if arg.dataType != expectedType.identifier:
                return InvalidAssignmentError(
                        f"Type {arg.dataType} can't be assigned to parameter of type {expectedType}",
                        self.errorLine(param),
                        param.beginPos, param.endPos
                    )

            symbols[varName.identifier] = (Identifier.VARIABLE, arg)

        functionInterpreter = Interpreter(func.body, self.srcCode, SymbolTable(symbols, self.symbolTable))
        return functionInterpreter.traverse()

    def handleForLoopNode(self, node: ForLoopNode):
        self.handleAssignNode(node.init)

        while True:
            conditionNode = self.handleNode(node.condition)

            if conditionNode:
                potentialReturnVal = self.traverse(node.body)
                if potentialReturnVal != None: return potentialReturnVal
                self.handleAssignNode(node.reAssign)
            else: break

    def handleStringNode(self, node: StringNode):
        return String(node)

    def handleNumberNode(self, node: NumberNode):
        return Number(node)
    
    def handleBoolNode(self, node: BoolNode):
        return Bool(node)

    def handleIdentifierNode(self, node: IdentifierNode):
        try: return self.symbolTable.get(node.identifier)
        except: return UndefinedNameError(f"Name {node.identifier} is undefined", self.errorLine(node), node.beginPos, node.endPos)

    def handleReturnNode(self, node: ReturnNode):
        if node.value != None:
            returnVal = self.handleNode(node.value)
            return returnVal

    def errorLine(self, node: Node):
        beginPos = node.beginPos.idx - node.beginPos.columnNo
        try: endPos = node.beginPos.idx + self.srcCode[node.beginPos.idx:].index('\n')
        except: return self.srcCode[beginPos:]
        return self.srcCode[beginPos : endPos]
