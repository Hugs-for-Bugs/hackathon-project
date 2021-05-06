import db

from telebot import types
from typing import List


def create_inline_keyboard_markup(**kwargs: dict) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)

    inline_keyboard_buttons = [types.InlineKeyboardButton(
        text=text,
        callback_data=kwargs["kb"]["callbacks"][idx].format(**kwargs),
    ) for idx, text in enumerate(kwargs["kb"]["text"])]

    kb.add(*inline_keyboard_buttons)

    return kb


def create_reply_keyboard_markup(buttons: List[str]) -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(
        one_time_keyboard=True,  resize_keyboard=True)

    kb.add(*buttons)

    return kb
