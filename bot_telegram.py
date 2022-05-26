from aiogram.utils import executor
from create_bot import dp
from handlers import client
import asyncio
timesend_sleep = 43200  #раз в 12 часов


async def background_on_start():
    while True:
        await client.check_birthday()
        await asyncio.sleep(timesend_sleep)


async def on_startup(_):
    asyncio.create_task(background_on_start())
    print("Бот вышел онлайн")

client.register_handlers_client(dp)
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
