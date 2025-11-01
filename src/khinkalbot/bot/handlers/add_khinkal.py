import logging
from datetime import datetime

from aiogram import types
from aiogram.utils.callback_data import CallbackData

from khinkalbot.bot.vitals import dp, bot
from khinkalbot.db.db import db
from khinkalbot.db.models.user import User

logger = logging.getLogger()

add_callback = CallbackData("add", "action", "user_id", "user_login", "number")


@dp.message_handler(commands=["add"])
async def add_khinkals(message: types.Message):
    _, number = message.get_full_command()
    try:
        number = int(number)
        assert number > 0
    except (ValueError, AssertionError):
        await message.reply(f"Плохое число: \"{number}\"")
        return

    user_data = dict(
        user_id=message.from_user.id,
        user_login="@" + message.from_user.username,
        number=number,
    )
    text_and_data = (
        ("Всё так", add_callback.new(action="ok", **user_data)),
        ("Врёт", add_callback.new(action="bad", **user_data))
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    keyboard_markup.row(*row_btns)

    await message.reply(
        f"Подтвердите, @{message.from_user.username} съел {number} хинкалей?", reply_markup=keyboard_markup
    )


@dp.callback_query_handler(add_callback.filter(action="ok"))
async def add_khinkal_ok_handler(query: types.CallbackQuery, callback_data: dict):
    if not isinstance(await bot.get_chat_member(query.message.chat.id, query.from_user.id), 
                      (types.ChatMemberAdministrator, types.ChatMemberOwner)):
        await query.answer("Ты не администратор")
        return
    number = int(callback_data["number"])
    db.connect()
    user, created = User.get_or_create(
        id=callback_data["user_id"],
        chat_id=query.message.chat.id,
        defaults={
            "login": callback_data["user_login"],
            "start_date": datetime.now(),
            "khinkal_count": number,
        }
    )
    if user.login != callback_data["user_login"]:
        user.login = callback_data["user_login"]
    old_count = user.khinkal_count if not created else 0
    if not created:
        user.khinkal_count += number
    new_count = user.khinkal_count
    user.save()
    db.close()
    await bot.edit_message_text(
        f"{user.login} съел(а) {number} хинкалей. ({old_count} -> {new_count})",
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )
    await query.answer("Кул")


@dp.callback_query_handler(add_callback.filter(action="bad"))
async def add_khinkal_bad_handler(query: types.CallbackQuery, callback_data: dict):
    if not isinstance(await bot.get_chat_member(query.message.chat.id, query.from_user.id), 
                      (types.ChatMemberAdministrator, types.ChatMemberOwner)):
        await query.answer("Ты не администратор")
        return
    await bot.edit_message_text(
        f"{callback_data['user_login']} наврал. Не засчитываем.",
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )
    await query.answer("Яяяяясно")
