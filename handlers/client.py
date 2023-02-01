from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client, client_save
from data_base import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import bot_text


# переменные для машины состояний
class FSMAdmin(StatesGroup):
    user_id = State()
    name_client = State()
    fam_client = State()
    otch_client = State()
    org_client = State()
    email_client = State()
    key_client = State()
    phone_number_client = State()
    name_room= State()
    date_book=State()
    time_book= State()
    name_client_book=State()


# открывает пользовательскую клавиатуру
async def send_start(message: types.Message):
    await message.answer(bot_text.start_message_user, reply_markup=kb_client)


# начинает решистрацию пользователя, запрашивает ввести любой текст, чтобы получить id пользователя
async def add_client(message: types.Message):
    await FSMAdmin.user_id.set()
    await message.reply(bot_text.registracia_user_message)


# завершает машину сотсояний елси ввести "отмена"
async def cancel_handler_client(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply(bot_text.cancel_message)


# сохраняет id пользователя, запрашивает имя
async def add_client_id(message: types.Message, state: FSMContext):
    global user_id
    user_id = message.from_user.id
    async with state.proxy() as data:
        data["user_id"] = user_id
    await FSMAdmin.next()
    await message.reply(bot_text.add_name_user)


# сохраняет имя, запрашивает фамилию
async def add_client_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name_client"] = message.text
    await FSMAdmin.next()
    await message.reply(bot_text.add_fam_user)


# сохраняет фамилию, запрашивате отчество
async def add_client_fam(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["fam_client"] = message.text
    await FSMAdmin.next()
    await message.reply(bot_text.add_otch_user)


# сохраняет отчество, запрашивает название организации
async def add_client_otch(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["otch_client"] = message.text
    await FSMAdmin.next()
    await message.reply(bot_text.add_org_user)


# сохраняет организация, запрашивает почту
async def add_client_org(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["org_client"] = message.text
    await FSMAdmin.next()
    await message.reply(bot_text.add_email_user)


# сохраняет почту, запрашивает пароль
async def add_client_email(message: types.Message, state: FSMContext):
    async  with state.proxy() as data:
        data["email_client"] = message.text
    await FSMAdmin.next()
    await message.reply(bot_text.add_key_user)


# сохраняет пароль, запрашивает номер телефона
async def add_client_key(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["key_client"] = message.text
    await FSMAdmin.next()
    await message.reply(bot_text.add_phone_user)


# сохраняте номер телефона, выводит все ранее введеные данные, вызывает кпоку сохранить
async def add_client_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone_number_client"] = message.text
    await message.reply(str(data))
    await FSMAdmin.next()
    await message.answer(bot_text.check_data_reg, reply_markup=client_save)


# сохраняет данные регистрации в БД
async def save_data_client(message: types.Message, state: FSMContext):
    await sqlite_db.sql_client_add(state)
    await message.reply(bot_text.comlete_reg_user)
    await state.finish()


# Вызывает список помещений

async def room_list_foruser(message: types.Message):
    await sqlite_db.sql_read(message)

@dp.message_handler(commands="Забронировать_помещение", state=None)
async def book_room(message: types.Message):
    await sqlite_db.sql_read(message)
    await FSMAdmin.name_room.set()
    await message.reply("Введите имя помещения")

@dp.message_handler(state=FSMAdmin.name_room)
async def name_room_book(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name_room_book"]=message.text
    await FSMAdmin.next()
    await message.reply("Введите дату")

@dp.message_handler(state=FSMAdmin.date_book)
async def date_book(message: types.Message, state: FSMContext):
    async  with state.proxy() as data:
        data["data_event"]=message.text
    await FSMAdmin.next()
    await message.reply("Введите время")

@dp.message_handler(state=FSMAdmin.time_book)
async def time_book(message: types.Message, state: FSMContext):
    async  with state.proxy() as data:
        data["time_event"]=message.text
    await FSMAdmin.next()

@dp.message_handler(state=FSMAdmin.name_client_book)
async def name_client_book(message: types.Message, state:FSMContext):



# регистрация хендлеров
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_start, commands=[bot_text.start_user_command])
    dp.register_message_handler(add_client, commands=[bot_text.registracia_command], state=None)
    dp.register_message_handler(cancel_handler_client, state="*", commands=bot_text.cancel_command)
    dp.register_message_handler(cancel_handler_client, Text(equals=bot_text.cancel_text, ignore_case=True), state="*")
    dp.register_message_handler(add_client_id, state=FSMAdmin.user_id)
    dp.register_message_handler(add_client_name, state=FSMAdmin.name_client)
    dp.register_message_handler(add_client_fam, state=FSMAdmin.fam_client)
    dp.register_message_handler(add_client_otch, state=FSMAdmin.otch_client)
    dp.register_message_handler(add_client_org, state=FSMAdmin.org_client)
    dp.register_message_handler(add_client_email, state=FSMAdmin.email_client)
    dp.register_message_handler(add_client_key, state=FSMAdmin.key_client)
    dp.register_message_handler(add_client_phone, state=FSMAdmin.phone_number_client)
    dp.register_message_handler(save_data_client, commands=bot_text.registracia_save_command)
    dp.register_message_handler(room_list_foruser, commands=[bot_text.user_list_room])
