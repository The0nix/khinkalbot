import peewee

from khinkalbot.db.db import db


class User(peewee.Model):
    object_id = peewee.AutoField()
    id = peewee.BigIntegerField()
    chat_id = peewee.BigIntegerField()
    login = peewee.CharField()
    khinkal_count = peewee.IntegerField(default=0)
    start_date = peewee.DateField()

    class Meta:
        database = db
