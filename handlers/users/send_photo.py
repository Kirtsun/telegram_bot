from aiogram import types

from loader import dp, db


@dp.message_handler(text=['/pars', 'Очень интересная функция'])
async def pars(massage: types.Message):
    if db.check_sub_status(massage.from_user.id):
        murkup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Курс валют')
        murkup.row(btn1)
        file = open('data/photo/photo.jpeg', 'rb')
        await massage.answer_photo(file, caption='А что ты думал, так быстро все будет? Нифига, я ток учу это все!',
                                   reply_markup=murkup)
    else:
        await massage.answer(f'Подписка не оформлена. Обратись к администратору -> @kyrtsun')
