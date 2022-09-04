from enum import Enum
import json

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from commands.constants import COMMAND_KEY, SET_LANGUAGE_SLUG
from commands.utils.additional_params import pass_language
from messages import AvailableLanguagesEnum, AvailableMessages, make_msg
from server_api import set_user_language


class SetLanguageCommandKeys(Enum):
    step1 = "1"


@pass_language
async def set_language(language: AvailableLanguagesEnum, update: Update, context: CallbackContext) -> None:
    keyboard = [
            [
                InlineKeyboardButton(
                    f"{language.name.capitalize()}",
                    callback_data=SetLanguageCommand.dumps(step1=language.name)
                ),
            ] for language in AvailableLanguagesEnum
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = make_msg(
        AvailableMessages.command__language__select,
        language
    )
    await update.message.reply_text(msg, reply_markup=reply_markup)


class SetLanguageCommand:
    @classmethod
    def dumps(cls, step1=None):
        data = {
            COMMAND_KEY: SET_LANGUAGE_SLUG
        }
        if step1 is not None:
            data[SetLanguageCommandKeys.step1.value] = step1
        return json.dumps(data)

    @classmethod
    async def done(cls, query, data):
        language_name = data.get(SetLanguageCommandKeys.step1.value)
        language = AvailableLanguagesEnum[language_name]
        await query.edit_message_text(f"Sent:\nlanguage {language_name}")
        r = set_user_language(query.from_user.id, language)
        if r:
            await query.edit_message_text(f"Successfully saved:\nlanguage {language_name}")

    @classmethod
    async def step1(cls, query, data):
        language_name = data.get(SetLanguageCommandKeys.step1.value)
        if language_name is None:
            await query.edit_message_text(
                f"Please choose preferred language:\n"
                f"language ",
                reply_markup=[
                    [
                        InlineKeyboardButton(
                            f"{language.name.capitalize()}",
                            callback_data=SetLanguageCommand.dumps(step1=language.name)
                        ),
                    ] for language in AvailableLanguagesEnum
                ]
            )
        else:
            await cls.done(query, data)
