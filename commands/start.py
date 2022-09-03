from telegram import Update
from telegram.ext import CallbackContext

from constants import API_URL


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    await update.message.reply_text(
        f"Hi! I'm your progress saver. Share them with me.\nYour results will be here:\n{API_URL}/?{user_id}"
    )
