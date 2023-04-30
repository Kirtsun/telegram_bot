from aiogram.dispatcher.filters.state import StatesGroup, State


class UserForm(StatesGroup):
    name = State()
    email = State()
