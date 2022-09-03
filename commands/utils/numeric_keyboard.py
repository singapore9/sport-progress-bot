import logging
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Enable logging
logger = logging.getLogger(__name__)


def get_numeric_keyboard(key_for_update, data, previous_key):
    SEND, DELETE, PREVIOUS_STEP = 'send', 'delete', 'previous_step'
    def get_new_dict(old_data, pressed_key):
        new_dict = dict([[k, v] for k, v in old_data.items()])
        value = new_dict.get(key_for_update)
        if pressed_key == DELETE:
            if value is not None:
                value = value[:-1] or '0'
        elif pressed_key == SEND:
            if value is not None:
                value = f'ok{int(value)}'
            else:
                value = 'ok0'
        else:
            if value is not None:
                if 'ok' in value:
                    value = value[3:]
                value = str(int(f"{value}{pressed_key}"))
            else:
                value = pressed_key
        new_dict[key_for_update] = value
        logger.info(f'NEW DICT IS: {new_dict}')
        return new_dict

    value = data.get(key_for_update)
    if value is None:
        data[key_for_update] = "0"

    bottom_line_codes = []
    value = data.get(key_for_update)
    if value != "0":
        bottom_line_codes.append(DELETE)
        bottom_line_codes.append("0")
    bottom_line_codes.append(SEND)

    def get_numeric_line(ind):
        pref = ind*3
        return [
            InlineKeyboardButton(
                str(pref + c),
                callback_data=json.dumps(get_new_dict(data, str(pref + c)))
            ) for c in [1, 2, 3]
        ]
    previous_dict = data.copy()
    previous_dict.pop(key_for_update, None)
    previous_dict.pop(previous_key, None)

    keyboard = InlineKeyboardMarkup([
        get_numeric_line(0),
        get_numeric_line(1),
        get_numeric_line(2),
        [
            InlineKeyboardButton(
                c,
                callback_data=json.dumps(get_new_dict(data, c))
            ) for c in bottom_line_codes
        ],
        [
            InlineKeyboardButton(
                PREVIOUS_STEP,
                callback_data=json.dumps(previous_dict)
            )
        ]
    ])
    return keyboard
