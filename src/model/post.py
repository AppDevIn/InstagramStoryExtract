import pdb


class Media:
    def __init__(self, media, video=False):
        self.media = media
        self.video = video


class Comment:
    def __init__(self, user, comment, time):
        self.user = user
        self.comment = comment
        self.time = time


class Post:
    def __init__(self, id, media: [Media], date_time, caption, likes, comments):
        self.id = id
        self.media: [Media] = media
        self.dateTime = date_time
        self.caption = caption
        self.likes = likes
        self.comments = comments

    def addMedia(self, media):
        for m in media:
            if m.media not in list(map(lambda x: x.media, self.media)):
                self.media.append(m)
