from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import order_select_car, order, order_select_car_service, order_get_full_name
from utils.db_api.database import Car, CarService


async def cars_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=4)

    keyboard.add(
        *[InlineKeyboardButton(
            text=car.name, callback_data=order_select_car.new(car_id=car.id)
        ) for car in await Car.all()]
    )
    return keyboard


async def services_for_car_keyboard(car_id: int):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        *[InlineKeyboardButton(
            text=car_service_name, callback_data=order_select_car_service.new(car_service_id=car_service_id)
        ) for car_service_id, car_service_name in await CarService.for_car(car_id=car_id)]
    )
    keyboard.row(
        InlineKeyboardButton(
            text="🔙", callback_data=order.new()
        )
    )
    return keyboard


def create_order_keyboard():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            text="Записаться", callback_data=order_get_full_name.new()
        )
    )
    return keyboard

