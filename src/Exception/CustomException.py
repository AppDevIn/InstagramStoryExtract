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


class NoUserStoryException(Exception):

    def __init__(self, message, default_message=""):
        super(NoUserStoryException, self).__init__()
        self.message = message
        self.default_message = default_message


class LoginException(Exception):

    def __init__(self, message, default_message=""):
        super(LoginException, self).__init__()
        self.message = message
        self.default_message = default_message


class StoryExtractionException(Exception):

    def __init__(self, message, default_message=""):
        super(StoryExtractionException, self).__init__()
        self.message = message
        self.default_message = default_message
