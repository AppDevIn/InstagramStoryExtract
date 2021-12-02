class Post:
    def __init__(self, media, date_time, caption):
        self.media = media
        self.dateTime = date_time
        self.caption = caption


class Media:
    def __init__(self, media, video=False):
        self.media = media
        self.video = video
