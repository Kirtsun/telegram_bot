from aiogram import types
from aiogram.dispatcher import FSMContext

from db import check_user_in_db, create_user
from loader import dp
from states.user_form import UserForm


@dp.message_handler(text='/start')
async def start(massage: types.Message):
    check_user = check_user_in_db(massage.from_user.id)
    if check_user is True:
        murkup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Очень интересная функция')
        btn2 = types.KeyboardButton('Курс валют')
        murkup.row(btn1, btn2)
        await massage.answer(f'Привет! Это тестовый бот, он пока что ничего не умеет кроме этого! Но он еще обучается!'
                             f' Думаю в скором времени он будет уметь гораздо больше.', reply_markup=murkup)
    else:
        await UserForm.name.set()
        await massage.answer(f'О, новенький, давай знакомиться. Введи свое имя)')


@dp.message_handler(state=UserForm.name)
async def name(massage: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = massage.text
    await UserForm.next()
    await massage.answer('Укажи свою почту.')


@dp.message_handler(state=UserForm.email)
async def email(massage: types.Message, state: FSMContext):
    if len(massage.text.split('@')) == 2:
        async with state.proxy() as data:
            data['email'] = massage.text
            data_to_save = {
                'pk_in_bot': massage.from_user.id,
                'name': data['name'],
                'email': data['email']
            }
            create = create_user(data_to_save)
            if create is True:
                await state.finish()
                await massage.answer('Регистрация прошла успешно. Пока есть одна команда "/currency"')
                await start(massage)
            else:
                await massage.answer('Что то не так c сохранением, перезапусти базу')
    else:
        await massage.answer('Что-то не так написано, проверь и давай еще раз.')


@dp.message_handler(commands='pars')
async def pars(massage: types.Message):
    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Курс валют')
    murkup.row(btn1)
    file = open('./photo.jpeg', 'rb')
    await massage.answer_photo(file, caption='А что ты думал, так быстро все будет? Нифига, я ток учу это все!',
                               reply_markup=murkup)
