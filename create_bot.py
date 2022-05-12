from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
TOKEN = '1130523818:AAHbAR4O9Lz-RuA3jfPckrkJZ-LKNZGD1U0'
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
