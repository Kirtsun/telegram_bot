from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv
from pars import get_currency

load_dotenv()

bot = Bot(os.getenv('API'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(massage: types.Message):
    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/pars')
    btn2 = types.KeyboardButton('Курс валют')
    murkup.row(btn1, btn2)
    await massage.answer(f'{massage.from_user.first_name}, Привет! Это тестовый бот, он пока что ничего'
                                      f' не умеет кроме этого! Но он еще обучается! Думаю в скором времени он будет '
                                      f'уметь гораздо больше.', reply_markup=murkup)


@dp.message_handler(commands=['pars'])
async def pars(massage: types.Message):
    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/currency')
    murkup.row(btn1)
    file = open('./photo.jpeg', 'rb')
    await massage.answer_photo(file, reply_markup=murkup)


@dp.message_handler(commands=['currency'])
async def currency(massage: types.Message):

    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/pars')
    murkup.row(btn1)
    res = get_currency()
    if res is not False:
        await massage.answer(f'Курс валют на сегодня согласно данным MonoBank.\n\nUSD 🇺🇸'
                                              f' Покупка: {res["USD"][0]} - Продажа {res["USD"][1]}\n\n'
                                              f'EUR 🇪🇺 Покупка: {res["EUR"][0]} - Продажа {res["EUR"][1]}', reply_markup=murkup)
    else:
        await massage.answer(f'Что-то пошло не так, попробуй через 2-3 минуточки. Спасибо ☺️')


if __name__ == '__main__':
    executor.start_polling(dp)
