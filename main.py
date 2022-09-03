import logging
import json

from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler)
from telegram.ext.filters import TEXT, COMMAND
from commands import COMMAND_KEY, COMMAND_ACTIVITY_BY_COMMAND_KEY, COMMAND_HANDLER_BY_COMMAND_NAME
from constants import TELEGRAM_TOKEN


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Enable logging
logger = logging.getLogger(__name__)


async def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    data = json.loads(query.data)
    command_name = data.get(COMMAND_KEY)
    CommandClass = COMMAND_ACTIVITY_BY_COMMAND_KEY.get(command_name)
    if CommandClass:
        await CommandClass.step1(query, data)
    else:
        await query.edit_message_text(text="unhandled command.. :)")


async def echo(update: Update, context: CallbackContext) -> None:
    await update.effective_message.reply_text(update.effective_message.text)


def get_tg_application():
    tg_application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    for command_name, handler_callback in COMMAND_HANDLER_BY_COMMAND_NAME.items():
        handler = CommandHandler(command_name, handler_callback)
        tg_application.add_handler(handler)

    tg_application.add_handler(CallbackQueryHandler(button))
    tg_application.add_handler(MessageHandler(TEXT & ~COMMAND, echo))
    return tg_application


app = FastAPI()
tg_application = get_tg_application()


@app.post("/webhook")
async def webhook_handler(req: Request):
    data = await req.json()

    try:
        await tg_application.initialize()
        update = Update.de_json(data, tg_application.bot)
        await tg_application.process_update(update)
    except Exception as e:
        print(f'Webhook error: {e}')
