import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from keyboards import client_kb
from doc import write_excel as we
from doc import word_otpusk as wotpusk
from doc import word_otgul as wotgul
from doc import json_download as jd
from create_bot import bot
from doc import project_exceptions as pe
from doc import doc_path as dpath
import os
from datetime import datetime, timedelta
chat_hb = -662196356


class FsmBot(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()
    state6 = State()
    state7 = State()
    state8 = State()
    state9 = State()
    state10 = State()


async def check_birthday():
    staff_data_hb = jd.load_staff_data(dpath.json_file)[1]
    hb_keys = list(staff_data_hb.keys())
    for i in hb_keys:
        datetime_object1 = datetime.strptime(i, '%d.%m.%Y')
        date_hb = datetime.now() + timedelta(days=1)
        if datetime_object1.strftime('%d.%m') == date_hb.strftime('%d.%m'):
            await bot.send_message(chat_hb, (f"День Рождения у {staff_data_hb[str(i)]} "f"\n Не забудьте поздравить "
                                             f"{datetime_object1.strftime('%d.%m')}."))


async def command_start(message: types.Message):
    # noinspection PyBroadException
    try:
        await bot.send_message(message.from_user.id, "Привет\nВведи свою фамилию")
        await FsmBot.state1.set()
    except BaseException:
        await message.reply("Общение с ботом через лс, напишите ему ")


async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        a1 = date.strftime("%d.%m.%Y")
        async with state.proxy() as data:
            data["date"] = a1

        await callback_query.message.answer(
            f'Ты выбрал {a1} \n Нажми далее',
            reply_markup=client_kb.kb_client1)


async def cancel_handler(message: types.message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("нажми /start")

async def cancel_handler1(message: types.message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("нажми /start")


async def bot_state1(message: types.Message):
    # noinspection PyBroadException
    try:
        staff_data = jd.load_staff_data(dpath.json_file)[0]
        fio = jd.find_fio(message.text, staff_data)
        await message.answer(text='Выбери ФИО', reply_markup=client_kb.kb(fio))
        await FsmBot.state2.set()
    except BaseException:
        await message.reply("Такого челика нет\n Попробуй еще разок")


async def bot_state2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        staff_data=jd.load_staff_data(dpath.json_file)[0]
        data["ФИО"] = jd.find_fio(message.text, staff_data)[0]
        data["all"] = staff_data[data["ФИО"]]
    await message.answer(text='Выбери отчет', reply_markup=client_kb.kb_client)
    await FsmBot.state3.set()


async def bot_state3(message: types.Message):
    if message.text == "авансовый":
        await message.answer('Выбран авансовый отчет \n Выбери нужный отчет',
                             reply_markup=client_kb.kb_av)
        await FsmBot.state4.set()
    elif message.text == "отпуск":
        await message.answer('Выбрано заявление на отпуск \n Введи колличество дней отпуска')
        await FsmBot.state5.set()
    elif message.text == "отгул":
        await message.answer('Выбрано заявление на отгул \n нажми далее',
                             reply_markup=client_kb.kb_client1)
        await FsmBot.state6.set()


async def bot_state4(message: types.Message):
    if message.text == "мобильная_связь" :
        await message.answer("пришли чек")
        await FsmBot.state7.set()
    elif message.text == "шаблон":
        await message.answer('Выбран авансовый отчет \n Выбери нужный отчет',
                             reply_markup=client_kb.kb_client1)
        await FsmBot.state10.set()


async def bot_state5(message: types.Message, state: FSMContext):
    # noinspection PyBroadException
    try:
        msg_txt = pe.isdigit(message.text)
        async with state.proxy() as data:
            data["number_day"] = msg_txt
        await message.answer("Выбери дату начала отпуска: ",
                             reply_markup=await SimpleCalendar().start_calendar())
        await FsmBot.state8.set()
    except BaseException:
        await message.reply("Некорректно введено колличество дней \n ВВеди целое число \n Попробуй еще разок")
        await FsmBot.state5.set()


async def bot_state6(message: types.Message, state: FSMContext):
    # noinspection PyBroadException
    await message.answer("Выбери дату отгула: ", reply_markup=await SimpleCalendar().start_calendar())
    await FsmBot.state9.set()


async def bot_state7(message: types.Message, state: FSMContext):
    if document := message.document:

        destination_file = dpath.avans_pdf(str(document.file_name))
        await document.download(destination_file=destination_file)
        # noinspection PyBroadException
        try:
            async with state.proxy() as data:
                avans_data = we.PdfToExcell()
                avans_data.write_excell(destination_file, data["ФИО"], data['all'][2])
            os.remove(destination_file)
            filesend = dpath.avans_ecxel_file
            with open(filesend, "rb") as f1:
                await message.answer_document(f1)

            await message.answer("Выбери что сделать еще", reply_markup=client_kb.kb_client)
            await FsmBot.state3.set()
        except BaseException:
            await message.answer("некорректный файл\n Отправь верный файл")
            await FsmBot.state7.set()
    else:
        await message.answer("test")
        await FsmBot.state7.set()


async def bot_state8(message: types.Message, state: FSMContext):
    df_otpusk = dpath.word_otpusk_file
    async with state.proxy() as data:
        dt_now = datetime.now().strftime("%d.%m.%Y")
        file_otpusk = wotpusk.write_word_holiday(df_otpusk, data['ФИО'], data["all"], data["number_day"],
                                                 data["date"], dt_now)
    with open(file_otpusk, "rb") as f1:
        await message.answer_document(f1)
    await message.answer("Выбери что сделать еще", reply_markup=client_kb.kb_client)
    await FsmBot.state3.set()


async def bot_state9(message: types.Message, state: FSMContext):
    df_otgul = dpath.word_otgul_file
    async with state.proxy() as data:
        dt_now = datetime.now().strftime("%d.%m.%Y")
        file_otgul = wotgul.write_word_otgul(df_otgul, data['ФИО'], data["all"], data["date"],
                                            dt_now)
    with open(file_otgul, "rb") as f1:
        await message.answer_document(f1)
    await message.answer("Выбери что сделать еще", reply_markup=client_kb.kb_client)
    await FsmBot.state3.set()

async def bot_state10(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        avans_data = we.PdfToExcell()
        avans_data.write_excell_template(data["ФИО"], data['all'][2])
    filesend = dpath.avans_ecxel_template
    with open(filesend, "rb") as f1:
        await message.answer_document(f1)

    await message.answer("Выбери что сделать еще", reply_markup=client_kb.kb_client)
    await FsmBot.state3.set()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(cancel_handler1, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(bot_state1, state=FsmBot.state1)
    dp.register_message_handler(bot_state2, state=FsmBot.state2)
    dp.register_message_handler(bot_state3, state=FsmBot.state3)
    dp.register_message_handler(bot_state4, state=FsmBot.state4)
    dp.register_message_handler(bot_state5, state=FsmBot.state5)
    dp.register_message_handler(bot_state6, state=FsmBot.state6)
    dp.register_message_handler(bot_state7, content_types=["document"], state=FsmBot.state7)
    dp.register_message_handler(bot_state8, state=FsmBot.state8)
    dp.register_message_handler(bot_state9, state=FsmBot.state9)
    dp.register_callback_query_handler(process_simple_calendar, simple_cal_callback.filter(),
                                       state=(FsmBot.state8))
    dp.register_callback_query_handler(process_simple_calendar, simple_cal_callback.filter(),
                                       state=(FsmBot.state9))

    dp.register_message_handler(bot_state10, state=FsmBot.state10)
