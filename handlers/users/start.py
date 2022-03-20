from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import types

from handlers.users.help import bot_help
from keyboards.default.menu import menu_keyboard
from loader import dp
from utils.db_api.database import User


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    await User.get_or_create(
        id=message.from_user.id, first_name=message.from_user.first_name, username=message.from_user.username
    )
    await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=menu_keyboard)
    await bot_help(message)
