from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderState(StatesGroup):
    car_id = State()
    car_service_id = State()
    full_name = State()
    phone = State()
