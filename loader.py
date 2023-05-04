import redis
from aiogram import Bot, Dispatcher, types
import os
from aiogram.contrib.fsm_storage.redis import RedisStorage2
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from data.db import DataBase

load_dotenv()

bot = Bot(os.getenv('API'), parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(
    host='redis',
    port=6379,
    db=0
)

dp = Dispatcher(bot, storage=storage)
db = DataBase()
