class PageTable:

    def __init__(self):
        self._dictPageFrame = {}

    def addPF(self, page, frame):
        self._dictPageFrame[page] = frame

    def getFrame(self, page):
        return self._dictPageFrame[page]

    def getFrames(self):
        return self._dictPageFrame.values()

    def getPages(self):
        return self._dictPageFrame.keys()