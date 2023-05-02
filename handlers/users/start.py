import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db
from states.user_form import UserForm


@dp.message_handler(text='/start')
async def start(message: types.Message):
    check_user = db.check_user_in_db(message.from_user.id)
    if check_user is True:
        check_sub = db.check_sub_status(message.from_user.id)
        if check_sub is True:
            murkup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton('Очень интересная функция')
            btn2 = types.KeyboardButton('Курс валют')
            murkup.row(btn1, btn2)
            await message.answer(f'Привет! Это тестовый бот, он пока что ничего не умеет кроме этого!'
                                 f' Но он еще обучается! Думаю в скором времени он будет уметь гораздо больше.',
                                 reply_markup=murkup)
        else:
            await message.answer(f'Подписка не оформлена. Обратитесь к администратору -> @kyrtsun')
    else:
        await UserForm.name.set()
        await message.answer(f'Добрый день! Добро пожаловать в наш бот. Для регистрации введите свое имя.')


@dp.message_handler(text=['/stop'], state='*')
async def stop(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Регистрация завершина. Для новой регистрации нажми -> /start')


@dp.message_handler(state=UserForm.name)
async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await UserForm.next()
    await message.answer('Укажите Вашу почту.')


@dp.message_handler(state=UserForm.email)
async def email(message: types.Message, state: FSMContext):
    if len(message.text.split('@')) == 2:
        async with state.proxy() as data:
            data['email'] = message.text
            data_to_save = {
                'pk_in_bot': message.from_user.id,
                'name': data['name'],
                'user_name': message.from_user.first_name,
                'email': data['email']
            }
            create = db.create_user(data_to_save)
            if create is True:
                await state.finish()
                await message.answer('Регистрация прошла успешно. Для оформления подписки обратитесь'
                                     ' к администратору -> @kyrtsun')
            else:
                await message.answer('Что то не так c сохранением, перезапустите бота')
    else:
        await message.answer('Что-то не так написано, проверьте правильность ввода.')


@dp.message_handler(text=['message'])
async def massage(message: types.Message):
    await message.answer(message)

