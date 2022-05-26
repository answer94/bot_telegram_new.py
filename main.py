import datetime

from json_test import find_fio
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types,Dispatcher
import os
from aiogram.dispatcher.filters import Text
from keyboards import client_kb
from doc import write_excel as we


from create_bot import TOKEN


from aiogram import Bot, Dispatcher, executor, types
from doc import word_otpusk as wo

from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar

from doc import json_download as jd
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup





API_TOKEN = TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())



class FSM_bot(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()
    state6 = State()
    state7 = State()
    state8 = State()




@dp.message_handler(commands='start',state=None)
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,"Привет\nВведи свою фамилию")
        await FSM_bot.state1.set()
    except:
        await message.reply("Общение с ботом через лс, напишите ему ")


# simple calendar usage
@dp.callback_query_handler(simple_cal_callback.filter(), state=(FSM_bot.state8 or FSM_bot.state7))
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        a1 = date.strftime("%d.%m.%Y")
        async with state.proxy() as data:
            data["date"] = a1

        await callback_query.message.answer(
            f'You selected {a1}',
            reply_markup=client_kb.kb_client1)



#выходд из состояния
@dp.message_handler(state="*",commands="отмена")
async def cancel_handler(message: types.message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")


@dp.message_handler(state=FSM_bot.state1)
async def cm_start(message: types.Message,state: FSMContext):
    str1 = message.text
    try:
        text_and_data = jd.find_fio(str1)
    except:
        await message.reply("Такого челика нет\n Попробуй еще разок")
    await message.answer(text='Выбери ФИО', reply_markup=client_kb.kb(text_and_data))
    await FSM_bot.next()


@dp.message_handler(state=FSM_bot.state2)  # if cb.data == 'no'
async def cm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        fio111 = message.text
        user_data = jd.find_fio(fio111)
        print(user_data)
        data["ФИО"] = user_data[0]
        data["all"] = jd.staff[data["ФИО"]]

    await message.answer(text='Выбери отчет', reply_markup=client_kb.inline_kb1)
    await FSM_bot.next()


@dp.callback_query_handler(lambda c: c.data == 'button1', state=FSM_bot.state3)
async def process_callback(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.from_user.id, 'Нажата первая кнопка!',reply_markup=client_kb.inline_kb11)
    await FSM_bot.state4.set()


@dp.callback_query_handler(lambda c: c.data == 'button2', state=FSM_bot.state3)
async def process_callback(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.from_user.id, 'введи кол-во дней отпуска',reply_markup=ReplyKeyboardRemove())
    await FSM_bot.state5.set()

@dp.callback_query_handler(lambda c: c.data == 'button3', state=FSM_bot.state3)
async def process_callback(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.from_user.id, 'Нажата 3!',reply_markup=client_kb.inline_kb11)
    await FSM_bot.state6.set()





@dp.message_handler(state=FSM_bot.state3)  # if cb.data == 'no'
async def cm(message: types.Message, state: FSMContext):
    if message.text == "авансовый_отчет":

        await FSM_bot.state4.set()

    elif message.text == "заявление_на_отпуск":
        await message.answer(text='2', reply_markup=client_kb.kb_client1)
        await FSM_bot.state5.set()
    elif message.text == "заявление_на_отгул":
        await message.answer(text='3', reply_markup=client_kb.kb_client1)
        await FSM_bot.state6.set()



@dp.message_handler(state=FSM_bot.state4)  # if cb.data == 'no'
async def cm(message: types.Message, state: FSMContext):
    await message.answer(text="пришли чек")
    await FSM_bot.state7.set()

class FioException(Exception):
    pass

def isdigit(data):
    if str(data).isdigit():
        return data
    else:
        raise FioException

@dp.message_handler(state=FSM_bot.state5)  # if cb.data == 'no'
async def cm1(message: types.Message, state: FSMContext):
    str1 = message.text
    try:
        str2 = isdigit(str1)
        async with state.proxy() as data:
            data["number_day"] = str2
        await message.answer("Выбери дату начала отпуска и введи коллво дней: ",
                             reply_markup=await SimpleCalendar().start_calendar())

        await FSM_bot.state8.set()
    except:
        await message.reply("Некорректно выбрано колличество дней \n ВВеди целое число \n Попробуй еще разок")
        FSM_bot.state5.set()






@dp.message_handler(state=FSM_bot.state6) # if cb.data == 'no'
async def cm2(message: types.Message, state: FSMContext):
    await message.answer(text="ВВеди дату начала отпуска, и колличество дней в формате 23.12.11 14")
    await state.finish()

@dp.message_handler(content_types=["document"],state=FSM_bot.state7)
async def load_document(message: types.Message,state: FSMContext):
    if document := message.document:
        destination_file=os.getcwd() + '/doc/' + str(document.file_name)
        await document.download(destination_file=destination_file)
        async with state.proxy() as data:
            a1=we.PdfToExcell()
            a1.write_excell(destination_file,data["ФИО"],data['all'][2])
        os.remove(destination_file)
        filesend = os.getcwd() + "/doc/report.xlsx"
        print(filesend)
        with open(filesend, "rb") as f1:
            await message.answer_document(f1)
        await state.finish()

    else:
        await state.finish()



@dp.message_handler(state=FSM_bot.state8)
async def cm2(message: types.Message, state: FSMContext):
    try:
        str1 = message.text

    except:
        await message.reply("Такого челика нет ")

    df_otpusk = os.getcwd() + '/doc/template_otpusk.docx'
    async with state.proxy() as data:
        a2=datetime.datetime.now().strftime("%d.%m.%Y")
        a1=wo.write_word_holiday(df_otpusk, data['ФИО'], data["all"],data["number_day"],data["date"],a2)
    with open(a1, "rb") as f1:
        await message.answer_document(f1)

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)