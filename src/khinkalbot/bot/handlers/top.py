import aiogram.utils.markdown as md
from aiogram import types
from datetime import date

from khinkalbot.bot.vitals import dp
from khinkalbot.db.models.user import User
from khinkalbot.db.db import db


def make_top_row(user, place):
    if 1 <= place <= 3:
        place = {1: "🥇", 2: "🥈", 3: "🥉"}[place]
    else:
        place = f"  {place}. "
    part1 = f"{place} {user.login[1:]}: {md.hbold(user.khinkal_count)}"
    part2 = f"с {user.start_date:%d.%m.%y}"
    days_elapsed = (date.today() - user.start_date).days
    if days_elapsed > 0:
        khinkal_per_day = md.hbold(f"{user.khinkal_count / days_elapsed:.1f}")
        part2 += f" — {khinkal_per_day} х/д"
    result = f"{part1} ({part2})"
    return result


def make_khinkal_top(users: User) -> str:
    rows = [make_top_row(user, i) for i, user in enumerate(users, 1)]

    return "\n".join(rows)


@dp.message_handler(commands=["top"])
async def get_leaderboard(message: types.Message):
    db.connect()
    users = list(User.select().where(User.chat_id == message.chat.id).order_by(User.khinkal_count.desc()))
    db.close()
    if not users:
        reply_text = "Пока никто не поел хинкалей"
    else:
        reply_text = make_khinkal_top(users)
    await message.reply(reply_text, parse_mode=types.ParseMode.HTML)
