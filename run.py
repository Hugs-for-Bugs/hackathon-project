import db

from bot import bot


if __name__ == "__main__":
    db.create_users_table()

    bot.polling()
