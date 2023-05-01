import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db
from states.user_form import UserForm


# def days(day):
#     return day * 24 * 60 * 60


@dp.message_handler(text='/start')
async def start(massage: types.Message):
    check_user = db.check_user_in_db(massage.from_user.id)
    if check_user is True:
        check_sub = db.check_sub_status(massage.from_user.id)
        if check_sub is True:
            murkup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton('Очень интересная функция')
            btn2 = types.KeyboardButton('Курс валют')
            murkup.row(btn1, btn2)
            await massage.answer(f'Привет! Это тестовый бот, он пока что ничего не умеет кроме этого!'
                                 f' Но он еще обучается! Думаю в скором времени он будет уметь гораздо больше.',
                                 reply_markup=murkup)
        else:
            await massage.answer(f'Подписка не оформлена. Обратитесь к администратору -> @kyrtsun')
    else:
        await UserForm.name.set()
        await massage.answer(f'Добрый день! Добро пожаловать в наш бот. Для регистрации введите свое имя.'
                             f'Если хотите отменить регистрацию, выполните команду "/stop"')


@dp.message_handler(state=UserForm.name)
async def name(massage: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = massage.text
    await UserForm.next()
    await massage.answer('Укажите Вашу почту.')


@dp.message_handler(state=UserForm.email)
async def email(massage: types.Message, state: FSMContext):
    if len(massage.text.split('@')) == 2:
        async with state.proxy() as data:
            data['email'] = massage.text
            data_to_save = {
                'pk_in_bot': massage.from_user.id,
                'name': data['name'],
                'user_name': massage.from_user.username,
                'email': data['email']
            }
            create = db.create_user(data_to_save)
            if create is True:
                await state.finish()
                await massage.answer('Регистрация прошла успешно. Для оформления подписки обратитесь'
                                     ' к администратору -> @kyrtsun')
            else:
                await massage.answer('Что то не так c сохранением, перезапустите бота')
    else:
        await massage.answer('Что-то не так написано, проверьте правильность ввода.')


@dp.message_handler(text=['/add_sub_time'])
async def subscription():
    """ Нужно написать стейты для добаления, сделать проверку входит ли автор этого всего в админы, после вызова команды
    запускаються стейты. Делаем это все в отдельной папке для админов. Еще так же дабавляем функционал как базе данных
    для добавления подписки беру int(time.time() + func(указываем количество дней). func - функция для преобразования
    дней в секунды.)"""
    pass


@dp.message_handler(text=['massages'])
async def massage(massage: types.Message):
    await massage.answer(massage)


