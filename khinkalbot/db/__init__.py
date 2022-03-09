import logging

from khinkalbot.db.models.user import User
from khinkalbot.db.db import db

logger = logging.getLogger()


def init():
    logger.info("Creating tables")
    db.create_tables([User])
    logger.info("Iinitialization successfully completed")
