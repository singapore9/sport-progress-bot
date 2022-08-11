from .base import UnknownTextHandler
from .start_command import StartCommandHandler
from .activity_add_command import ActivityAddCommandHandler

HANDLED_COMMANDS = [StartCommandHandler, ActivityAddCommandHandler]
