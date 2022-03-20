from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

SERVICES_OVERVIEW = 'Ознакомиться с услугами'
ORDER_FOR_SERVICE = 'Записаться на обслуживание'
CONTACTS = 'Контактные данные автосервиса'

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[

        [KeyboardButton(text=SERVICES_OVERVIEW)],
        [KeyboardButton(text=ORDER_FOR_SERVICE)],
        [KeyboardButton(text=CONTACTS)]

    ],
    resize_keyboard=True
)
