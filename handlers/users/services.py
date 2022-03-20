from aiogram import types

from keyboards.default.menu import SERVICES_OVERVIEW
from loader import dp
from utils.db_api.database import Service


@dp.message_handler(text=SERVICES_OVERVIEW, state='*')
@dp.message_handler(commands=['services'], state='*')
async def bot_services(message: types.Message):
    await message.answer(
        "\n".join([f"✔ {service.name}" for service in await Service.all()])
    )
