from telegram import Update
from telegram.ext import CallbackContext

from server_api import get_exercises


async def exercises(update: Update, context: CallbackContext) -> None:
    exercises = get_exercises()
    exercises_str = '\n'.join(list(sorted(exercises)))
    await update.message.reply_text(
        f"I know about this list of activities:\n{exercises_str}"
    )
