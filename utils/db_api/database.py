from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.exceptions import BotBlocked
from gino import Gino
from sqlalchemy import Column, Integer, String, Index, Sequence, ForeignKey, Float, and_
from sqlalchemy import sql
from sqlalchemy.exc import InvalidRequestError

from data.config import DATABASE_URL

database = Gino()


class BaseModel(database.Model):
    query: sql.Select

    @classmethod
    async def filter(cls, id: int):
        return await cls.query.where(cls.id == id).gino.all()

    @classmethod
    async def all(cls):
        return await cls.query.gino.all()

    @classmethod
    async def get(cls, id: int):
        return await cls.query.where(cls.id == id).gino.first()

    @classmethod
    async def get_or_create(cls, **kwargs):
        obj = None
        if 'id' in kwargs:
            obj = await cls.get(kwargs.get('id'))
        if not obj:
            obj = await cls.create(**kwargs)
        return obj

    @classmethod
    async def count(cls) -> int:
        return await database.func.count(cls.id).gino.scalar()


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    first_name = Column(String(128))
    username = Column(String(128))

    _idx = Index('user_id_index', 'id')

    @staticmethod
    async def mailing(bot: Bot, text: str, keyboard: InlineKeyboardMarkup = None) -> int:
        count_users = 0
        for user in await User.query.gino.all():
            try:
                await bot.send_message(chat_id=user.id, text=text, reply_markup=keyboard)
                count_users += 1
            except BotBlocked:
                pass
        return count_users


class Car(BaseModel):
    __tablename__ = 'cars'

    id = Column(Integer, Sequence('car_id_seq'), primary_key=True)
    name = Column(String(32))

    _idx = Index('car_id_index', 'id')


class Service(BaseModel):
    __tablename__ = 'services'

    id = Column(Integer, Sequence('services_id_seq'), primary_key=True)
    name = Column(String(60))

    _idx = Index('services_id_index', 'id')


class CarService(BaseModel):
    __tablename__ = 'car_services'

    id = Column(Integer, Sequence('car_services_id_seq'), primary_key=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    price = Column(Float)

    _idx = Index('car_services_id_index', 'id')

    @staticmethod
    async def for_car(car_id: int):
        return [
            (car_service[0], car_service[-1]) for car_service in await CarService.join(Service).select().where(CarService.car_id == car_id).gino.all()
        ]

    @staticmethod
    async def get_result_by_id(id: int):
        car_service = await CarService.join(Car).join(Service).select().where(CarService.id == id).gino.first()
        return car_service[5], car_service[7], car_service[3]


class Order(BaseModel):
    __tablename__ = 'orders'

    id = Column(Integer, Sequence('orders_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    car_service_id = Column(Integer, ForeignKey('car_services.id'))
    price = Column(Float)

    full_name = Column(String(64))
    phone = Column(String(12))

    _idx = Index('orders_id_index', 'id')


async def create_database():
    await database.set_bind(DATABASE_URL)
    try:
        await database.gino.create_all()
    except InvalidRequestError:
        pass
