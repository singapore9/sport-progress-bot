from enum import Enum
import json

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from commands.constants import COMMAND_KEY, ACTIVITY_ADD_SLUG
from commands.utils.additional_params import pass_language
from commands.utils.numeric_keyboard import get_numeric_keyboard
from messages import AvailableLanguagesEnum, AvailableMessages, make_msg
from server_api import get_exercises, send_activity


class AddActivityCommandKeys(Enum):
    step1 = "1"
    step2 = "2"
    step3 = "3"


@pass_language
async def activity_add(language: AvailableLanguagesEnum, update: Update, context: CallbackContext) -> None:
    exercises = get_exercises(language)
    keyboard = [
            [
                InlineKeyboardButton(
                    f"{localized_name}",
                    callback_data=AddActivityCommand.dumps(step1=exercise_code)
                ),
            ] for exercise_code, localized_name in exercises
    ]
    msg = make_msg(
        AvailableMessages.command__activity_add__select,
        language
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(msg, reply_markup=reply_markup)


class AddActivityCommand:
    @classmethod
    def dumps(cls, step1=None, step2=None, step3=None):
        data = {
            COMMAND_KEY: ACTIVITY_ADD_SLUG
        }
        if step1 is not None:
            data[AddActivityCommandKeys.step1.value] = step1
        if step2 is not None:
            data[AddActivityCommandKeys.step2.value] = step2
        if step3 is not None:
            data[AddActivityCommandKeys.step3.value] = step3
        return json.dumps(data)

    @classmethod
    async def done(cls, user_id, language, query, data):
        activity_name = data.get(AddActivityCommandKeys.step1.value)
        count = data.get(AddActivityCommandKeys.step2.value)
        seconds = data.get(AddActivityCommandKeys.step3.value)
        command = f"activity_add {activity_name} {count[2:]} {seconds[2:]}"
        msg = make_msg(
            AvailableMessages.base_command__info_was_sent,
            language,
            [command, ]
        )
        await query.edit_message_text(msg)
        iterations_count = int(count[2:])
        pause_before_item = int(seconds[2:])
        r = send_activity(user_id, activity_name, iterations_count, pause_before_item)
        if r:
            msg = make_msg(
                AvailableMessages.base_command__info_was_saved,
                language,
                [command, ]
            )
            await query.edit_message_text(msg)

    @classmethod
    async def step3(cls, user_id, language, query, data):
        activity_name = data.get(AddActivityCommandKeys.step1.value)
        count = data.get(AddActivityCommandKeys.step2.value)
        seconds = data.get(AddActivityCommandKeys.step3.value)
        if seconds is None or "ok" not in seconds:
            command = f"activity_add {activity_name} {count[2:]} {seconds or ''}"
            msg = make_msg(
                AvailableMessages.command__activity_add__step3__select,
                language,
                [command, ]
            )
            await query.edit_message_text(
                msg,
                reply_markup=get_numeric_keyboard(
                    AddActivityCommandKeys.step3.value,
                    data,
                    AddActivityCommandKeys.step2.value
                )
            )
        else:
            await cls.done(user_id, language, query, data)

    @classmethod
    async def step2(cls, user_id, language, query, data):
        activity_name = data.get(AddActivityCommandKeys.step1.value)
        count = data.get(AddActivityCommandKeys.step2.value)
        if count is None or "ok" not in count:
            command = f"activity_add {activity_name} {count or ''}"
            msg = make_msg(
                AvailableMessages.command__activity_add__step2__select,
                language,
                [command, ]
            )
            await query.edit_message_text(
                msg,
                reply_markup=get_numeric_keyboard(
                    AddActivityCommandKeys.step2.value,
                    data,
                    AddActivityCommandKeys.step1.value
                )
            )
        else:
            await cls.step3(user_id, language, query, data)

    @classmethod
    async def step1(cls, user_id, language, query, data):
        activity_name = data.get(AddActivityCommandKeys.step1.value)
        exercises = get_exercises(language)
        if activity_name is None:
            msg = make_msg(
                AvailableMessages.command__activity_add__step1__select,
                language
            )
            await query.edit_message_text(
                msg,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            f"{localized_name}",
                            callback_data=cls.dumps(step1=exercise_code)
                        ),
                    ] for exercise_code, localized_name in exercises
                ])
            )
        else:
            await cls.step2(user_id, language, query, data)
