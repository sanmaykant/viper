from position import Position

class Error:
    def __init__(
        self,
        errorName: str,
        details: str,
        errorLine: str,
        beginPos: Position,
        endPos: Position | None = None
    ) -> None:
        self.errorName = errorName
        self.details = details
        self.errorLine = errorLine
        self.beginPos = beginPos
        if endPos == None: self.endPos = beginPos
        else: self.endPos = endPos
    
    def __repr__(self) -> str:
        errorDetails: str = f"{self.errorName}: {self.details} | column {self.beginPos.columnNoInFile} line {self.beginPos.lineNoInFile}"

        if '\n' in self.errorLine:
            return errorDetails + '\n\n' + self.errorLine
        elif self.beginPos is self.endPos:
            errorPosition = f'{self.errorLine}\n' + ' '*self.beginPos.columnNo + '^'
        else:
            errorPosition: str = f'{self.errorLine}\n' + ' '*self.beginPos.columnNo + '^'*(self.endPos.columnNo + 1 - self.beginPos.columnNo)

        error: str = errorDetails + '\n\n' + errorPosition
        return error
    
    def setEndPos(self, endPos: Position) -> None:
        self.endPos = endPos

class InvalidLiteralError(Error):
    def __init__(self, details: str, errorLine: str, beginPos: Position, endPos: Position | None = None) -> None:
        super().__init__('InvalidLiteralError', details, errorLine, beginPos, endPos)

class InvalidCharError(Error):
    def __init__(self, details: str, errorLine: str, beginPos: Position, endPos: Position | None = None) -> None:
        super().__init__('InvalidCharError', details, errorLine, beginPos, endPos)

class MissingTokenError(Error):
    def __init__(self, errorName: str, details: str, errorLine: str, beginPos: Position, endPos: Position | None = None) -> None:
        super().__init__(errorName, details, errorLine, beginPos, endPos)

class MissingExprError(Error):
    def __init__(self, details: str, errorLine: str, beginPos: Position, endPos: Position | None = None) -> None:
        super().__init__('MissingExprError', details, errorLine, beginPos, endPos)

class UnexpectedTokenError(Error):
    def __init__(self, details: str, errorLine: str, beginPos: Position, endPos: Position | None = None) -> None:
        super().__init__('UnexpectedTokenError', details, errorLine, beginPos, endPos)

class InvalidSyntaxError(Error):
    def __init__(self, details: str, errorLine: str, beginPos: Position, endPos: Position | None = None) -> None:
        super().__init__('InvalidSyntaxError', details, errorLine, beginPos, endPos)

class InvalidAssignmentError(Error):
    def __init__(self, details: str, errorLine: str, beginPos: Position, endPos: Position | None = None) -> None:
        super().__init__('IvalidAssignmentError', details, errorLine, beginPos, endPos)

class InvalidTypeError(Error):
    def __init__(self, details: str, errorLine: str, beginPos: Position, endPos: Position | None = None) -> None:
        super().__init__('InvalidTypeError', details, errorLine, beginPos, endPos)

class UndefinedNameError(Error):
    def __init__(self, details: str, errorLine: str, beginPos: Position, endPos: Position | None = None) -> None:
        super().__init__('UndefinedNameError', details, errorLine, beginPos, endPos)