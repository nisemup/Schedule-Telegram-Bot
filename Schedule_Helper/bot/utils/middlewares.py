from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from .database import Database


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    async def pre_process(self, obj, data, *args):
        db = await self.pool.acquire()
        data["db"] = db
        data["data"] = Database(db)

    async def post_process(self, obj, data, *args):
        del data["data"]
        db = data.get("db")
        if db:
            await self.pool.release(db)
