from src.model.post import Post
from json import JSONEncoder


class ListOfPost:
    def __init__(self):
        self.posts = []

    def add(self, id, media, date_time, caption):
        self.posts.append(Post(id, media, str(date_time), caption))

    def add(self, post: Post):
        self.posts.append(post)

    def getAll(self):
        return self.posts

    def getSize(self) -> int:
        return len(self.posts)


class ListOfPostEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
