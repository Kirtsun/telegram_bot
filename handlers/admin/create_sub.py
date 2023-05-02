import time

from loader import dp, db
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.create_sub import CreateSub
from aiogram.dispatcher.filters import Text

admins = [465659759]


@dp.message_handler(Text(equals='/set_sub'))
async def set_sub(message: types.Message):
    if message.from_user.id in admins:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        btn1 = types.KeyboardButton('30 days', )
        btn2 = types.KeyboardButton('60 days')
        markup.row(btn1, btn2)
        await message.answer('Выберити подписку. Для отмены оформления выполните команду /cancel', reply_markup=markup)
    else:
        await message.answer('У вас нет прав для этой функции. Обратитесь к админу -> @Kyrtsun')


@dp.message_handler(text='/cancel', state='*')
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие отменено. Возвращаемся в начальное состояние.')


@dp.message_handler(text='30 days')
async def thirty_day(message: types.Message):
    await message.answer(f'Вы выбрали подписку 30 дней.\nВведите ник пользователя для проверки его в регистрации.\n'
                         f'Для отмены оформления выполните команду /cancel')
    await CreateSub.user_name.set()


@dp.message_handler(state=CreateSub.user_name)
async def add_sub_time(message: types.Message, state: FSMContext):
    res = db.get_user_name(message.text)
    if res is True:
        await state.finish()
        times = (30 * 24 * 60 * 60) + time.time()
        update_sub = db.update_sub(message.text, int(times))
        if update_sub is True:
            await message.answer('Подписка оформлена!')
        else:
            await message.answer('Ошибка дабавления подписки, проверьте подключение к базе')
    else:
        await message.answer('Пользолватель не найден')


# @dp.message_handler(text='/cancel', state='*')
# async def cancel(message: types.Message, state: FSMContext):
#     # current_state = await state.get_state()
#     # if current_state is None:
#     #     return
#
#     await state.finish()
#     await message.answer('Действие отменено. Возвращаемся в начальное состояние.')



