from telegram import Update
from telegram.ext import CallbackContext

from commands.utils.additional_params import pass_language
from messages import AvailableLanguagesEnum, AvailableMessages, make_msg
from server_api import get_exercises


@pass_language
async def exercises(language: AvailableLanguagesEnum, update: Update, context: CallbackContext) -> None:
    exercises = get_exercises()
    exercises_str = '\n'.join(list(sorted(exercises)))
    msg = make_msg(
        AvailableMessages.command__exercises,
        language,
        [exercises_str]
    )
    await update.message.reply_text(msg)
