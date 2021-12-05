class InstagramException(Exception):

    def __init__(self, message, default_message=""):
        super(InstagramException, self).__init__()
        self.message = message
        self.default_message = default_message


class MissingArgumentException(Exception):

    def __init__(self, message, default_message=""):
        super(MissingArgumentException, self).__init__()
        self.message = message
        self.default_message = default_message
