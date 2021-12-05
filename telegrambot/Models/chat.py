class Chat(object):
    
    _id = int()
    _type = str()
    _first_name = str()
    _title = str()

    def __init__(self, response):
        super().__init__()
        self._id = response["id"]
        self._type = response["type"]

        if self._type == "private":
            self._first_name = response["first_name"]
        else:
            self._title = response["title"]

    def getID(self) -> int:
        return self._id
    