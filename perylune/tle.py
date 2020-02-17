
class tle():
    def __init__(self, line1: str, line2: str, line0: str = ""):
        self.setLine1(line1)
        self.setLine2(line2)
        self.name = line0

    def setLine1(self, line: str) -> str:
        # @todo: Add sanity checks for line 1
        self.line1 = line

    def setLine2(self, line: str) -> str:
        # @todo: Add sanity checks for line 2
        self.line2 = line