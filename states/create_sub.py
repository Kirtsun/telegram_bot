from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateSub(StatesGroup):
    user_name = State()
