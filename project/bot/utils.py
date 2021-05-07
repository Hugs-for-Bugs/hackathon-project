from telebot import types


def create_inline_keyboard_markup(**kwargs: dict) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)

    inline_keyboard_buttons = [types.InlineKeyboardButton(
        text=text,
        callback_data=kwargs["kb"]["callbacks"][i].format(**kwargs),
    ) for i, text in enumerate(kwargs["kb"]["text"])]

    kb.add(*inline_keyboard_buttons)

    return kb
