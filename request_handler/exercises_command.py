from messages import AvailableMessages
from server_api import get_exercises
from .base import CommandHandler


class ExercisesCommandHandler(CommandHandler):
    @staticmethod
    def get_command_name():
        return "/exercises"

    def handle(self):
        exercises = get_exercises()
        exercises_str = '\n'.join(list(sorted(exercises)))

        self.post_msg(AvailableMessages.command__exercises, [exercises_str])
