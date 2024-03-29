from pathlib import Path

import asyncpg
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "settings" / ".env")


class Database:
    def __init__(self, connect):
        self.__connect: asyncpg.connection = connect

    async def get_faculty(self) -> list[str]:
        sql = """SELECT DISTINCT faculty FROM backend_groups"""
        return sorted([key[0] for key in await self.__connect.fetch(sql)])

    async def get_gnum(self, faculty: str) -> list[str]:
        sql = """SELECT gnum FROM backend_groups WHERE faculty = $1"""
        return sorted([key[0] for key in await self.__connect.fetch(sql, faculty)])

    async def get_gid(self, faculty: str, gnum: str) -> str:
        sql = """SELECT gid FROM backend_groups WHERE faculty = $1 AND gnum = $2"""
        return await self.__connect.fetchval(sql, faculty, int(gnum))

    async def create_user(self, uid: str, gid: str, username: str = None) -> bool:
        sql = """
            INSERT INTO backend_profiles (user_id, username, group_id, notification)
            VALUES ($1, $2, $3, True)
            ON CONFLICT (user_id)
            DO UPDATE SET
                username = EXCLUDED.username,
                group_id = EXCLUDED.group_id;
        """
        await self.__connect.execute(sql, int(uid), username, gid)
        return True

    async def get_admins(self) -> list[str]:
        sql = """SELECT user_id FROM backend_profiles WHERE is_admin = True"""
        return [key[0] for key in await self.__connect.fetch(sql)]

    async def get_moderators(self) -> list[str]:
        sql = """SELECT user_id FROM backend_profiles WHERE is_moderator = True"""
        return [key[0] for key in await self.__connect.fetch(sql)]

    async def get_notification(self, uid: str) -> bool:
        sql = """SELECT notification FROM backend_profiles WHERE user_id = $1"""
        return await self.__connect.fetchval(sql, int(uid))

    async def update_notification(self, uid: str, data: bool) -> bool:
        state = False if data else True
        sql = """UPDATE backend_profiles SET notification = $1 WHERE user_id = $2"""
        await self.__connect.execute(sql, state, int(uid))
        return True

    async def get_group(self, uid: str) -> str:
        sql = """SELECT group_id FROM backend_profiles WHERE user_id = $1"""
        return await self.__connect.fetchval(sql, int(uid))

    async def get_schedule(self, gid: str, week_type: str) -> list[str]:
        sql = """
            SELECT day, number, name, start_time, end_time, classroom, url
            FROM backend_schedule WHERE group_id = $1 AND week_type = $2
        """
        return await self.__connect.fetch(sql, gid, week_type)

    async def get_day(self, gid: str, day: str, week: str) -> list[str]:
        sql = """
            SELECT day, number, name, start_time, end_time, classroom, url
            FROM backend_schedule WHERE group_id = $1 AND week_type = $2 AND day = $3
        """
        return await self.__connect.fetch(sql, gid, week, day.lower())

    async def get_uids_notif(self) -> list[str]:
        sql = """SELECT user_id FROM backend_profiles WHERE notification = True"""
        return [key[0] for key in await self.__connect.fetch(sql)]

    async def get_week_reverse(self, gid: str) -> bool:
        sql = """SELECT week_reverse FROM backend_groups WHERE gid = $1"""
        return await self.__connect.fetchval(sql, gid)

    async def add_count(self, user: str, button: str) -> bool:
        sql = """
            INSERT INTO backend_stats (user_id, button_name, count)
            VALUES ($1, $2, 1)
            ON CONFLICT (user_id, button_name)
            DO UPDATE SET
                count = backend_stats.count+1;
        """
        return await self.__connect.execute(sql, user, button)
