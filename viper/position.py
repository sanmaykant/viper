from __future__ import annotations

class Position:
    def __init__(self, idx: int = 0, lineNo: int = 0, columnNo: int = 0) -> None:
        self.idx: int = idx
        self.lineNo: int = lineNo
        self.columnNo: int = columnNo

    def advance(self, currentChar: str | None = None):
        self.columnNo += 1
        self.idx += 1
        if currentChar == "\n":
            self.lineNo += 1
            self.columnNo = 0

        return self

    def revert(self) -> None:
        self.idx -= 1
        self.columnNo -= 1
        if self.columnNo < 0:
            self.lineNo -= 1
            self.columnNo = 0
    
    def __repr__(self) -> str:
        return f'lineNo: {self.lineNo}, columnNo: {self.columnNo}'

    @property
    def lineNoInFile(self) -> int:
        return self.lineNo + 1

    @property
    def columnNoInFile(self) -> int:
        return self.columnNo + 1
    
    def copy(self) -> Position:
        return Position(self.idx, self.lineNo, self.columnNo)