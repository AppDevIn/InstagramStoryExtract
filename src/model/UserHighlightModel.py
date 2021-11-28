from src.model.StoriesModel import StoriesModel


class UserHighlightModel(StoriesModel):
    def __init__(self, name):
        self.stories = []
        self.name = name

    def getHighlightName(self):
        return self.name
