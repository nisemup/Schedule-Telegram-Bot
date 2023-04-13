import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware, BaseMiddleware
from aiogram.utils.exceptions import Throttled

from .database import Database

logger = logging.getLogger(__name__)


class DbMiddleware(LifetimeControllerMiddleware):
    __skip_patterns = ["error", "update"]

    def __init__(self, pool):
        super().__init__()
        self.__pool = pool

    async def pre_process(self, obj, data, *args):
        db = await self.__pool.acquire()
        data["db"] = db
        data["data"] = Database(db)

    async def post_process(self, obj, data, *args):
        del data["data"]
        db = data.get("db")
        if db:
            await self.__pool.release(db)


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = DEFAULT_RATE_LIMIT, key_prefix: str = 'antiflood_'):
        self.__rate_limit = limit
        self.__prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.__rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.__prefix}_{handler.__name__}")
        else:
            limit = self.__rate_limit
            key = f"{self.__prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        handler = current_handler.get()
        limit = getattr(handler, 'throttling_rate_limit', self.__rate_limit)
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count <= 2:
            logger.warning(f'User {message.from_user.id} spamming')
        await asyncio.sleep(delta)
