import logging

from ..language import uk_UA as t
from ..utils.database import Database
from ..utils.utils import create_schedule, get_week_type, get_weekday
from ..utils import keyboard as key
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup


class TimeTable(StatesGroup):
    day_selection = State()
    callback_register = State()


async def cmd_timetable(message: types.Message, state: FSMContext, data: Database):
    week = get_week_type()
    gid = await data.get_group(message.chat.id)
    raw_data = await data.get_schedule(gid, week)
    week_reverse = await data.get_week_reverse(gid)
    await state.update_data(week=week, gid=gid, schedule=create_schedule(raw_data), week_reverse=week_reverse)
    await message.answer(t.day_text, reply_markup=key.sdl(week, week_reverse))
    await TimeTable.callback_register.set()


async def callback_register(call: types.CallbackQuery, state: FSMContext, data: Database):
    fsm_data = await state.get_data()

    await data.add_count(call.message.chat.id, 'timetable')

    week = fsm_data['week']
    schedule = fsm_data['schedule']
    week_reverse = fsm_data['week_reverse']
    day = call.data if call.data != 'close' and call.data != 'odd' and call.data != 'even' else get_weekday()

    if call.data == 'odd' or call.data == 'even':
        week = call.data
        raw = await data.get_schedule(fsm_data['gid'], week)
        schedule = create_schedule(raw)
        await state.update_data(week=week, schedule=schedule)
    elif call.data == 'close':
        await call.message.delete()
        await state.finish()

    try:
        await call.message.edit_text(
            schedule[day] + t.form_footer if day in schedule else t.none_text,
            reply_markup=key.sdl(week, week_reverse, day),
            disable_web_page_preview=True
        )
    except Exception as ex:
        logging.error(ex)
        pass

    await call.answer()
    return


def register_handler_timetable(dp: Dispatcher):
    dp.register_message_handler(cmd_timetable, Text(equals=t.b_timetable, ignore_case=True), state="*")
    dp.register_callback_query_handler(callback_register, state=TimeTable.callback_register)
