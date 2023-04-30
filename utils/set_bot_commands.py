from aiogram import types


async def set_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand(command='/start', description='Начало всего'),
        types.BotCommand(command='/currency', description="курс валют"),
    ])
