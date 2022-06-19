from aiogram import types

from keyboards.default.menu import COMMUNICATION
from loader import dp


@dp.message_handler(text=COMMUNICATION, state='*')
@dp.message_handler(commands=['communication'], state='*')
async def bot_communication(message: types.Message):
    await message.answer("Перейдите по следующему адресу: @OnlineConsultFitServiceBot")