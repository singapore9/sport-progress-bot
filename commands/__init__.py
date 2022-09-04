from commands.add_activity import activity_add, AddActivityCommand
from commands.constants import ACTIVITY_ADD_SLUG, SET_LANGUAGE_SLUG, COMMAND_KEY
from commands.exercises import exercises
from commands.set_language import set_language, SetLanguageCommand
from commands.start import start

COMMAND_ACTIVITY_BY_COMMAND_KEY = {
    ACTIVITY_ADD_SLUG: AddActivityCommand,
    SET_LANGUAGE_SLUG: SetLanguageCommand,
}

COMMAND_HANDLER_BY_COMMAND_NAME = {
    'activity_add': activity_add,
    'exercises': exercises,
    'language': set_language,
    'start': start
}