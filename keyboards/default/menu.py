from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

SERVICES_OVERVIEW = 'Ознакомиться с услугами'
ORDER_FOR_SERVICE = 'Записаться на обслуживание'
CONTACTS = 'Контактные данные автосервиса'
COMMUNICATION = 'Перейти в чат с оператором'

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[

        [KeyboardButton(text=SERVICES_OVERVIEW)],
        [KeyboardButton(text=ORDER_FOR_SERVICE)],
        [KeyboardButton(text=CONTACTS)],
        [KeyboardButton(text=COMMUNICATION)],

    ],
    resize_keyboard=True
)
