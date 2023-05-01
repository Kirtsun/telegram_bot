from aiogram import types

from loader import dp


@dp.message_handler()
async def unknown_command(massage: types.Message):
    await massage.answer(f'Что-то не введено, давай попробуем еще раз.')

