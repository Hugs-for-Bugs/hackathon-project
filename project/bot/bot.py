import telebot

from project.config import config_dict


bot = telebot.TeleBot(config_dict["BOT_TOKEN"],
                      parse_mode="markdown", threaded=False, skip_pending=True)
