class InlineKeyboard(object):

    keyboards = []
    def __init__(self, response):
        super().__init__()
        

        for item in response[0]:
            self.keyboards.append(keyboard(item["text"], item["callback_data"]))
        


class keyboard(object):

    def __init__(self, text, callbackData) -> None:
        super().__init__()
        self.text = text
        self.callbackData = callbackData