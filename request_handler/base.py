import requests
from typing import List, Any

from constants import TELEGRAM_TOKEN
from logger import logging
from messages import make_msg, AvailableMessages
from model import UserMessage
from server_api import get_user_language

# Link for configuring DETA + Telegram webhook
# https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={SERVER_URL}

base_url = "https://api.telegram.org/bot"

URL = f"{base_url}{TELEGRAM_TOKEN}/sendMessage"


class RequestHandler:
    def __init__(self, message_obj: UserMessage):
        self.message_obj = message_obj
        self.user_id = message_obj.message.chat.id
        self.language = get_user_language(self.user_id)

    def handle(self):
        raise NotImplementedError(f'Request should be handled by bot')

    def make_msg(self, template_code: AvailableMessages, params: List[Any] = None) -> str:
        return make_msg(
            template_code,
            self.language,
            params
        )

    def post_msg(self, template_code: AvailableMessages, params: List[Any] = None):
        requests.post(URL, params={
            "chat_id": self.user_id,
            "text": self.make_msg(
                template_code,
                params
            )
        })


class CommandHandler(RequestHandler):
    @staticmethod
    def get_command_name():
        raise NotImplementedError('Command should have own name')

    def handle(self):
        raise NotImplementedError(f'Command handler for {self.get_command_name()} should exist')


class UnknownTextHandler(RequestHandler):
    def handle(self):
        logging.error(f'logs -> {self.message_obj}')
        self.post_msg(AvailableMessages.unknown_command)
