from .activity_add_command import ActivityAddCommandHandler
from .base import UnknownTextHandler
from .exercises_command import ExercisesCommandHandler
from .start_command import StartCommandHandler

HANDLED_COMMANDS = [StartCommandHandler, ActivityAddCommandHandler, ExercisesCommandHandler]
