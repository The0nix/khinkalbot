from aiogram import types

from khinkalbot.bot.vitals import dp
from khinkalbot.db.models.user import User
from khinkalbot.db.db import db


def make_khinkal_top(users: User) -> str:

    strings = [f"{i}. {user.login}: {user.khinkal_count} (с {user.start_date:%d.%m.%y})"
               for i, user in enumerate(users, 1)]
    return "\n".join(strings)


@dp.message_handler(commands=["top"])
async def get_leaderboard(message: types.Message):
    db.connect()
    users = list(User.select().where(User.chat_id == message.chat.id).order_by(User.khinkal_count.desc()))
    db.close()
    if not users:
        reply_text = "Пока никто не поел хинкалей"
    else:
        reply_text = make_khinkal_top(users)
    await message.reply(reply_text)
