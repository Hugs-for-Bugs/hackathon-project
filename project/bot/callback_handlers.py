from project.bot import utils
from project.bot import consts

from project.db import db

from telebot import types

from project.bot.bot import bot


@bot.callback_query_handler(func=lambda call: call.data.startswith("ch_location"))
def change_location_from_inlinekb(call: types.CallbackQuery) -> None:
    bot.send_message(call.message.chat.id,
                     "*Enter your location for job search:*")
    db.change_value_in_DB(table="users", field_to_update="page",
                          field_to_update_value="input_location", pivot="tg_user_id", pivot_value=call.message.chat.id)

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("search_bot"))
def search_vacancy_in_bot_from_inlinekb(call: types.CallbackQuery) -> None:
    location = db.return_value_from_DB(
        table="users", field="location", pivot="tg_user_id", pivot_value=call.message.chat.id)

    vacancies = db.get_vacancies(location)
    if not len(vacancies):
        bot.send_message(call.message.chat.id,
                         "There are no vacancies in the location you selected")
    else:
        msg_for_user: str = ""

        for i, vacancy in enumerate(vacancies):
            msg_for_user += f"{i + 1}.\n*Title*: {vacancy[2]}\n*About what*:\n{vacancy[3]}\n*Contact Information*:\n{vacancy[5]}\n\n[Employer](tg://user?id={vacancy[1]})\n\n"

        bot.send_message(call.message.chat.id, msg_for_user)

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("search_online"))
def search_vacancy_in_online_from_inlinekb(call: types.CallbackQuery) -> None:
    location = db.return_value_from_DB(
        table="users", field="location", pivot="tg_user_id", pivot_value=call.message.chat.id)

    bot.send_message(call.message.chat.id,
                     "*Enter the vacancy you are interested in:*")
    db.change_value_in_DB(table="users", field_to_update="page",
                          field_to_update_value="input_vacancy", pivot="tg_user_id", pivot_value=call.message.chat.id)

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("employer"))
def send_inlinekb_for_employer(call: types.CallbackQuery) -> None:
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
def back_to(call: types.CallbackQuery) -> None:
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
def set_value_for_vacancy(call: types.CallbackQuery) -> None:
    value_to_set = call.data.split("_")[1]

    text: str

    if value_to_set == "title":
        text = "*Enter a title for the job:*"
    elif value_to_set == "info":
        text = "*Enter vacancy description:*"
    elif value_to_set == "location":
        text = "*Enter the location of the vacancy:*"
    elif value_to_set == "contacts":
        text = "*Enter the contacts of your organization:*"

    bot.send_message(call.message.chat.id, text)

    db.change_value_in_DB(table="users", field_to_update="page",
                          field_to_update_value=f"input_vacancies_{value_to_set}", pivot="tg_user_id", pivot_value=call.message.chat.id)

    bot.answer_callback_query(call.id)
