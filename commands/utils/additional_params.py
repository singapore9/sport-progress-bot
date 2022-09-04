from telegram import Update
from telegram.ext import CallbackContext

from server_api import get_user_language


def pass_user_id(func):
    async def wrapped(update: Update, context: CallbackContext, *args, **kwargs) -> None:
        user_id = update.message.from_user.id
        return await func(user_id=user_id, update=update, context=context, *args, **kwargs)
    return wrapped


def pass_language(func):
    async def wrapped(update: Update, context: CallbackContext, *args, **kwargs) -> None:
        user_id = update.message.from_user.id
        language = get_user_language(user_id)
        return await func(language=language, update=update, context=context, *args, **kwargs)
    return wrapped
