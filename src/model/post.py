class Post:
    def __init__(self, id, media, date_time, caption, likes, comments):
        self.id = id
        self.media = media
        self.dateTime = date_time
        self.caption = caption
        self.likes = likes
        self.comments = comments


class Media:
    def __init__(self, media, video=False):
        self.media = media
        self.video = video


class Comment:
    def __init__(self, user, comment, time):
        self.user = user
        self.comment = comment
        self.time = time
