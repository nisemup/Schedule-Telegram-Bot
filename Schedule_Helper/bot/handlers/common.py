from ..utils import keyboard as key
from ..utils.database import Database
from ..language import uk_UA as t
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup


class StartHandler(StatesGroup):
    faculty_selection = State()
    user_register = State()


async def start(message: types.Message, state: FSMContext, data: Database):
    await state.finish()
    username = message.from_user.username if message.from_user.username else None
    await state.update_data(username=username)
    faculty = await data.get_faculty()
    await message.answer(t.faculty_message, reply_markup=key.inline_choose(faculty))
    await StartHandler.faculty_selection.set()


async def cb_faculty(call: types.CallbackQuery, state: FSMContext, data: Database):
    await state.update_data(faculty=call.data)
    gnum = await data.get_gnum(call.data)
    await call.message.edit_text(t.faculty_confirm + call.data)
    await call.message.answer(t.group_message,
                              reply_markup=key.inline_choose(gnum))
    await call.answer()
    await StartHandler.user_register.set()


async def user_register(call: types.CallbackQuery, state: FSMContext, data: Database):
    fsm_data = await state.get_data()
    await call.message.edit_text(t.group_confirm + call.data)
    gid = await data.get_gid(fsm_data['faculty'], call.data)
    if await data.create_user(call.message.chat.id, gid, fsm_data['username']):
        await call.message.answer(t.hi_text, reply_markup=key.main_menu(call.message.chat.id))
        await state.finish()


async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Скасування!", reply_markup=key.main_menu(message.chat.id))
    await state.finish()


def register_handler_common(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_callback_query_handler(cb_faculty, state=StartHandler.faculty_selection)
    dp.register_callback_query_handler(user_register, state=StartHandler.user_register)
    dp.register_message_handler(cancel, Text(equals=t.b_cancel, ignore_case=False), state="*")
