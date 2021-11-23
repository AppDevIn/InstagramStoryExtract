from src.model.HighlightModel import HighlightModel


class UserHighlightModel:
    def __init__(self):
        self.arrOfNames = []
        self.highlight = []
        self.elements = {}

    def appendElements(self, web_elements):
        for element in web_elements:
            name = element.get_attribute("alt")
            if name not in self.arrOfNames:
                img = element.get_attribute("src")
                self.arrOfNames.append(name)
                self.highlight.append(HighlightModel(name, img))

    def appendWebElement(self, web_elements):
        for element in web_elements:
            name = element.find_element_by_css_selector(".tUtVM img")\
                .get_attribute("alt")
            self.elements[name] = element

    def getHighlight(self):
        return self.highlight

    def __len__(self):
        return len(self.highlight)
