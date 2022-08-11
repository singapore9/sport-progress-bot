import requests

from messages import make_msg, AvailableLanguagesEnum, AvailableMessages
from .base import CommandHandler, URL


class StartCommandHandler(CommandHandler):
    @staticmethod
    def get_command_name():
        return "/start"

    def handle(self):
        requests.post(URL, params={
            "chat_id": self.message_obj.message.chat.id,
            "text": make_msg(
                AvailableMessages.command__start,
                AvailableLanguagesEnum.eng
            )
        })
