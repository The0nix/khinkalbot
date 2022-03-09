def start_bot():
    from aiogram import executor
    from khinkalbot.bot.vitals import dp
    import khinkalbot.bot.handlers  # noqa
    executor.start_polling(dp, skip_updates=True)
