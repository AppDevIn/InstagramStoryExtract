class InstagramException(Exception):

    def __init__(self, message, default_message):
        super(InstagramException, self).__init__()
        self.message =  message
        self.default_message = default_message
