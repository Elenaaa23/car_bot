from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state='*')
async def bot_help(message: types.Message):
    await message.answer(
        "\n".join(
            [
                "Выберите нужный пункт меню, для этого нажмите на кнопку или укажите соответствующую кнопку:",
                "・ Ознакомиться с услугами",
                "・ Записаться на обслуживание",
                "・ Контактные данные автосервиса",
            ]
        )
    )
