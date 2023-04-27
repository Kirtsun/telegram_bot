import telebot

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
    murkup.row(btn1)
    bot.send_message(massage.chat.id, f'{massage.from_user.first_name}, Привет! Это тестовый бот, он пока что ничего не умеет кроме этого!'
                     f'но он еще обучается! Думаю в скором времени он будет уметь гораздо больше.', reply_markup=murkup)
    bot.register_next_step_handler(massage, pars)


def pars(massage):
    if massage.text == '/pars':
        murkup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('/start')
        murkup.row(btn1)
        file = open('./photo.jpeg', 'rb')
        bot.send_photo(massage.chat.id, file, reply_markup=murkup)
        bot.register_next_step_handler(massage, start)


if __name__ == '__main__':
    bot.polling(none_stop=True)
