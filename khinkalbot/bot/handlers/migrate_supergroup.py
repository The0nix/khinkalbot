from aiogram import types
from khinkalbot.bot.vitals import dp, bot


@dp.message_handler(content_types=["migrate_to_chat_id"])
async def group_upgrade_to(message: types.Message):
    """
    When group is migrated to supergroup, sends new chat ID.
    Notice that the first argument of send_message is message.migrate_to_chat_id, not message.chat.id!
    Otherwise, MigrateChat exception will raise
    :param message: Telegram message with "migrate_to_chat_id" field not empty
    """
    await bot.send_message(message.migrate_to_chat_id, f"Group upgraded to supergroup.\n"
                                                       f"Old ID: <code>{message.chat.id}</code>\n"
                                                       f"New ID: <code>{message.migrate_to_chat_id}</code>")
