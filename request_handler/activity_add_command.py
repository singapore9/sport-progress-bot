import requests

from constants import API_URL
from messages import make_msg, AvailableLanguagesEnum, AvailableMessages
from .base import CommandHandler, URL


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
