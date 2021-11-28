from src.model.StoryModel import StoryModel


class StoriesModel:
    def __init__(self):
        self.stories = []

    def addStory(self, media, date_time, video=False):
        self.stories.append(StoryModel(media, date_time, video))

    def getStories(self):
        return self.stories

    def getSize(self) -> int:
        return len(self.stories)
