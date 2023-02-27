from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from .utils.database import Database
from pathlib import Path
import asyncio
import os


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "settings" / ".env")

# storage = MongoStorage(host='localhost', port=27017, db_name='aiogram_fsm')
storage = RedisStorage2('localhost', 6379, db=5, pool_size=10, prefix='my_fsm_key')

bot = Bot(token=os.getenv('BOT_API_TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


async def set_commands():
    commands = [
        BotCommand(command="/cancel", description="Скасування будь-якої дії.")
    ]
    await bot.set_my_commands(commands)
