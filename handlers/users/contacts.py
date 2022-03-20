from aiogram import types

from keyboards.default.menu import CONTACTS
from loader import dp


@dp.message_handler(text=CONTACTS, state='*')
@dp.message_handler(commands=['contacts'], state='*')
async def bot_contacts(message: types.Message):
    await message.answer("🏡 ул. Софийская, 2\n🕛 Время работы: 8:00 - 22:00\n☎ +7(499)224-94-38\n✉ car@fir-service.ru")