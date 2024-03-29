import asyncio
import os
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import exceptions
from dotenv import load_dotenv

from ..language import uk_UA as t
from ..loader import bot, BASE_DIR
from ..utils import keyboard as key
from ..utils.database import Database

load_dotenv(BASE_DIR / "settings" / ".env")


class AdminMenu(StatesGroup):
    menu_selection = State()
    mailing_menu = State()
    confirm_menu = State()


async def cmd_admin(message: types.Message, state: FSMContext):
    if message.chat.id == int(os.getenv("MAIN_ADMIN")):
        await message.answer(t.a_hi, reply_markup=key.admin())
        await AdminMenu.menu_selection.set()
    else:
        await state.finish()
        return


async def menu(message: types.Message):
    if message.text == t.b_newsletter:
        await message.answer(t.a_newsletter)
        await AdminMenu.mailing_menu.set()
    else:
        await message.answer(t.error_text)
        return


async def newsletter(message: types.Message, state: FSMContext):
    await message.answer(message.text, reply_markup=key.send_news())
    await state.update_data(text=message.text)
    await AdminMenu.confirm_menu.set()


async def confirm_send(message: types.Message, state: FSMContext, data: Database):
    if message.text != t.b_send_news:
        await message.answer(t.error_text)
        return

    fsm_data = await state.get_data()
    users = await data.get_uids_notif()

    async def send_message(user_id, text):
        try:
            await bot.send_message(user_id, text)
            await asyncio.sleep(0.3)
        except exceptions.BotBlocked:
            pass
        except Exception as ex:
            logging.error(f"Error while sending message to user {user_id}: {ex}")

    tasks = [send_message(user, fsm_data['text']) for user in users]

    await asyncio.gather(*tasks)

    await message.answer(t.hi_text, reply_markup=key.main_menu(message.chat.id))
    await state.finish()


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(cmd_admin, Text(equals=t.b_admin, ignore_case=True), state="*")
    dp.register_message_handler(menu, state=AdminMenu.menu_selection)
    dp.register_message_handler(newsletter, state=AdminMenu.mailing_menu)
    dp.register_message_handler(confirm_send, state=AdminMenu.confirm_menu)
