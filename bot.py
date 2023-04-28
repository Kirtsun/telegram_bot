from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv
from pars import get_currency

load_dotenv()


async def start(massage: types.Message):
    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Очень интересная функция')
    btn2 = types.KeyboardButton('Курс валют')
    murkup.row(btn1, btn2)
    await massage.answer(f'{massage.from_user.first_name}, Привет! Это тестовый бот, он пока что ничего'
                                      f' не умеет кроме этого! Но он еще обучается! Думаю в скором времени он будет '
                                      f'уметь гораздо больше.', reply_markup=murkup)


async def pars(massage: types.Message):
    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Курс валют')
    murkup.row(btn1)
    file = open('./photo.jpeg', 'rb')
    await massage.answer_photo(file, caption='А что ты думал, так быстро все будет? Нифига, я ток учу это все!',
                               reply_markup=murkup)


async def currency(massage: types.Message):
    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Очень интересная функция')
    murkup.row(btn1)
    res = get_currency()
    if res is not False:
        await massage.answer(f'Курс валют на сегодня согласно данным MonoBank.\n\nUSD 🇺🇸'
                                              f' Покупка: {res["USD"][0]} - Продажа {res["USD"][1]}\n\n'
                                              f'EUR 🇪🇺 Покупка: {res["EUR"][0]} - Продажа {res["EUR"][1]}',
                             reply_markup=murkup)
    else:
        await massage.answer(f'Что-то пошло не так, попробуй через 2-3 минуточки. Спасибо ☺️')


async def handler_command(massage: types.Message):
    text = massage.text.lower().lower()
    if text == 'курс валют':
        await currency(massage)
    elif text == 'очень интересная функция':
        await pars(massage)
    else:
        await massage.answer(f'Что не то ввел фраерок, давай ка еще разок!')


if __name__ == '__main__':
    dp = Dispatcher(Bot(os.getenv('API')))
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(pars, commands=['pars'])
    dp.register_message_handler(handler_command)
    executor.start_polling(dp)
