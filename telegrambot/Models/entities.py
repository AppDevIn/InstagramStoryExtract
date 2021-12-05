class Entities(object):

    def __init__(self, response) -> None:
        super().__init__()

        self.offset = response["offset"]
        self.length = response["length"]
        self.type =  response["type"]

