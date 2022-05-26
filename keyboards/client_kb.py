from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

b1 = KeyboardButton('авансовый')
b2 = KeyboardButton('отпуск')
b3 = KeyboardButton('отгул')
kb_client=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
kb_client.add(b1,b2,b3)


a1 = KeyboardButton('далее')
a2 = KeyboardButton('отмена')
kb_client1=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
kb_client1.row(a1,a2)


def kb(data):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in data:
        keyboard.add(name)
    keyboard.add('отмена')
    return keyboard


av_k1 = KeyboardButton('мобильная_связь')
av_k2 = KeyboardButton('шаблон')
kb_av=ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
kb_av.row(av_k1,av_k2)
