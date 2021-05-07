from project.bot import utils
from project.bot import consts

from project.db import db
from project.parser import work_ua

from telebot import types

from project.bot.bot import bot


@bot.message_handler(content_types=["text"])
def all_text(msg: types.Message) -> None:
    page = db.return_value_from_DB(
        table="users", field="page", pivot="tg_user_id", pivot_value=msg.chat.id)

    if page.startswith("input"):
        type_of_value_to_input = page.split("_", 1)[1]

        if type_of_value_to_input == "location":
            db.change_value_in_DB(table="users", field_to_update="location",
                                  field_to_update_value=msg.text.lower(), pivot="tg_user_id", pivot_value=msg.chat.id)

            bot.send_message(msg.chat.id, "Your Location updated successfully")

            bot.send_message(msg.chat.id,
                             consts.START_MESSAGE,
                             reply_markup=utils.create_inline_keyboard_markup(
                                 kb=consts.START_KB, group=msg.text),
                             )
            db.change_value_in_DB(table="users", field_to_update="page",
                                  field_to_update_value="start", pivot="tg_user_id", pivot_value=msg.chat.id)
        elif type_of_value_to_input == "vacancy":
            location = db.return_value_from_DB(
                table="users", field="location", pivot="tg_user_id", pivot_value=msg.chat.id)

            vacancies = work_ua.work(msg.text, location)

            if vacancies:
                msg_for_user: str = ""

                for vacancy in vacancies.values():
                    msg_for_user += f"[{vacancy['title']}]({vacancy['href']})\n{vacancy['info'].strip()}\n\n"

                bot.send_message(msg.chat.id, msg_for_user,
                                 disable_web_page_preview=True)
            else:
                bot.send_message(
                    msg.chat.id, "Nothing found for your location")
                bot.send_message(msg.chat.id,
                                 consts.START_MESSAGE,
                                 reply_markup=utils.create_inline_keyboard_markup(
                                     kb=consts.START_KB, group=msg.text),
                                 )
                db.change_value_in_DB(table="users", field_to_update="page",
                                      field_to_update_value="start", pivot="tg_user_id", pivot_value=msg.chat.id)

        else:
            type_of_value_to_input = type_of_value_to_input.split("_")[1]

            db.change_value_in_DB(table="vacancies", field_to_update=type_of_value_to_input,
                                  field_to_update_value=msg.text.lower(), pivot="tg_user_id", pivot_value=msg.chat.id)
            bot.send_message(
                msg.chat.id, "Information has been successfully updated")

            is_full = db.check_if_vacancy_is_full(msg.chat.id)

            if is_full:
                bot.send_message(
                    msg.chat.id, "Vacancy successfully added")
                bot.send_message(msg.chat.id,
                                 consts.START_MESSAGE,
                                 reply_markup=utils.create_inline_keyboard_markup(
                                     kb=consts.START_KB),
                                 )
                db.insert_empty(msg.chat.id)
