import telebot
import consts

from cfg import config_dict


bot = telebot.TeleBot(config_dict["BOT_TOKEN"],
                      parse_mode="markdown", threaded=False, skip_pending=True)


@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id, consts.START_MESSAGE)
