import logging

from aiogram import Dispatcher


async def admin(dp: Dispatcher):
    text = 'Bot ready to work'
    await dp.bot.send_message(chat_id=465659759, text=text)
