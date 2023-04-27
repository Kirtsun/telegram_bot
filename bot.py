import telebot
import time
from telebot import types
import requests
import os

from dotenv import load_dotenv

load_dotenv()

key = os.getenv('API')

bot = telebot.TeleBot(os.getenv('API'))


@bot.message_handler(commands=['start'])
def start(massage):
    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/pars')
    btn2 = types.KeyboardButton('/currency')
    murkup.row(btn1, btn2)
    bot.send_message(massage.chat.id, f'{massage.from_user.first_name}, Привет! Это тестовый бот, он пока что ничего не умеет кроме этого!'
                     f'но он еще обучается! Думаю в скором времени он будет уметь гораздо больше.', reply_markup=murkup)


@bot.message_handler(commands=['pars'])
def pars(massage):
    file = open('./photo.jpeg', 'rb')
    bot.send_photo(massage.chat.id, file)


@bot.message_handler(commands=['currency'])
def currency(massage):
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
        bot.send_message(massage.chat.id, f'Курс Валют на сегодня.\n\nUSD 🇺🇸 Покупка: {buy_usd} - Продажа {sell_usd}\n\n'
                                          f'EUR 🇪🇺 Покупка: {buy_eur} - Продажа {sell_eur}')
    else:
        bot.send_message(massage.chat.id, f'Что-то пошло не так, попробуй позже')


if __name__ == '__main__':
    bot.polling(none_stop=True)
