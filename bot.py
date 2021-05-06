import telebot
import consts
import db
import utils

from cfg import config_dict
from typing import Union
from telebot import types


bot = telebot.TeleBot(config_dict["BOT_TOKEN"],
                      parse_mode="markdown", threaded=False, skip_pending=True)


@bot.message_handler(commands=["start"])
def start(msg) -> None:
    db.set_start_page_or_ignore(msg.chat.id)

    location = db.return_value_from_DB(
        table="users", field="location", pivot="tg_user_id", pivot_value=msg.chat.id)

    if not location:
        bot.send_message(msg.chat.id, "Введите Вашу локацию для поиска работы")
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


@bot.message_handler(content_types=["text"])
def all_text(msg) -> None:
    page = db.return_value_from_DB(
        table="users", field="page", pivot="tg_user_id", pivot_value=msg.chat.id)

    if page.startswith("input"):
        value_to_input = page.split("_", 1)[1]

        if value_to_input == "location":
            db.change_value_in_DB(table="users", field_to_update="location",
                                  field_to_update_value=msg.text, pivot="tg_user_id", pivot_value=msg.chat.id)

            bot.send_message(msg.chat.id, "Ваша локация успешно обновлена")

            bot.send_message(msg.chat.id,
                             consts.START_MESSAGE,
                             reply_markup=utils.create_inline_keyboard_markup(
                                 kb=consts.START_KB, group=msg.text),
                             )
            db.change_value_in_DB(table="users", field_to_update="page",
                                  field_to_update_value="start", pivot="tg_user_id", pivot_value=msg.chat.id)
        else:
            is_full = db.check_if_vacancy_is_full(msg.chat.id)

            if is_full:
                bot.send_message(msg.chat.id, "Вакансия успешно добавлена")
                bot.send_message(msg.chat.id,
                                 consts.START_MESSAGE,
                                 reply_markup=utils.create_inline_keyboard_markup(
                                     kb=consts.START_KB),
                                 )
                db.insert_empty(msg.chat.id)
            else:
                value_to_input = value_to_input.split("_")[1]

                db.change_value_in_DB(table="vacancies", field_to_update=value_to_input,
                                      field_to_update_value=msg.text, pivot="tg_user_id", pivot_value=msg.chat.id)
                bot.send_message(msg.chat.id, "Информация успешно обновлена")

                is_full = db.check_if_vacancy_is_full(msg.chat.id)

                if is_full:
                    bot.send_message(
                        msg.chat.id, "Вакансия успешно добавлена")
                    bot.send_message(msg.chat.id,
                                     consts.START_MESSAGE,
                                     reply_markup=utils.create_inline_keyboard_markup(
                                         kb=consts.START_KB),
                                     )
                    db.insert_empty(msg.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("employer"))
def send_inlinekb_for_employer(call) -> None:
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=consts.EMPLOYER_MESSAGE,
        reply_markup=utils.create_inline_keyboard_markup(
            kb=consts.EMPLOYER_KB, page="start"),
    )

    db.change_value_in_DB(table="users", field_to_update="page",
                          field_to_update_value="employer", pivot="tg_user_id", pivot_value=call.message.chat.id)

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("back"))
def back_to(call) -> None:
    page = call.data.split("_")[1]

    text: str
    reply_markup: Union[types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup]

    if page == "start":
        text = consts.START_MESSAGE
        reply_markup = utils.create_inline_keyboard_markup(kb=consts.START_KB)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=reply_markup,
    )

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("set"))
def back_to(call) -> None:
    value_to_set = call.data.split("_")[1]

    text: str

    if value_to_set == "title":
        text = "Введите заголовок для вакансии"
    elif value_to_set == "info":
        text = "Введите описание вакансии"
    elif value_to_set == "location":
        text = "Введите местонахождение вакансии"

    bot.send_message(call.message.chat.id, text)

    db.change_value_in_DB(table="users", field_to_update="page",
                          field_to_update_value=f"input_vacancies_{value_to_set}", pivot="tg_user_id", pivot_value=call.message.chat.id)

    bot.answer_callback_query(call.id)
