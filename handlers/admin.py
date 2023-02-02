from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import bot_text


# переменные для машины состояний
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
    name_event = State()
    room_event = State()
    org_event = State()
    date_event = State()
    time_event = State()


# команда для перехода в режим администратора
async def admin(message: types.Message):
    await message.answer(bot_text.start_admin, reply_markup=admin_kb.button_main_menu)


# функция, вызывающая вкладку помещения и кнопки к ней
async def admin_kb_main(message: types.Message):
    await message.answer(bot_text.room_tab, reply_markup=admin_kb.button_case_admin_room)


# функция запускающая машину состояний для добавления помещения
async def cm_start(message: types.Message):
    # if user=="Admin":
    await FSMAdmin.photo.set()
    await message.reply(bot_text.photo_load)


# фунция которая завершает машину состояний
async def cancel_handler(message: types.Message, state: FSMContext):
    # if user=="Admin":
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply(bot_text.cancel_message)


# сохраняет полученное фото помещения, запрашивает его имя
async def load_photo(message: types.Message, state: FSMContext):
    # if user=="Admin":
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply(bot_text.name_room)


# сохраняет имя, запрашивает описание
async def load_name(message: types.Message, state: FSMContext):
    # if user=="Admin":
    async with state.proxy() as data:
        data["name"] = message.text
    await FSMAdmin.next()
    await message.reply(bot_text.description_room)


# сохраняет описание,запрашивает список оборудования
async def load_description(message: types.Message, state: FSMContext):
    # if user=="Admin":
    async with state.proxy() as data:
        data["description"] = message.text
    await FSMAdmin.next()
    await message.reply(bot_text.device_room)


# сохраняет список оборудования, все раннее введеные данные сохраняются в БД, завершает машину состояний
async def load_device(message: types.Message, state: FSMContext):
    # if user=="Admin":
    async with state.proxy() as data:
        data["device"] = message.text

    await sqlite_db.sql_add_room(state)
    await state.finish()


# вызывает из БД все записи из табицы помещения
async def room_list_command(message: types.Message):
    await sqlite_db.sql_read(message)


# вызывает вкладку сотруднки и кнопки к ней
async def emp(message: types.Message):
    await message.answer(bot_text.employee_tab, reply_markup=admin_kb.button_case_admin_emp)


# запускает машину состояний для добавления сотрудника, запрашивает имя
async def add_emp(message: types.Message):
    await FSMAdmin.name_emp.set()
    await message.reply(bot_text.employee_name)


# сохраняет имя, запрашивает фамилию
async def add_emp_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name_emp"] = message.text
    await FSMAdmin.next()
    await message.reply(bot_text.employee_fam)


# сохраняет фамилию, запрашивает отчество
async def add_emp_fam(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["fam_emp"] = message.text
    await FSMAdmin.next()
    await message.reply(bot_text.employee_otnc)


# сохраняет отчесвто, запрашивает роль сотрудника
async def add_emp_otch(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["otch_emp"] = message.text
    await FSMAdmin.next()
    await message.reply(bot_text.employee_role)


# сохраняет роль, запрашивает почту сотрудника
async def add_emp_role(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["role_emp"] = message.text
    await FSMAdmin.next()
    await message.reply(bot_text.employee_email)


# сохраняет почту, запрашивает пароль сотрудника
async def add_email_emp(message: types.Message, state: FSMContext):
    async  with state.proxy() as data:
        data["email_emp"] = message.text
    await FSMAdmin.next()
    await message.reply(bot_text.employee_key)


# сохраняет пароль, сохраняет все в БД, завершает машину состояний
async def add_key_emp(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["key"] = message.text
    await sqlite_db.sql_add_emp(state)
    await state.finish()


# вызывает из БД список сотрудников
async def emp_list_command(message: types.Message):
    await sqlite_db.sql_emp_read(message)


# функции для удаления помещения через инлайн кнопку НЕ РАБОТАЕТ
'''@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
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
                               add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))'''


# функция для удаления помещения по имени

async def sql_delete_room(message: types.Message):
    name_room = message.text
    sqlite_db.sql_delete_room(name_room)
    answer_message = "удалено"
    await message.answer(answer_message)


# функция для вызова списка пользователей
async def user_list(message: types.Message):
    await sqlite_db.sql_client_read(message)


# открывает вкладку мероприятия и клавиатуру к ней
async def event(message: types.Message):
    await message.answer(bot_text.event_tab, reply_markup=admin_kb.button_case_admin_event)


# функция для добавления мероприятия, активирует машину состояний, запрашивает название

async def add_event(message: types.Message):
    await FSMAdmin.name_event.set()
    await message.reply(bot_text.name_event)


# сохряняет имя, выводит список помещений, запрашивает имя помещения

async def add_name_event(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name_event"] = message.text
    await FSMAdmin.next()
    await sqlite_db.sql_read(message)
    await message.reply(bot_text.enter_name_room)


# сохраняет имя, запрашивает название организации

async def add_room_event(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name_room"] = message.text
    await  FSMAdmin.next()
    await message.reply(bot_text.enter_org_event)


# сохраняет название организации, запрашивает дату

async def add_org_event(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["org_event"] = message.text
    await  FSMAdmin.next()
    await message.reply(bot_text.enter_date_event)


# сохраняет дату, запрашивает время

async def add_date_event(message: types.Message, state: FSMContext):
    async  with state.proxy() as data:
        data["date_event"] = message.text
    await  FSMAdmin.next()
    await  message.reply(bot_text.enter_time_event)


# сохраняет все в БД, завершает машину состояний

async def add_time_event(message: types.Message, state: FSMContext):
    async  with state.proxy() as data:
        data["time_event"] = message.text
    await  sqlite_db.sql_event_add()
    await state.finish()


# выводит список мероприятий

async def event_list(message: types.Message):
    await sqlite_db.sql_list_event(message)
###########для бронирования НЕ РАБОТАЕТ################
@dp.message_handler(commands="Бронь")
async def book_list(message: types.Message):
    await sqlite_db.book_list(message)
# регистрация хендлеров
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin, commands=[bot_text.start_moderator])
    dp.register_message_handler(admin_kb_main, commands=[bot_text.room_tab_command])
    dp.register_message_handler(cm_start, commands=[bot_text.room_add_command], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=bot_text.cancel_command)
    dp.register_message_handler(cancel_handler, Text(equals=bot_text.cancel_text, ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_device, state=FSMAdmin.device)
    dp.register_message_handler(room_list_command, commands=[bot_text.room_list_command])
    dp.register_message_handler(emp, commands=[bot_text.employee_tab_command])
    dp.register_message_handler(add_emp, commands=[bot_text.employee_add_command], state=None)
    dp.register_message_handler(add_emp_name, state=FSMAdmin.name_emp)
    dp.register_message_handler(add_emp_fam, state=FSMAdmin.fam_emp)
    dp.register_message_handler(add_emp_otch, state=FSMAdmin.otch_emp)
    dp.register_message_handler(add_emp_role, state=FSMAdmin.role_emp)
    dp.register_message_handler(add_email_emp, state=FSMAdmin.email_emp)
    dp.register_message_handler(add_key_emp, state=FSMAdmin.key_emp)
    dp.register_message_handler(emp_list_command, commands=[bot_text.employee_list_command])
    dp.register_message_handler(user_list, commands=[bot_text.user_list_command])
    dp.register_message_handler(sql_delete_room, commands=[bot_text.delete_room])
    dp.register_message_handler(event, commands=[bot_text.event_tab])
    dp.register_message_handler(add_event, commands=[bot_text.add_event])
    dp.register_message_handler(add_name_event, state=FSMAdmin.name_event)
    dp.register_message_handler(add_room_event, state=FSMAdmin.room_event)
    dp.register_message_handler(add_date_event, state=FSMAdmin.org_event)
    dp.register_message_handler(add_date_event, state=FSMAdmin.date_event)
    dp.register_message_handler(add_time_event, state=FSMAdmin.time_event)
    dp.register_message_handler(event_list, commands=[bot_text.list_event])
