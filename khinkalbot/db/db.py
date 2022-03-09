import peewee

DATABASE_NAME = "users_data.db"

db = peewee.SqliteDatabase(DATABASE_NAME)
