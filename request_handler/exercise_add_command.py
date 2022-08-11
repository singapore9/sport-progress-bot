import requests

from messages import make_msg, AvailableLanguagesEnum, AvailableMessages
from server_api import send_exercise, get_exercises
from .base import CommandHandler, URL


class ExerciseAddCommandHandler(CommandHandler):
    @staticmethod
    def get_command_name():
        return "/exercise_add"

    def types_check(self, text_parts: list):
        msgs = []
        command, exercise_name = text_parts
        existed_exercises = get_exercises()
        if exercise_name in existed_exercises:
            msgs.append(
                make_msg(
                    AvailableMessages.command__exercise_add__duplicate_error,
                    AvailableLanguagesEnum.eng,
                    [exercise_name]
                )
            )
        return '\n'.join(msgs)

    def send_info_to_server(self, text_parts):
        command, exercise_name = text_parts
        r = send_exercise(exercise_name)
        if r:
            requests.post(URL, params={
                "chat_id": self.message_obj.message.chat.id,
                "text": make_msg(
                    AvailableMessages.command__exercise_add__info_was_sent,
                    AvailableLanguagesEnum.eng
                )
            })

    def handle(self):
        text_parts = self.message_obj.message.text.split(' ')
        msg = ''
        if len(text_parts) != 2:
            msg = make_msg(
                AvailableMessages.command__exercise_add__arguments_error,
                AvailableLanguagesEnum.eng
            )
        else:
            checks_result = self.types_check(text_parts)
            if checks_result:
                pretext_msg = make_msg(
                    AvailableMessages.command__exercise_add__errors_pretext,
                    AvailableLanguagesEnum.eng
                )
                msg = f"{pretext_msg}\n{checks_result}"
            else:
                self.send_info_to_server(text_parts)
                msg = make_msg(
                    AvailableMessages.command__exercise_add__info_was_saved,
                    AvailableLanguagesEnum.eng
                )

        requests.post(URL, params={"chat_id": self.message_obj.message.chat.id, "text": msg})
