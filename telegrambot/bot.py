from typing import List
import requests
import json
import configparser as cfg
from telegrambot.Models.update import Update, UpdateType
import telegram


class TeleBot:
    _commands = {}
    _callback = {}

    def __init__(self, token):
        self.base = f"https://api.telegram.org/bot{token}/"

    def run(self):
        lastUpdate = None
        while True:
            print("...")

            if lastUpdate == None:
                updates = self.get_updates(offset=-1)
            else:
                updates = self.get_updates(offset=lastUpdate.getNextUpdateID())

            if updates:
                for item in updates:
                    lastUpdate = item

                    if item.getUpdateType() == UpdateType.MESSAGE and item.message.entityType():
                        command = item.message.text[item.message.entities[0].offset:item.message.entities[0].length]
                        print(command)
                        if self._commands.get(command): self._commands.get(command)(item)
                    elif item.getUpdateType() == UpdateType.CALLBACK:
                        callback = item.callback.message.replyMarkup.keyboards[0].callbackData.split("@")[1]
                        self._callback.get(callback)(item)

    def add_command(self, commnad, func):
        self._commands[commnad] = func

    def add_callback(self, callbackData, func):
        self._callback[callbackData] = func

    def get_updates(self, offset=None) -> List[Update]:
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + f"&offset={str(offset)}"
        response = requests.request("GET", url, headers={}, data={})
        response = json.loads(response.content)["result"]

        updates = []
        if response:
            for item in response:
                updates.append(Update(response=item))
        return updates

    def send_message(self, chat_id, text):
        url = self.base + f"sendMessage?chat_id={chat_id}&text={text}"
        requests.request("POST", url, headers={}, data={})

    def send_callback(self, chat_id, text, replyMarkUp):
        url = self.base + f"sendMessage?chat_id={chat_id}&text={text}&reply_markup={replyMarkUp}"
        requests.request("POST", url, headers={}, data={})

    def read_token_from_config(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get("creds", "token")

    def send_photo(self, chat_id, file):
        up = {'photo': ("i.png", open(file, 'rb'), "multipart/form-data")}
        url = self.base + f"sendPhoto"
        requests.post(url, files=up, data={
            "chat_id": chat_id,
        })
