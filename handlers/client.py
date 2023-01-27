from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client, client_save
from data_base import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text


class FSMAdmin(StatesGroup):
    user_id = State()
    name_client = State()
    fam_client = State()
    otch_client = State()
    org_client = State()
    email_client = State()
    key_client = State()
    phone_number_client = State()


async def send_start(message: types.Message):
    await message.answer("Привет я бот ЦОПП для бронирования помещений!", reply_markup=kb_client)


async def add_client(message: types.Message):
    await FSMAdmin.user_id.set()
    await message.reply("Начать регистрацию?Введите любой текст, чтобы продолжнить или 'отмена'")


async def cancel_handler_client(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")


async def add_client_id(message: types.Message, state: FSMContext):
    global user_id
    user_id = message.from_user.id
    async with state.proxy() as data:
        data["user_id"] = user_id
    await FSMAdmin.next()
    await message.reply("Ваше имя")


async def add_client_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name_client"] = message.text
    await FSMAdmin.next()
    await message.reply("Ваша фамилия")


async def add_client_fam(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["fam_client"] = message.text
    await FSMAdmin.next()
    await message.reply("Ваше отчество")


async def add_client_otch(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["otch_client"] = message.text
    await FSMAdmin.next()
    await message.reply("Ваша организация")


async def add_client_org(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["org_client"] = message.text
    await FSMAdmin.next()
    await message.reply("Ваша почта")


async def add_client_email(message: types.Message, state: FSMContext):
    async  with state.proxy() as data:
        data["email_client"] = message.text
    await FSMAdmin.next()
    await message.reply("Ваш пароль")


async def add_client_key(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["key_client"] = message.text
    await FSMAdmin.next()
    await message.reply("Ваш номер телефона")


async def add_client_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone_number_client"] = message.text
    await message.reply(str(data))
    await FSMAdmin.next()
    await message.answer("Проверьте корректность введенных данных, если данные неверны введите 'отмена' и повторите регистрацию", reply_markup=client_save)

async def save_data_client(message: types.Message, state: FSMContext):
    await sqlite_db.sql_client_add(state)
    await message.reply("Вы зарегистрированы")
    await state.finish()




@dp.message_handler(commands=["Список_помещений"])
async def room_list_foruser(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_start, commands=["start"])
    dp.register_message_handler(add_client, commands=["Регистрация"], state=None)
    dp.register_message_handler(cancel_handler_client, state="*", commands="отмена")
    dp.register_message_handler(cancel_handler_client, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(add_client_id, state=FSMAdmin.user_id)
    dp.register_message_handler(add_client_name, state=FSMAdmin.name_client)
    dp.register_message_handler(add_client_fam, state=FSMAdmin.fam_client)
    dp.register_message_handler(add_client_otch, state=FSMAdmin.otch_client)
    dp.register_message_handler(add_client_org, state=FSMAdmin.org_client)
    dp.register_message_handler(add_client_email, state=FSMAdmin.email_client)
    dp.register_message_handler(add_client_key, state=FSMAdmin.key_client)
    dp.register_message_handler(add_client_phone, state=FSMAdmin.phone_number_client)
    dp.register_message_handler(save_data_client, commands="Сохранить")
