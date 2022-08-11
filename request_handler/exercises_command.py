import requests

from messages import make_msg, AvailableLanguagesEnum, AvailableMessages
from server_api import get_exercises
from .base import CommandHandler, URL


class ExercisesCommandHandler(CommandHandler):
    @staticmethod
    def get_command_name():
        return "/exercises"

    def handle(self):
        exercises = get_exercises()
        exercises_str = '\n'.join(list(sorted(exercises)))

        requests.post(URL, params={
            "chat_id": self.message_obj.message.chat.id,
            "text": make_msg(
                AvailableMessages.command__exercises,
                AvailableLanguagesEnum.eng,
                [exercises_str]
            )
        })
