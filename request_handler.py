import requests

from constants import TELEGRAM_TOKEN, API_URL
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


class ActivityAddCommandHandler(CommandHandler):
    @staticmethod
    def get_command_name():
        return "/activity_add"

    def types_check(self, text_parts: list):
        msgs = []
        command, activity_name, iterations_count, pause_before_item = text_parts
        ALLOWED_ACTIVITES = ['push-ups', 'press']
        if activity_name not in ALLOWED_ACTIVITES:
            activities_str = ", ".join(ALLOWED_ACTIVITES)
            msgs.append(
                make_msg(
                    AvailableMessages.command__activity_add__unknown_activity,
                    AvailableLanguagesEnum.eng,
                    [activity_name, activities_str]
                )
            )
        try:
            int(iterations_count)
            if int(iterations_count) < 1:
                raise ValueError
        except ValueError:
            msgs.append(
                make_msg(
                    AvailableMessages.command__activity_add__iterations_count_error,
                    AvailableLanguagesEnum.eng,
                    [iterations_count]
                )
            )
        try:
            float(pause_before_item)
            if float(pause_before_item) < 0:
                raise ValueError
        except ValueError:
            msgs.append(
                make_msg(
                    AvailableMessages.command__activity_add__pause_before_error,
                    AvailableLanguagesEnum.eng,
                    [pause_before_item]
                )
            )
        return '\n'.join(msgs)

    def send_info_to_server(self, text_parts):
        command, activity_name, iterations_count, pause_before_item = text_parts
        iterations_count = int(iterations_count)
        pause_before_item = float(pause_before_item)
        r = requests.post(f"{API_URL}/api/workout-item/", json={
            "name": activity_name,
            "iterations_count": iterations_count,
            "pause_before_item": pause_before_item
        })
        if r.status_code == 200:
            requests.post(URL, params={
                "chat_id": self.message_obj.message.chat.id,
                "text": make_msg(
                    AvailableMessages.command__activity_add__info_was_sent,
                    AvailableLanguagesEnum.eng
                )
            })

    def handle(self):
        text_parts = self.message_obj.message.text.split(' ')
        msg = ''
        if len(text_parts) != 4:
            msg = make_msg(
                AvailableMessages.command__activity_add__arguments_error,
                AvailableLanguagesEnum.eng
            )
        else:
            checks_result = self.types_check(text_parts)
            if checks_result:
                pretext_msg = make_msg(
                    AvailableMessages.command__activity_add__errors_pretext,
                    AvailableLanguagesEnum.eng
                )
                msg = f"{pretext_msg}\n{checks_result}"
            else:
                self.send_info_to_server(text_parts)
                msg = make_msg(
                    AvailableMessages.command__activity_add__info_was_saved,
                    AvailableLanguagesEnum.eng
                )

        requests.post(URL, params={"chat_id": self.message_obj.message.chat.id, "text": msg})


HANDLED_COMMANDS = [StartCommandHandler, ActivityAddCommandHandler]


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
