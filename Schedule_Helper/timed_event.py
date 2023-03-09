import asyncio
import logging
import asyncpg
import aiogram
import os
import sys
from datetime import datetime, timedelta
from bot.loader import dp
from bot.utils.middlewares import DbMiddleware
from bot.utils.database import Database
from bot.language import uk_UA as t
from bot.loader import bot
from bot.utils.utils import get_week_type, create_schedule, create_pre, days


async def on_startup():
    pool = await asyncpg.create_pool(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    await main(sys.argv, Database(pool))


async def main(argv, data: Database):
    date = datetime.now()
    date = datetime.weekday((date + timedelta(days=1))) if argv[1] == 'pre' else datetime.weekday(date)
    date = days[date]

    users = await data.get_uids_notif()
    for user in users:
        gid = await data.get_group(user)
        raw = await data.get_day(gid, date, get_week_type())
        if raw:
            schedule = create_pre(raw) if argv[1] == 'pre' else t.hi + create_schedule(raw)[raw[0][0]] + t.form_footer
            try:
                await bot.send_message(user, schedule, disable_web_page_preview=True)
            except aiogram.utils.exceptions.BotBlocked:
                logging.info(f"А user {user} the blocked bot!")
                continue
            await asyncio.sleep(0.3)
    logging.info("Mailing completed successfully!")

asyncio.get_event_loop().run_until_complete(on_startup())
