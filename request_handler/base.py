import requests

from constants import TELEGRAM_TOKEN
from logger import logging
from messages import make_msg, AvailableLanguagesEnum, AvailableMessages
from model import UserMessage

# Link for configuring DETA + Telegram webhook
# https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={SERVER_URL}

base_url = "https://api.telegram.org/bot"

URL = f"{base_url}{TELEGRAM_TOKEN}/sendMessage"


class RequestHandler:
    def __init__(self, message_obj: UserMessage):
        self.message_obj = message_obj

    def handle(self):
        raise NotImplementedError(f'Request should be handled by bot')


class CommandHandler(RequestHandler):
    @staticmethod
    def get_command_name():
        raise NotImplementedError('Command should have own name')

    def handle(self):
        raise NotImplementedError(f'Command handler for {self.get_command_name()} should exist')


class UnknownTextHandler(RequestHandler):
    def handle(self):
        logging.error(f'logs -> {self.message_obj}')
        requests.post(URL, params={
            "chat_id": self.message_obj.message.chat.id,
            "text": make_msg(
                AvailableMessages.unknown_command,
                AvailableLanguagesEnum.eng
            )
        })
