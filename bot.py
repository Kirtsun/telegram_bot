from aiogram import Bot, Dispatcher, executor, types
import requests
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(os.getenv('API'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(massage: types.Message):
    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/pars')
    btn2 = types.KeyboardButton('/currency')
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
    USD = 840
    EUR = 978
    r = requests.get(url='https://api.monobank.ua/bank/currency')
    if r.status_code == 200:
        res = r.json()
        for i in res:
            if i['currencyCodeA'] == USD:
                buy_usd = i['rateBuy']
                sell_usd = i['rateSell']
            elif i['currencyCodeA'] == EUR and i['currencyCodeB'] == 980:
                buy_eur = i['rateBuy']
                sell_eur = i['rateSell']
        await massage.answer(f'Курс валют на сегодня согласно данным MonoBank.\n\nUSD 🇺🇸'
                                          f' Покупка: {buy_usd} - Продажа {sell_usd}\n\n'
                                          f'EUR 🇪🇺 Покупка: {buy_eur} - Продажа {sell_eur}', reply_markup=murkup)
    else:
        await massage.answer(f'Что-то пошло не так, попробуй через 2-3 минуточки, API MonoBank не дает'
                                          f' часто обновлять запрос. Спасибо ☺️')


if __name__ == '__main__':
    executor.start_polling(dp)
