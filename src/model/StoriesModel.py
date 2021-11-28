from src.model.StoryModel import StoryModel


class StoriesModel:
    def __init__(self):
        self.stories = []

    def add(self, media, date_time, video=False):
        self.stories.append(StoryModel(media, date_time, video))

    def getAll(self):
        return self.stories

    def getSize(self) -> int:
        return len(self.stories)
