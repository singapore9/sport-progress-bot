from messages import AvailableMessages
from .base import CommandHandler


class StartCommandHandler(CommandHandler):
    @staticmethod
    def get_command_name():
        return "/start"

    def handle(self):
        self.post_msg(AvailableMessages.command__start)
