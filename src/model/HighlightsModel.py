from src.model.UserHighlightModel import UserHighlightModel


class HighlightsModel:

    def __init__(self):
        self.highlights = []

    def add(self, highlight: UserHighlightModel):
        self.highlights.append(highlight)

    def getAll(self):
        return self.highlights

    def getTotalMediaSize(self):
        total = 0
        for h in self.highlights:
            total += h.getSize()

        return total

    def getSize(self):
        return len(self.highlights)
