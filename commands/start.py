from telegram import Update
from telegram.ext import CallbackContext

from commands.utils.additional_params import pass_user_id, pass_language
from constants import API_URL
from messages import AvailableLanguagesEnum, AvailableMessages, make_msg


@pass_user_id
@pass_language
async def start(user_id: int, language: AvailableLanguagesEnum, update: Update, context: CallbackContext) -> None:
    msg = make_msg(
        AvailableMessages.command__start,
        language,
        [f'{API_URL}/?{user_id}', ]
    )
    await update.message.reply_text(msg)
