from enum import Enum
import json

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from commands.constants import COMMAND_KEY, ACTIVITY_ADD_SLUG
from commands.numeric_keyboard import get_numeric_keyboard
from server_api import get_exercises, send_activity


class AddActivityCommandKeys(Enum):
    step1 = "1"
    step2 = "2"
    step3 = "3"


async def activity_add(update: Update, context: CallbackContext) -> None:
    exercises = get_exercises()
    keyboard = [
            [
                InlineKeyboardButton(
                    f"{exercise}",
                    callback_data=AddActivityCommand.dumps(step1=exercise)
                ),
            ] for exercise in exercises
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose:', reply_markup=reply_markup)


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
    async def done(cls, query, data):
        activity_name = data.get(AddActivityCommandKeys.step1.value)
        count = data.get(AddActivityCommandKeys.step2.value)
        seconds = data.get(AddActivityCommandKeys.step3.value)
        await query.edit_message_text(f"Sent:\nactivity_add {activity_name} {count[2:]} {seconds[2:]}")
        iterations_count = int(count[2:])
        pause_before_item = int(seconds[2:])
        r = send_activity(query.from_user.id, activity_name, iterations_count, pause_before_item)
        if r:
            await query.edit_message_text(f"Successfully saved:\nactivity_add {activity_name} {count[2:]} {seconds[2:]}")

    @classmethod
    async def step3(cls, query, data):
        activity_name = data.get(AddActivityCommandKeys.step1.value)
        count = data.get(AddActivityCommandKeys.step2.value)
        seconds = data.get(AddActivityCommandKeys.step3.value)
        if seconds is None or "ok" not in seconds:
            await query.edit_message_text(
                f"Please type waiting time (seconds) before starting this set of repetitions:\n"
                f"activity_add {activity_name} {count[2:]} {seconds or ''}",
                reply_markup=get_numeric_keyboard(
                    AddActivityCommandKeys.step3.value,
                    data,
                    AddActivityCommandKeys.step2.value
                )
            )
        else:
            await cls.done(query, data)

    @classmethod
    async def step2(cls, query, data):
        activity_name = data.get(AddActivityCommandKeys.step1.value)
        count = data.get(AddActivityCommandKeys.step2.value)
        if count is None or "ok" not in count:
            await query.edit_message_text(
                f"Please type repetitions count:\nactivity_add {activity_name} {count or ''}",
                reply_markup=get_numeric_keyboard(
                    AddActivityCommandKeys.step2.value,
                    data,
                    AddActivityCommandKeys.step1.value
                )
            )
        else:
            await cls.step3(query, data)

    @classmethod
    async def step1(cls, query, data):
        activity_name = data.get(AddActivityCommandKeys.step1.value)
        exercises = get_exercises()
        if activity_name is None:
            await query.edit_message_text(
                f"Please choose exercise:\n"
                f"activity_add ",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            f"{exercise}",
                            callback_data=cls.dumps(step1=exercise)
                        ),
                    ] for exercise in exercises
                ])
            )
        else:
            await cls.step2(query, data)
