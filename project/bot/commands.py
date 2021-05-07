from project.bot import utils
from project.bot import consts

from project.db import db

from telebot import types

from project.bot.bot import bot


@bot.message_handler(commands=["start"])
def start(msg: types.Message) -> None:
    db.set_start_page_or_ignore(msg.chat.id)

    location = db.return_value_from_DB(
        table="users", field="location", pivot="tg_user_id", pivot_value=msg.chat.id)

    if not location:
        bot.send_message(msg.chat.id, "*Enter your location for job search:*")
        db.change_value_in_DB(table="users", field_to_update="page",
                              field_to_update_value="input_location", pivot="tg_user_id", pivot_value=msg.chat.id)
    else:
        bot.send_message(msg.chat.id,
                         consts.START_MESSAGE,
                         reply_markup=utils.create_inline_keyboard_markup(
                             kb=consts.START_KB),
                         )
        db.change_value_in_DB(table="users", field_to_update="page",
                              field_to_update_value="start", pivot="tg_user_id", pivot_value=msg.chat.id)
