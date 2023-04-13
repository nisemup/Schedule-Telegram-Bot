import asyncio
import logging
import os
from multiprocessing import Process
from pathlib import Path

import asyncpg
import uvicorn
from aiogram import Dispatcher, executor
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

from bot import loader as load
from bot.handlers.admin import register_handler_admin
from bot.handlers.common import register_handler_common
from bot.handlers.settings import register_handler_settings
from bot.handlers.timetable import register_handler_timetable
from bot.utils.middlewares import DbMiddleware, ThrottlingMiddleware

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "settings" / ".env")

logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") == 'True' else logging.INFO,
    filename="logs.log",
    datefmt="%H:%M:%S",
    format="[%(asctime)s] %(levelname)s | %(module)s-%(funcName)s (%(lineno)d): %(message)s"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


class MyBot:
    __dp = load.dp
    Dispatcher.set_current(load.dp)

    @classmethod
    def run(cls):
        executor.start_polling(cls.__dp, on_startup=cls.on_startup, on_shutdown=cls.on_shutdown)

    @staticmethod
    async def on_startup(dp: Dispatcher):
        await load.set_commands()

        pool = await asyncpg.create_pool(
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )

        dp.middleware.setup(DbMiddleware(pool))
        dp.middleware.setup(ThrottlingMiddleware())

        register_handler_common(dp)
        register_handler_settings(dp)
        register_handler_timetable(dp)
        register_handler_admin(dp)

    @staticmethod
    async def on_shutdown(dp: Dispatcher):
        await dp.storage.close()
        await dp.storage.wait_closed()


class MyServer:
    __app = get_asgi_application()

    __config = uvicorn.Config(app=__app, loop=loop, port=8000, host="0.0.0.0")
    __server = uvicorn.Server(config=__config)

    @classmethod
    def run(cls):
        asyncio.run(cls.on_startup())
        asyncio.run(cls.__server.serve())
        asyncio.run(cls.on_shutdown())

    @staticmethod
    async def on_startup() -> None:
        pass

    @staticmethod
    async def on_shutdown() -> None:
        pass


def run_app():
    bot = Process(target=MyBot.run)
    server = Process(target=MyServer.run)

    server.start()
    bot.start()


if __name__ == "__main__":
    run_app()
