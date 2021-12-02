from src.model.post import Post


class ListOfPost:
    def __init__(self):
        self.posts = []

    def add(self, media, date_time, caption):
        self.posts.append(Post(media, date_time, caption))

    def getAll(self):
        return self.posts

    def getSize(self) -> int:
        return len(self.posts)
