import telebot
import consts
import db
import utils

from cfg import config_dict


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
def all_text(msg):
    page = db.return_value_from_DB(
        table="users", field="page", pivot="tg_user_id", pivot_value=msg.chat.id)

    if page == "input_location":
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
