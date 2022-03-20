from aiogram.utils.callback_data import CallbackData

order = CallbackData("order")
order_select_car = CallbackData("order_select_car", "car_id")
order_select_car_service = CallbackData("order_select_car_service", "car_service_id")
order_get_full_name = CallbackData("order_get_full_name")
