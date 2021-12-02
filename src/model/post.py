class Post:
    def __init__(self, id, media, date_time, caption):
        self.id = id
        self.media = media
        self.dateTime = date_time
        self.caption = caption


class Media:
    def __init__(self, media, video=False):
        self.media = media
        self.video = video
