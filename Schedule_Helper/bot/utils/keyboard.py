import os
from pathlib import Path

from aiogram import types
from dotenv import load_dotenv

from ..language import uk_UA as t

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "settings" / ".env")


def inline_choose(data):
    keyboard = types.InlineKeyboardMarkup()
    for key in data:
        keyboard.add(types.InlineKeyboardButton(text=key, callback_data=key))
    return keyboard


def back():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(t.b_back, t.b_cancel)
    return keyboard


def cancel():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(t.b_cancel)
    return keyboard


def main_menu(aid):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(t.b_timetable)
    keyboard.add(t.b_settings)
    if aid == int(os.getenv("MAIN_ADMIN")):
        keyboard.add(t.b_admin)
    return keyboard


def settings():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(t.b_notification)
    keyboard.add(t.b_group)
    keyboard.add(t.b_cancel)
    return keyboard


def chosen_on():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(t.b_on_off)
    keyboard.add(t.b_back)
    return keyboard


def admin():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(t.b_newsletter)
    keyboard.add(t.b_cancel)
    return keyboard


def send_news():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(t.b_send_news)
    keyboard.add(t.b_cancel)
    return keyboard


def sdl(week, week_reverse=False, day=None):
    days = {
        'monday': types.InlineKeyboardButton(text='Пн', callback_data='monday'),
        'tuesday': types.InlineKeyboardButton(text='Вт', callback_data='tuesday'),
        'wednesday': types.InlineKeyboardButton(text='Ср', callback_data='wednesday'),
        'thursday': types.InlineKeyboardButton(text='Чт', callback_data='thursday'),
        'friday': types.InlineKeyboardButton(text='Пт', callback_data='friday'),
        'saturday': types.InlineKeyboardButton(text='Cб', callback_data='saturday'),
    }

    odd_text = t.even if week_reverse else t.odd
    even_text = t.odd if week_reverse else t.even

    odd = types.InlineKeyboardButton(text=odd_text, callback_data='odd')
    even = types.InlineKeyboardButton(text=even_text, callback_data='even')
    close = types.InlineKeyboardButton(text='Закрити', callback_data='close')

    if day in days:
        days[day].text = '👁'

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*days.values())
    keyboard.add(odd if week == 'even' else even)
    keyboard.add(close)
    return keyboard


def sdl_edit():
    edit = types.InlineKeyboardButton(text='Редагувати', callback_data='edit')
    delete = types.InlineKeyboardButton(text='Видалити', callback_data='full')
    close = types.InlineKeyboardButton(text='Закрити', callback_data='close')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(edit, delete)
    keyboard.add(close)
    return keyboard


def prst():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(t.b_prst_pr, t.b_prst_lc)
    keyboard.add(t.b_back, t.b_cancel)
    return keyboard
