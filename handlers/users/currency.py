from aiogram import types

from loader import dp, db
from requests_to_web.requests_currency import get_currency


@dp.message_handler(text=['/currency', 'курс валют', 'А ну ка обнови курс валют!', 'Курс валют'])
async def currency(massage: types.Message):
    if db.check_sub_status(massage.from_user.id):
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
    else:
        await massage.answer(f'Подписка не оформлена. Обратись к администратору -> @kyrtsun')