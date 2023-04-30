from aiogram import types

from loader import dp
from pars import get_currency


@dp.message_handler(commands=['currency'])
async def currency(massage: types.Message):
    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Очень интересная функция')
    btn2 = types.KeyboardButton('А ну ка обнови курс валют!')
    murkup.row(btn1, btn2)
    res = get_currency()
    if res is not False:
        await massage.answer(f'Курс валют на сегодня согласно данным MonoBank.\n\nUSD 🇺🇸'
                                              f' Покупка: {res["USD"][0]} - Продажа {res["USD"][1]}\n\n'
                                              f'EUR 🇪🇺 Покупка: {res["EUR"][0]} - Продажа {res["EUR"][1]}',
                             reply_markup=murkup)
    else:
        await massage.answer(f'Что-то пошло не так, попробуй через 2-3 минуточки. Спасибо ☺️')
