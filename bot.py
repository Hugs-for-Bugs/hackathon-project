import telebot
import consts
import db
import utils

from parser import work_ua

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
        type_of_value_to_input = page.split("_", 1)[1]

        if type_of_value_to_input == "location":
            db.change_value_in_DB(table="users", field_to_update="location",
                                  field_to_update_value=msg.text.lower(), pivot="tg_user_id", pivot_value=msg.chat.id)

            bot.send_message(msg.chat.id, "Ваша локация успешно обновлена")

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

                bot.send_message(msg.chat.id, msg_for_user)
            else:
                bot.send_message(
                    msg.chat.id, "Для вашей локации ничего не найдено")
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


@bot.callback_query_handler(func=lambda call: call.data.startswith("ch_location"))
def change_location_from_inlinekb(call) -> None:
    bot.send_message(call.message.chat.id,
                     "Введите Вашу локацию для поиска работы")
    db.change_value_in_DB(table="users", field_to_update="page",
                          field_to_update_value="input_location", pivot="tg_user_id", pivot_value=call.message.chat.id)

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("search_bot"))
def search_vacancy_in_bot_from_inlinekb(call) -> None:
    location = db.return_value_from_DB(
        table="users", field="location", pivot="tg_user_id", pivot_value=call.message.chat.id)

    vacancies = db.get_vacancies(location)
    if not len(vacancies):
        bot.send_message(call.message.chat.id,
                         "В выбранной вами локации нет ваканский")
    else:
        msg_for_user: str = ""

        for i, vacancy in enumerate(vacancies):
            msg_for_user += f"{i + 1}.\n*Название*: {vacancy[2]}\n*О чем*:\n{vacancy[3]}\n*Контактная информация*:\n{vacancy[5]}\n\n[Работодатель](tg://user?id={vacancy[1]})\n\n"

        bot.send_message(call.message.chat.id, msg_for_user)

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("search_online"))
def search_vacancy_in_online_from_inlinekb(call) -> None:
    location = db.return_value_from_DB(
        table="users", field="location", pivot="tg_user_id", pivot_value=call.message.chat.id)

    bot.send_message(call.message.chat.id,
                     "Введите интересующую вас вакансию")
    db.change_value_in_DB(table="users", field_to_update="page",
                          field_to_update_value="input_vacancy", pivot="tg_user_id", pivot_value=call.message.chat.id)

    bot.answer_callback_query(call.id)


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
def set_value_for_vacancy(call) -> None:
    value_to_set = call.data.split("_")[1]

    text: str

    if value_to_set == "title":
        text = "Введите заголовок для вакансии"
    elif value_to_set == "info":
        text = "Введите описание вакансии"
    elif value_to_set == "location":
        text = "Введите местонахождение вакансии"
    elif value_to_set == "contacts":
        text = "Введи контакты вашей организации"

    bot.send_message(call.message.chat.id, text)

    db.change_value_in_DB(table="users", field_to_update="page",
                          field_to_update_value=f"input_vacancies_{value_to_set}", pivot="tg_user_id", pivot_value=call.message.chat.id)

    bot.answer_callback_query(call.id)
