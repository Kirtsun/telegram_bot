from utils.set_bot_commands import set_commands
from utils.notyfi import admin
from handlers.users import dp
from aiogram import executor
from loader import db


async def on_start(disp):
    await admin(dp)
    await set_commands(disp)


if __name__ == '__main__':
    db.create_table()
    executor.start_polling(dp, on_startup=on_start)
