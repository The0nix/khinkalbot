import os

from aiogram import Bot, Dispatcher

API_TOKEN = os.environ["BOT_TOKEN"]

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
