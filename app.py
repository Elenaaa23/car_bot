import asyncio

from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.db_api.database import create_database
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_database())

    executor.start_polling(dp, on_startup=on_startup)
