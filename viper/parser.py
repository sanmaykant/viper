from types import MethodType
from errors import Error, InvalidSyntaxError, MissingTokenError, UnexpectedTokenError
from nodes import AssignNode, BinOpNode, BoolNode, CallableNode, CompOpNode, ElseNode, ForLoopNode, FunctionNode, IdentifierNode, IfElseNode, IfNode, Node, NumberNode, ReturnNode, StringNode, UnaryOpNode
from position import Position
from tokens import ArithmeticOp, CompOp, Keyword, Literal, LogicalOp, Punctuator, Separator, Token, TokenFamily

class Parser:
    def __init__(self, tokens: list[Token], srcCode: str) -> None:
        self.tokens = tokens
        self.srcCode = srcCode.split('\n')
        self.idx = 0
        self.currentTok = self.tokens[self.idx] if len(self.tokens) > self.idx else self.tokens[-1]
    
    def advance(self, n: int = 1):
        self.idx += n
        self.currentTok = self.tokens[self.idx] if len(self.tokens) > self.idx else self.tokens[-1]
        return self.currentTok
    
    def revert(self, n: int = 1):
        self.idx -= n
        self.currentTok = self.tokens[self.idx] if len(self.tokens) > self.idx else self.tokens[-1]
        return self.currentTok

    def parse(self, n: int | None = None):
        stmts: list[Node] = []
        if n != None:
            for _ in range(n):
                node = self.buildNodes()
                if isinstance(node, Error): return node
                stmts += node

        else:
            while self.currentTok.tokenType != Punctuator.EOF:
                node = self.buildNodes()
                if isinstance(node, Error): return node
                stmts += node
        
        return stmts
    
    def buildNodes(self) -> list[Node] | Error:
        nodes: list[Node] | Error = []
        builders: list[MethodType] = [self.ifElseNode, self.functionNode, self.returnNode, self.forLoopNode, self.callableNode, self.assignmentNode, self.reassignmentNode] # type: ignore

        for builder in builders:
            node = self.buildNodeFromNodeBuilder(builder, nodes)
            if isinstance(node, Error): return node
            if node != None: return node

        if self.currentTok.tokenType == Separator.RBRACE:
            self.advance()
            return nodes

        return UnexpectedTokenError(f"'{self.currentTok.value}'", self.errorLine(self.currentTok.beginPos), self.currentTok.beginPos, self.currentTok.endPos)

    def buildNodeFromNodeBuilder(self, nodeBuilder: MethodType, nodes: list[Node]):
        node = nodeBuilder()
        if isinstance(node, Error): return node
        if node != None:
            nodes.append(node)
            if self.currentTok.tokenType == Punctuator.SEMI:
                self.advance()
                node = self.buildNodes()
                if isinstance(node, Error): return node
                nodes += node
            return nodes        

    # def assignmentNode(self):
    #     currentToken = self.currentTok
    #     firstNextToken = self.advance()
    #     secondNextToken = self.advance()
    #     self.revert(2)

    #     dataType: Token | None = None
    #     if currentToken.familyType == TokenFamily.IDENTIFIER and firstNextToken.familyType == TokenFamily.IDENTIFIER and secondNextToken.familyType == TokenFamily.ASSIGNOP:
    #         dataType = self.currentTok
    #         self.advance()
    #     elif currentToken.familyType == TokenFamily.IDENTIFIER and firstNextToken.familyType == TokenFamily.ASSIGNOP:
    #         dataType = None
    #     elif currentToken.familyType == TokenFamily.LITERAL:
    #         return InvalidSyntaxError("Invalid identifier: Literal", self.errorLine(currentToken.beginPos), currentToken.beginPos, currentToken.endPos)
    #     elif firstNextToken.familyType == TokenFamily.LITERAL:
    #         return InvalidSyntaxError("Invalid identifier: Literal", self.errorLine(firstNextToken.beginPos), firstNextToken.beginPos, firstNextToken.endPos)
    #     else: return

    #     identifier = self.currentTok
    #     assignOp = self.advance()
    #     self.advance()
    #     value = self.logicalExpr()
    #     if isinstance(value, Error): return value

    #     return AssignNode(identifier, value, assignOp, dataType)

    def assignmentNode(self):
        dataType = self.currentTok
        varName = self.advance()
        assignOp = self.advance()

        if not(dataType.familyType == TokenFamily.IDENTIFIER and varName.familyType == TokenFamily.IDENTIFIER and assignOp.familyType == TokenFamily.ASSIGNOP):
            self.revert(2)
            return

        if self.advance().familyType == TokenFamily.KEYWORD:
            return InvalidSyntaxError(f'Expected {dataType.value}', self.errorLine(self.currentTok.beginPos), assignOp.beginPos.advance())
        value = self.logicalExpr()
        if isinstance(value, Error): return value

        return AssignNode(varName, value, assignOp, dataType)
    
    def reassignmentNode(self):
        beginIdx = self.idx
        varName = self.dotChain()
        if varName == None: return varName
        assignOp = self.currentTok
        endIdx = self.idx

        if not(assignOp.familyType == TokenFamily.ASSIGNOP):
            self.revert(endIdx - beginIdx)
            return
        
        if self.advance().familyType == TokenFamily.KEYWORD:
            # TODO come up with a better error msg if possible
            return InvalidSyntaxError(f'', self.errorLine(self.currentTok.beginPos), assignOp.beginPos.advance())
        value = self.logicalExpr()
        if isinstance(value, Error): return value

        return AssignNode(varName, value, assignOp)

    def ifElseNode(self):
        if self.currentTok.tokenType != Keyword.IF:
            return

        self.advance()

        ifCondition = self.logicalExpr()
        if isinstance(ifCondition, Error): return ifCondition
        ifBody = self.body()
        if isinstance(ifBody, Error): return ifBody

        ifNode = IfNode(ifCondition, ifBody)

        elifNodes: list[IfNode] = []
        while self.currentTok.tokenType == Keyword.ELIF: # type: ignore
            self.advance()
            elifCondition = self.logicalExpr()
            if isinstance(elifCondition, Error): return elifCondition
            elifBody = self.body()
            if isinstance(elifBody, Error): return elifBody

            ifNode = IfNode(elifCondition, elifBody)
            elifNodes.append(ifNode)

        elseNode: ElseNode | None = None
        if self.currentTok.tokenType == Keyword.ELSE: # type: ignore
            self.advance()
            elseBody = self.body()
            if isinstance(elseBody, Error): return elseBody
            elseNode = ElseNode(elseBody)
        
        ifElseNode = IfElseNode(ifNode, elifNodes, elseNode)

        return ifElseNode

    def functionNode(self):
        currentToken = self.currentTok
        firstNextToken = self.advance()
        secondNextToken = self.advance()
        self.revert(2)

        if not (currentToken.familyType == TokenFamily.IDENTIFIER and firstNextToken.familyType == TokenFamily.IDENTIFIER and secondNextToken.tokenType == Separator.LPAR):
            return
        
        returnType = self.currentTok
        funcName = self.advance()
        self.advance()
        formalParameters = self.formalParameters()
        if isinstance(formalParameters, Error): return formalParameters
        body = self.body()
        if isinstance(body, Error): return body

        return FunctionNode(returnType, funcName, formalParameters, body)
    
    def returnNode(self):
        if not self.currentTok.tokenType == Keyword.RETURN:
            return

        self.advance()
        returnVal = None
        if self.currentTok.familyType == TokenFamily.IDENTIFIER or self.currentTok.familyType == TokenFamily.LITERAL:
            returnVal = self.logicalExpr()
            if isinstance(returnVal, Error): return returnVal
        return ReturnNode(returnVal)
    
    def forLoopNode(self):
        if self.currentTok.tokenType != Keyword.FOR: return

        self.advance(2)
        assignOp = self.assignmentNode()
        if assignOp == None:
            return InvalidSyntaxError('Expected assignment operation', self.errorLine(self.currentTok.beginPos), self.currentTok.beginPos)
        if isinstance(assignOp, Error): return assignOp

        if self.currentTok.tokenType == Punctuator.SEMI: self.advance()

        condition = self.logicalExpr()
        if isinstance(condition, Error): return condition

        if self.currentTok.tokenType == Punctuator.SEMI: self.advance()

        reAssignOp = self.assignmentNode()
        if reAssignOp == None:
            return InvalidSyntaxError('Expected reassignment operation', self.errorLine(self.currentTok.beginPos), self.currentTok.beginPos)
        if isinstance(reAssignOp, Error): return reAssignOp
        self.advance()

        body = self.body()
        if isinstance(body, Error): return body

        return ForLoopNode(assignOp, condition, reAssignOp, body)

    def callableNode(self):
        beginIdx = self.idx
        callableName = self.dotChain()
        if callableName == None: return
        nextToken = self.currentTok
        endIdx = self.idx

        if not (nextToken.tokenType == Separator.LPAR):
            self.revert(endIdx - beginIdx)
            return

        identifier = callableName
        actualParams = self.actualParameters()
        if isinstance(actualParams, Error): return actualParams

        return CallableNode(identifier, actualParams[0], identifier.beginPos, actualParams[1])

    def formalParameters(self):
        self.advance()

        formalParameters: list[tuple[IdentifierNode, IdentifierNode]] = []
        while self.currentTok.tokenType != Separator.RPAR:
            datatype = self.currentTok
            if datatype.tokenType == Punctuator.EOF: return MissingTokenError('MissingParanError', "')'", self.errorLine(datatype.beginPos), datatype.beginPos)

            identifier = self.advance()

            if datatype.familyType != TokenFamily.IDENTIFIER:
                return InvalidSyntaxError(f'Invalid identifier: {datatype.familyType.name.title()}', self.errorLine(datatype.beginPos), datatype.beginPos, datatype.endPos)
            if identifier.familyType != TokenFamily.IDENTIFIER:
                return InvalidSyntaxError(f'Invalid identifier: {identifier.familyType.name.title()}', self.errorLine(identifier.beginPos), identifier.beginPos, identifier.endPos)

            datatype = IdentifierNode(datatype)
            identifier = IdentifierNode(identifier)

            formalParameters.append((datatype, identifier))
            self.advance()
            if self.currentTok.tokenType == Separator.COMMA: self.advance()

        self.advance()
        return formalParameters
    
    def actualParameters(self) -> Error | tuple[list[Node], Position]:
        self.advance()

        actualParameters: list[Node] = []
        while self.currentTok.tokenType != Separator.RPAR:
            if self.currentTok.tokenType == Punctuator.EOF: return MissingTokenError('MissingParanError', "')'", self.errorLine(self.currentTok.beginPos), self.currentTok.beginPos)
            param = self.callableNode()
            if param == None: param = self.logicalExpr()
            if isinstance(param, Error): return param
            actualParameters.append(param)
            if self.currentTok.tokenType == Separator.COMMA: self.advance()

        endPos = self.currentTok.endPos
        self.advance()
        return actualParameters, endPos

    def term(self) -> Node | Error:
        if self.currentTok.familyType == TokenFamily.LITERAL:
            literal: Node
            if self.currentTok.tokenType == Literal.NUM:
                literal = NumberNode(self.currentTok)
                self.advance()
                return literal
            if self.currentTok.tokenType == Literal.STRING:
                literal = StringNode(self.currentTok)
                self.advance()
                return literal
            if self.currentTok.tokenType == Literal.BOOL:
                literal = BoolNode(self.currentTok)
                self.advance()
                return literal

        if self.currentTok.tokenType == ArithmeticOp.MINUS:
            operator = self.currentTok
            self.advance()
            elem = self.term()
            if isinstance(elem, Error): return elem
            return UnaryOpNode(operator, elem)

        if self.currentTok.tokenType == LogicalOp.NOT:
            operator = self.currentTok
            self.advance()
            elem = self.term()
            if isinstance(elem, Error): return elem
            return UnaryOpNode(operator, elem)

        if self.currentTok.tokenType == Separator.LPAR:
            self.advance()
            expr = self.logicalExpr()
            if self.currentTok.tokenType != Separator.RPAR: return MissingTokenError('MissingParanError', "')'", self.errorLine(expr.beginPos), self.currentTok.beginPos) # type: ignore
            self.advance()
            return expr

        if self.currentTok.familyType == TokenFamily.IDENTIFIER:
            identifier = self.callableNode()
            if isinstance(identifier, Error): return identifier
            if identifier == None:
                identifier = self.dotChain()
                if identifier != None:
                    return identifier
                else:
                    identifier = self.currentTok
                    self.advance()
                    return IdentifierNode(identifier)
            return identifier
        return NumberNode(self.tokens[-1])

    def factor(self):
        leftTerm = self.term()
        if isinstance(leftTerm, Error): return leftTerm

        if self.currentTok.tokenType in (ArithmeticOp.STAR, ArithmeticOp.SLASH, ArithmeticOp.DOUBLESTAR):
            operator = self.currentTok
            self.advance()
            rightTerm: BinOpNode | NumberNode = self.factor()
            return BinOpNode(leftTerm, operator, rightTerm)

        return leftTerm
    
    def mathExpr(self):
        leftFactor = self.factor()
        if isinstance(leftFactor, Error): return leftFactor

        if self.currentTok.tokenType in (ArithmeticOp.PLUS, ArithmeticOp.MINUS):
            operator = self.currentTok
            self.advance()
            rightFactor: BinOpNode | NumberNode = self.mathExpr()
            return BinOpNode(leftFactor, operator, rightFactor)

        return leftFactor

    def compExpr(self):
        leftExpr = self.mathExpr()
        if isinstance(leftExpr, Error): return leftExpr

        if self.currentTok.tokenType in CompOp:
            operator = self.currentTok
            self.advance()
            rightExpr: Node | Error = self.compExpr()
            if isinstance(rightExpr, Error): return rightExpr
            return CompOpNode(leftExpr, operator, rightExpr)

        return leftExpr

    def logicalExpr(self):
        leftExpr = self.compExpr()
        if isinstance(leftExpr, Error): return leftExpr

        if self.currentTok.tokenType in (LogicalOp.AND, LogicalOp.OR):
            operator = self.currentTok
            self.advance()
            rightExpr: Node | Error = self.logicalExpr()
            if isinstance(rightExpr, Error): return rightExpr
            return BinOpNode(leftExpr, operator, rightExpr)

        return leftExpr
    
    def dotChain(self):
        chainMembers: list[Token] = []

        while True:
            if self.currentTok.familyType == TokenFamily.IDENTIFIER:
                chainMembers.append(self.currentTok)
                if self.advance().tokenType == Punctuator.DOT: self.advance(); continue
                else: break
            else: break
        if len(chainMembers) == 0: return

        def buildChain(i: int = 0) -> IdentifierNode | None:
            try: return IdentifierNode(chainMembers[i], buildChain(i + 1))
            except: return

        return buildChain()

    def body(self) -> Error | list[Node]:
        if self.currentTok.tokenType != Separator.LBRACE:
            nodes = self.buildNodes()
            if isinstance(nodes, Error): return nodes
            body = nodes
            return body
        elif self.currentTok.tokenType == Separator.LBRACE:
            bodyBegin = self.idx
            lBraceCount = 0
            rBraceCount = 0
            while True:
                if self.currentTok.tokenType == Separator.LBRACE:
                    lBraceCount += 1
                elif self.currentTok.tokenType == Separator.RBRACE: # type: ignore
                    rBraceCount += 1
                elif self.currentTok.tokenType == Punctuator.EOF: # type: ignore
                    bodyEnd = self.idx
                    MISSINGPARANOFFSET = 1
                    self.revert(bodyEnd - bodyBegin - MISSINGPARANOFFSET)
                    return MissingTokenError('MissingBraceError', "'}'", self.errorLine(self.currentTok.beginPos), self.currentTok.beginPos)
                if lBraceCount == rBraceCount: break
                self.advance()
            bodyEnd = self.idx
            self.revert(bodyEnd - bodyBegin)

            self.advance()
            body: list[Node] = []

            while bodyEnd > self.idx:
                nodes = self.buildNodes()
                if isinstance(nodes, Error): return nodes
                body += nodes

            self.advance()
            return body
        return self.parse()
        

    def errorLine(self, pos: Position):
        return self.srcCode[pos.lineNo]