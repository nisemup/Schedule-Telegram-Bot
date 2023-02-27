import asyncio
import asyncpg
import logging
import uvicorn
import os

from bot.handlers.admin import register_handlers_admin
from bot.handlers.settings import register_handlers_settings
from bot.handlers.common import register_handlers_common
from bot.handlers.timetable import register_handlers_timetable
from bot.utils.middlewares import DbMiddleware

from multiprocessing import Process
from pathlib import Path
from bot import loader as load
from aiogram import Bot, Dispatcher, executor, types
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    datefmt="%H:%M:%S",
    format="[%(asctime)s] %(levelname)s | %(module)s-%(funcName)s (%(lineno)d): %(message)s"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

load_dotenv(BASE_DIR / "settings" / ".env")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


class MyBot:
    dp = load.dp
    Dispatcher.set_current(load.dp)

    @classmethod
    def run(cls):
        executor.start_polling(cls.dp, on_startup=cls.on_startup, on_shutdown=cls.on_shutdown)

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
        register_handlers_common(dp)
        register_handlers_settings(dp)
        register_handlers_timetable(dp)
        register_handlers_admin(dp)

    @staticmethod
    async def on_shutdown(dp: Dispatcher):
        await dp.storage.close()
        await dp.storage.wait_closed()


class MyServer:
    app = get_asgi_application()

    config = uvicorn.Config(app=app, loop=loop, port=8000, host="0.0.0.0")
    server = uvicorn.Server(config=config)

    @classmethod
    def run(cls):
        asyncio.run(cls.on_startup())
        asyncio.run(cls.server.serve())
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
