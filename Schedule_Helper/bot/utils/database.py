import asyncpg
import os
import asyncio
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "settings" / ".env")


class Database:
    def __init__(self, conn):
        self.conn: asyncpg.connection = conn

    async def get_faculty(self):
        sql = """SELECT DISTINCT faculty FROM backend_groups"""
        return sorted([key[0] for key in await self.conn.fetch(sql)])

    async def get_gnum(self, faculty):
        sql = """SELECT gnum FROM backend_groups WHERE faculty = $1"""
        return sorted([key[0] for key in await self.conn.fetch(sql, faculty)])

    async def get_gid(self, faculty, gnum):
        sql = """SELECT gid FROM backend_groups WHERE faculty = $1 AND gnum = $2"""
        return await self.conn.fetchval(sql, faculty, int(gnum))

    async def create_user(self, uid, gid, username=None):
        sql = """
            INSERT INTO backend_profiles (user_id, username, group_id, notification)
            VALUES ($1, $2, $3, True)
            ON CONFLICT (user_id)
            DO UPDATE SET
                username = EXCLUDED.username,
                group_id = EXCLUDED.group_id;
        """
        await self.conn.execute(sql, int(uid), username, gid)
        return True

    async def get_admins(self):
        sql = """SELECT user_id FROM backend_profiles WHERE is_admin = True"""
        return [key[0] for key in await self.conn.fetch(sql)]

    async def get_moderators(self):
        sql = """SELECT user_id FROM backend_profiles WHERE is_moderator = True"""
        return [key[0] for key in await self.conn.fetch(sql)]

    async def get_notification(self, uid):
        sql = """SELECT notification FROM backend_profiles WHERE user_id = $1"""
        return await self.conn.fetchval(sql, int(uid))

    async def update_notification(self, uid, data):
        state = False if data else True
        sql = """UPDATE backend_profiles SET notification = $1 WHERE user_id = $2"""
        await self.conn.execute(sql, state, int(uid))
        return True

    async def get_group(self, uid):
        sql = """SELECT group_id FROM backend_profiles WHERE user_id = $1"""
        return await self.conn.fetchval(sql, int(uid))

    async def get_schedule(self, gid, week_type):
        sql = """
            SELECT day, number, name, start_time, end_time, classroom, url
            FROM backend_schedule WHERE group_id = $1 AND week_type = $2
        """
        return await self.conn.fetch(sql, gid, week_type)

    async def get_day(self, gid, day, week):
        sql = """
            SELECT day, number, name, start_time, end_time, classroom, url
            FROM backend_schedule WHERE group_id = $1 AND week_type = $2 AND day = $3
        """
        return await self.conn.fetch(sql, gid, week, day.lower())

    async def get_uids_notif(self):
        sql = """SELECT user_id FROM backend_profiles WHERE notification = True"""
        return [key[0] for key in await self.conn.fetch(sql)]
