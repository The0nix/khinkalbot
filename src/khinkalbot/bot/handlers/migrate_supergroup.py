import logging

from aiogram import types

from khinkalbot.bot.vitals import dp
from khinkalbot.db.db import db
from khinkalbot.db.models.user import User

logger = logging.getLogger()


@dp.message_handler(content_types=["migrate_to_chat_id"])
async def group_upgrade_to(message: types.Message):
    """
    When group is migrated to supergroup, sends new chat ID.
    Notice that the first argument of send_message is message.migrate_to_chat_id, not message.chat.id!
    Otherwise, MigrateChat exception will raise
    :param message: Telegram message with "migrate_to_chat_id" field not empty
    """
    db.connect()
    User.update(chat_id=message.migrate_to_chat_id).where(User.chat_id == message.chat.id).execute()
    db.close()
    logger.info(f"Group upgraded to supergroup.\n"
                f"Old ID: <code>{message.chat.id}</code>\n"
                f"New ID: <code>{message.migrate_to_chat_id}</code>")
