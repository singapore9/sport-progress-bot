import requests

from messages import AvailableMessages
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
                self.make_msg(
                    AvailableMessages.command__exercise_add__duplicate_error,
                    [exercise_name]
                )
            )
        return '\n'.join(msgs)

    def send_info_to_server(self, text_parts):
        command, exercise_name = text_parts
        r = send_exercise(exercise_name)
        if r:
            self.post_msg(
                AvailableMessages.command__exercise_add__info_was_sent
            )

    def handle(self):
        text_parts = self.message_obj.message.text.split(' ')
        msg = ''
        if len(text_parts) != 2:
            msg = self.make_msg(
                AvailableMessages.command__exercise_add__arguments_error
            )
        else:
            checks_result = self.types_check(text_parts)
            if checks_result:
                pretext_msg = self.make_msg(
                    AvailableMessages.command__exercise_add__errors_pretext
                )
                msg = f"{pretext_msg}\n{checks_result}"
            else:
                self.send_info_to_server(text_parts)
                msg = self.make_msg(
                    AvailableMessages.command__exercise_add__info_was_saved
                )

        requests.post(URL, params={"chat_id": self.user_id, "text": msg})
