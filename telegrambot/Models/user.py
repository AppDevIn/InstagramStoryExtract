class User(object):

    _id = int()
    _is_bot = bool()
    first_name = str()

    def __init__(self, response):
        self._id = response["id"]
        self._is_bot = response["is_bot"]
        self.first_name = response["first_name"]
    
    def getID(self) -> int:
        return self._id
        