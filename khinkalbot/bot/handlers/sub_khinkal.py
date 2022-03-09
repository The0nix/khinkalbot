import logging

import peewee
import aiogram
from aiogram import types
from aiogram.utils.callback_data import CallbackData

from khinkalbot.bot.vitals import dp, bot
from khinkalbot.db.db import db
from khinkalbot.db.models.user import User

logger = logging.getLogger()

sub_callback = CallbackData("sub", "action", "from_user_login", "to_user_login", "number")


@dp.message_handler(commands=["sub"])
async def add_khinkals(message: types.Message):
    _, args = message.get_full_command()
    try:
        login, number = args.split()
    except ValueError:
        await message.reply(f"Неверные аргументы: \"{args}\". Нужен логин и число хинкалей")
        return
    try:
        number = int(number)
    except ValueError:
        await message.reply(f"Плохое число: \"{number}\"")
        return

    user_data = dict(
        from_user_login="@" + message.from_user.username,
        to_user_login=login,
        number=number,
    )
    text_and_data = (
        ("Да, так его", sub_callback.new(action="ok", **user_data)),
        ("Не", sub_callback.new(action="bad", **user_data))
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    keyboard_markup.row(*row_btns)

    await message.reply(
        f"@{message.from_user.username} хочет лишить {login} {number} хинкалей. Разрешаем?", 
        reply_markup=keyboard_markup
    )


@dp.callback_query_handler(sub_callback.filter(action="ok"))
async def add_khinkal_ok_handler(query: types.CallbackQuery, callback_data: dict):
    if not isinstance(await bot.get_chat_member(query.message.chat.id, query.from_user.id), 
                      (types.ChatMemberAdministrator, types.ChatMemberOwner)):
        await query.answer("Ты не администратор")
        return
    number = int(callback_data["number"])
    db.connect()
    try:
        user = User.get(
            login=callback_data["to_user_login"],
            chat_id=query.message.chat.id
        )
    except peewee.DoesNotExist:
        db.close()
        await bot.edit_message_text(
            f"А {callback_data['to_user_login']} и не ел хинкалей.",
            query.message.chat.id,
            query.message.message_id,
            reply_markup=None
        )
        await query.answer("Кул")
        return
    old_count = user.khinkal_count
    user.khinkal_count = user.khinkal_count - number if number < user.khinkal_count else 0
    new_count = user.khinkal_count
    if new_count == 0:
        user.delete_instance()
    else:
        user.save()
    db.close()
    await bot.edit_message_text(
        f"У {callback_data['to_user_login']} отняли {number} хинкалей. ({old_count} -> {new_count})",
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )
    await query.answer("ТАК ЕГООООО!")


@dp.callback_query_handler(sub_callback.filter(action="bad"))
async def add_khinkal_bad_handler(query: types.CallbackQuery, callback_data: dict):
    if not isinstance(await bot.get_chat_member(query.message.chat.id, query.from_user.id),
                      (types.ChatMemberAdministrator, types.ChatMemberOwner)):
        await query.answer("Ты не администратор")
        return
    await bot.edit_message_text(
        "Ноуп.",
        query.message.chat.id,
        query.message.message_id,
        reply_markup=None
    )
    await query.answer("Окей")
