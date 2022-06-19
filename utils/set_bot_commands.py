from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("services", "Список услуг"),
            types.BotCommand("order", "Записаться на обслуживание"),
            types.BotCommand("contacts", "Контакты"),
            types.BotCommand("communication", "Перейти в чат для консультации"),
        ]
    )
