from errors import Error, InvalidLiteralError
from position import Position
from tokens import DIGITS, KEYWORDS, LETTERS, BOOLS, OPERATORFIRSTCHAR, OPERATORS, PUNCTUATORS, SEPARATORS, ArithmeticOp, AssignOp, CompOp, Keyword, Literal, LogicalOp, Punctuator, Token, TokenFamily

class Lexer:
    def __init__(self, src: str) -> None:
        self.position = Position()
        self.srcCode = src
        self.currentChar = self.srcCode[self.position.idx] if len(self.srcCode) > self.position.idx else None

    def advance(self, currentChar: str | None = None) -> None:
        self.position.advance(currentChar if currentChar != None else self.currentChar)
        self.currentChar = self.srcCode[self.position.idx] if len(self.srcCode) > self.position.idx else None

    def yieldTokens(self) -> list[Token] | Error:
        tokens: list[Token] = []

        while self.currentChar != None:
            if self.currentChar in ' \n\t':
                self.advance()
                continue
            if self.currentChar in DIGITS:
                result: Token | InvalidLiteralError = self.makeNumber()
                if isinstance(result, Error): return result
                tokens.append(result)
                continue
            if self.currentChar in ('\'', '"'):
                tokens.append(self.makeStr(self.currentChar))
                continue
            if self.currentChar in LETTERS:
                tokens.append(self.makeKeyIdLit())
                continue
            if self.currentChar in OPERATORS or self.currentChar in OPERATORFIRSTCHAR:
                op = self.currentChar
                beginPos = self.position.copy()
                self.advance()

                tokenFamily: TokenFamily
                tokenType: ArithmeticOp | CompOp | AssignOp | LogicalOp | None

                potentialOp = op + self.currentChar
                if potentialOp in OPERATORS:
                    endPos = self.position.copy()
                    self.advance()
                    tokenType = OPERATORS[potentialOp]
                    tokenFamily = TokenFamily.getTokenFamily(tokenType)
                    tokens.append(Token(tokenFamily, tokenType, potentialOp, beginPos, endPos))
                    continue

                tokenType = OPERATORS[op]
                tokenFamily = TokenFamily.getTokenFamily(tokenType)
                tokens.append(Token(tokenFamily, tokenType, op, beginPos))
                continue
            if self.currentChar in PUNCTUATORS:
                tokens.append(Token(TokenFamily.PUNCTUATOR, PUNCTUATORS[self.currentChar], self.currentChar, self.position.copy()))
                self.advance()
            if self.currentChar in SEPARATORS:
                tokens.append(Token(TokenFamily.PUNCTUATOR, SEPARATORS[self.currentChar], self.currentChar, self.position.copy()))
                self.advance()

        tokens.append(Token(TokenFamily.PUNCTUATOR, Punctuator.EOF, 'EOF', self.position.copy()))
        return tokens

    def makeNumber(self) -> Token | InvalidLiteralError:
        numStr: str = ''
        dotCount: int = 0

        beginPos = self.position.copy()

        error: InvalidLiteralError | type[InvalidLiteralError] | None = None
        while self.currentChar in DIGITS + ['.']:
            if self.currentChar == '.':
                if dotCount == 1:
                    error = InvalidLiteralError
                dotCount += 1
                numStr += self.currentChar
            else:
                numStr += self.currentChar
            self.advance()

        if error:
            endPos = self.position.copy()
            endPos.revert()
            error = error(numStr, self.errorLine(beginPos.lineNo), beginPos, endPos)
            return error

        endPos: Position = self.position.copy()
        endPos.revert()

        token = Token(TokenFamily.LITERAL, Literal.NUM, numStr, beginPos, endPos)
        return token
    
    def makeStr(self, punctuator: str) -> Token:
        strStr: str = ''
        beginPos = self.position.copy()

        self.advance()
        while self.currentChar != punctuator and self.currentChar != None:
            strStr += self.currentChar
            self.advance()
        self.advance()

        endPos = self.position.copy()
        endPos.revert()
        
        tokenFamily = TokenFamily.LITERAL
        tokenType = Literal.STRING

        return Token(tokenFamily, tokenType, strStr, beginPos, endPos)

    def makeKeyIdLit(self) -> Token:
        idStr: str = ''
        beginPos = self.position.copy()

        while self.currentChar in LETTERS + DIGITS + ['_']:
            idStr += self.currentChar
            self.advance()

        endPos: Position = self.position.copy()
        endPos.revert()

        tokenType: Keyword | Literal | ArithmeticOp | CompOp | AssignOp | LogicalOp | TokenFamily | None
        if idStr in BOOLS[0] or idStr in BOOLS[1]:
            tokenFamily = TokenFamily.LITERAL
            tokenType = Literal.BOOL
        elif idStr in KEYWORDS:
            tokenFamily = TokenFamily.KEYWORD
            tokenType = KEYWORDS[idStr]
        elif idStr in OPERATORS:
            tokenType = OPERATORS[idStr]
            tokenFamily = TokenFamily.getTokenFamily(tokenType)
        else:
            tokenFamily = TokenFamily.IDENTIFIER
            tokenType = TokenFamily.IDENTIFIER

        return Token(tokenFamily, tokenType, idStr, beginPos, endPos)
    
    def errorLine(self, lineNo: int) -> str:
        return self.srcCode.split('\n')[lineNo]
