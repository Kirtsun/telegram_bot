from aiogram import Bot, Dispatcher, types
import os
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from dotenv import load_dotenv


load_dotenv()

bot = Bot(os.getenv('API'), parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(
    host='localhost',
    port=6379,
    db=1
)

dp = Dispatcher(bot)
