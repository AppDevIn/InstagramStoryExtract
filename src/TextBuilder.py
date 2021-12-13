class TextBuilder:

    def __init__(self, separator="\n"):
        self.separator = separator
        self.text = ""

    def addText(self, text):
        self.text += text + self.separator
        return self

    def build(self) -> str:
        return self.text