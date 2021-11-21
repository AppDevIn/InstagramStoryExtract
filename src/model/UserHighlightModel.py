from src.model.HighlightModel import HighlightModel


class UserHighlightModel:
    def __init__(self):
        self.arrOfNames = []
        self.highlight = []

    def appendElements(self, web_elements):
        for element in web_elements:
            name = element.get_attribute("alt")
            if name not in self.arrOfNames:
                img = element.get_attribute("src")
                self.arrOfNames.append(name)
                self.highlight.append(HighlightModel(name, img))

    def getHighlight(self):
        return self.highlight

    def __len__(self):
        return len(self.highlight)
