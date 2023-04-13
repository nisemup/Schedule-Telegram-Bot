from os import getenv
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import BotCommand
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "settings" / ".env")

storage = MemoryStorage() if getenv('DEBUG') == 'True' else RedisStorage2('localhost', 6379, db=5, pool_size=10, prefix='my_fsm_key')

bot = Bot(token=getenv('BOT_API_TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


async def set_commands():
    commands = [
        BotCommand(command="/cancel", description="Скасування будь-якої дії.")
    ]
    await bot.set_my_commands(commands)
