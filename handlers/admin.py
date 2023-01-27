from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    device = State()
    name_emp = State()
    fam_emp = State()
    otch_emp = State()
    role_emp = State()
    email_emp = State()
    key_emp = State()


async def admin(message: types.Message):
    await message.answer("Привет админ", reply_markup=admin_kb.button_main_menu)


async def admin_kb_main(message: types.Message):
    await message.answer("Вкладка помещения ", reply_markup=admin_kb.button_case_admin_room)


async def cm_start(message: types.Message):
    # if user=="Admin":
    await FSMAdmin.photo.set()
    await message.reply("Загрузи фото")


async def cancel_handler(message: types.Message, state: FSMContext):
    # if user=="Admin":
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")


async def load_photo(message: types.Message, state: FSMContext):
    # if user=="Admin":
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply("Название")


async def load_name(message: types.Message, state: FSMContext):
    # if user=="Admin":
    async with state.proxy() as data:
        data["name"] = message.text
    await FSMAdmin.next()
    await message.reply("Введите описание")


async def load_description(message: types.Message, state: FSMContext):
    # if user=="Admin":
    async with state.proxy() as data:
        data["description"] = message.text
    await FSMAdmin.next()
    await message.reply("Введите список оборудования")


async def load_device(message: types.Message, state: FSMContext):
    # if user=="Admin":
    async with state.proxy() as data:
        data["device"] = message.text

    await sqlite_db.sql_add_room(state)
    await state.finish()



async def room_list_command(message: types.Message):
    await sqlite_db.sql_read(message)
@dp.message_handler(commands=["Сотрудники"])
async def emp(message: types.Message):
    await message.answer("Вкладка сотрудники", reply_markup=admin_kb.button_case_admin_emp)

async def add_emp(message: types.Message):
    await FSMAdmin.name_emp.set()
    await message.reply("Имя сотрудника")


async def add_emp_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name_emp"] = message.text
    await FSMAdmin.next()
    await message.reply("Фамилия сотрудника")


async def add_emp_fam(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["fam_emp"] = message.text
    await FSMAdmin.next()
    await message.reply("Отчество сотрудника")


async def add_emp_otch(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["otch_emp"] = message.text
    await FSMAdmin.next()
    await message.reply("Роль сотрудника")


async def add_emp_role(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["role_emp"] = message.text
    await FSMAdmin.next()
    await message.reply("e-mail")


async def add_email_emp(message: types.Message, state: FSMContext):
    async  with state.proxy() as data:
        data["email_emp"] = message.text
    await FSMAdmin.next()
    await message.reply("пароль")


async def add_key_emp(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["key"] = message.text
    await sqlite_db.sql_add_emp(state)
    await state.finish()


async def emp_list_command(message: types.Message):
    await sqlite_db.sql_emp_read(message)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del", "")} удалено ', show_alert=True)


@dp.message_handler(commands="Удалить")
async def delete_item(message: types.Message):
    read = await sqlite_db.sql_read2()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\n Описание: {ret[2]}\n Оборудование {ret[-1]}")
        await bot.send_message(message.from_user.id, text="Удалить помещение из списка?",
                               reply_markup=InlineKeyboardMarkup(). \
                               add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


@dp.message_handler(commands="Список_пользователей")
async def user_list(message: types.Message):
    await sqlite_db.sql_client_read(message)

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin, commands=["moderator"])
    dp.register_message_handler(admin_kb_main, commands=["Помещения"])
    dp.register_message_handler(cm_start, commands=["Добавить_помещение"], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands="отмена")
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_device, state=FSMAdmin.device)
    dp.register_message_handler(room_list_command, commands=["Список_помещений"])
    dp.register_message_handler(add_emp, commands=["Добавить_сотрудника"], state=None)
    dp.register_message_handler(add_emp_name, state=FSMAdmin.name_emp)
    dp.register_message_handler(add_emp_fam, state=FSMAdmin.fam_emp)
    dp.register_message_handler(add_emp_otch, state=FSMAdmin.otch_emp)
    dp.register_message_handler(add_emp_role, state=FSMAdmin.role_emp)
    dp.register_message_handler(add_email_emp, state=FSMAdmin.email_emp)
    dp.register_message_handler(add_key_emp, state=FSMAdmin.key_emp)
    dp.register_message_handler(emp_list_command, commands=["Список_сотрудников"])
