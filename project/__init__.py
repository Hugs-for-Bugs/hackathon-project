from project.bot import bot
from project.db import db


def run() -> None:
    db.create_tables()
    bot.polling()
