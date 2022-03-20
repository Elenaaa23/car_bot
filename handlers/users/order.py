from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import BotBlocked

from data.config import ADMINS
from keyboards.default.menu import ORDER_FOR_SERVICE, menu_keyboard
from keyboards.default.order import request_phone
from keyboards.inline.callback_data import order_select_car, order, order_select_car_service, order_get_full_name
from keyboards.inline.order import cars_keyboard, services_for_car_keyboard, create_order_keyboard
from loader import dp
from states.order import OrderState
from utils.db_api.database import CarService, Order


@dp.message_handler(text=ORDER_FOR_SERVICE, state='*')
@dp.message_handler(commands=['order'], state='*')
async def bot_order(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await OrderState.car_id.set()

    await message.answer("Выберите марку автомобиля", reply_markup=await cars_keyboard())


@dp.callback_query_handler(order.filter(), state='*')
async def bot_order_callback(call: CallbackQuery, callback_data: dict):
    await bot_order(call.message)


@dp.callback_query_handler(order_select_car.filter(), state=OrderState.car_id)
async def bot_order_select_car_callback(call: CallbackQuery, callback_data: dict, state: FSMContext):
    car_id = int(callback_data['car_id'])
    await state.update_data(car_id=car_id)
    await OrderState.car_service_id.set()

    await call.message.edit_text("Выберите услугу", reply_markup=await services_for_car_keyboard(car_id=car_id))


@dp.callback_query_handler(order_select_car_service.filter(), state=OrderState.car_service_id)
async def bot_order_select_car_service_callback(call: CallbackQuery, callback_data: dict, state: FSMContext):
    car_service_id = int(callback_data['car_service_id'])
    await state.update_data(car_service_id=car_service_id)
    await state.reset_state(with_data=False)

    car_name, service_name, price = await CarService.get_result_by_id(id=car_service_id)

    await call.message.edit_text(f"Автомобиль: {car_name}\nУслуга: {service_name}\n\nЦена: {price}",
                                 reply_markup=create_order_keyboard())


@dp.callback_query_handler(order_get_full_name.filter(), state='*')
async def bot_order_get_full_name_callback(call: CallbackQuery, callback_data: dict):
    await OrderState.full_name.set()

    await call.message.edit_text("Пришлите полное имя")


@dp.message_handler(state=OrderState.full_name)
async def bot_order_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await OrderState.phone.set()

    await message.answer("Пришлите номер телефона", reply_markup=request_phone)


@dp.message_handler(content_types=['contact'], state=OrderState.phone)
async def bot_order_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    data = await state.get_data()
    await state.reset_state(with_data=True)

    car_service = await CarService.get(id=data['car_service_id'])
    Order.create(user_id=message.from_user.id, car_service_id=car_service.id, price=car_service.price,
                 full_name=data['full_name'], phone=data['phone'])

    car_name, service_name, price = await CarService.get_result_by_id(id=car_service.id)

    text = f"Новая запись от пользователя {data['full_name']}\nНомер телефона: {data['phone']}\n\nАвтомобиль: {car_name}\nУслуга: {service_name}\n\nЦена: {price}"
    for user_id in ADMINS:
        try:
            await dp.bot.send_message(chat_id=user_id, text=text)
        except BotBlocked:
            pass

    await message.answer("Ваша запись подтвердится по телефону, ожидайте!", reply_markup=menu_keyboard)
