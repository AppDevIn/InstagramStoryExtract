from enum import Enum

from telegrambot.Models.callbackMessage import CallbackMessage
from telegrambot.Models.message import Message


class UpdateType(Enum):
    MESSAGE = 0
    CALLBACK = 1

class Update(object):
    _update_id = int()
    _hasCallback = True
    _hasMessage = True

    def __init__(self, response):
        super().__init__()
        self._update_id = int(response["update_id"])

        try:
            self.message = Message(response["message"])
        except:
            self._hasMessage = False

        try:
            self.callback = CallbackMessage(response["callback_query"])
        except KeyError:
            self._hasCallback = False
    
    def getUpdateType(self) -> UpdateType:
        
        if self._hasMessage: 
            return UpdateType.MESSAGE
        elif self._hasCallback: 
            return UpdateType.CALLBACK

    
    def getNextUpdateID(self):
        return self._update_id + 1

    def getMessage(self) -> Message:
        if self._hasMessage: return self.message
        else: raise ValueError

    def getCallback(self) -> Message:
        if self._hasCallback: return self.callback
        else: raise ValueError
    


