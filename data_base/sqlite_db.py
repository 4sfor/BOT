import sqlite3 as sq
from create_bot import bot


# создание БД и таблиц
def sql_start():
    global base, cur
    base = sq.connect("copp.db")
    cur = base.cursor()
    if base:
        print("Data base connected OK")
    base.execute("CREATE TABLE IF NOT EXISTS room(img TEXT, name TEXT PRIMARY KEY, description TEXT, device TEXT)")
    base.execute(
        "CREATE TABLE IF NOT EXISTS employee( name TEXT, fam TEXT , otch TEXT ,role TEXT, email TEXT, key TEXT)")
    base.execute(
        "CREATE TABLE IF NOT EXISTS client(id TEXT PRIMARY KEY,name TEXT, fam TEXT , otch TEXT ,org TEXT, email TEXT, key TEXT, "
        "PhoneNumber TEXT)")
    base.execute("CREATE TABLE IF NOT EXISTS event(name TEXT PRIMARY KEY, room TEXT, org TEXT, date TEXT, time TEXT)")
    base.execute(
        "CREATE TABLE IF NOT EXISTS book(name_room TEXT, date_book TEXT, time_book TEXT, name_client TEXT, fam_client TEXT, org_client TEXT)")
    base.commit()


# запись данных в таблицу помещения
async def sql_add_room(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO room VALUES(?,?,?,?)", tuple(data.values()))
        base.commit()


# вывод данных из таблицы помещения
async def sql_read(message):
    for ret in cur.execute("SELECT*FROM room").fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f" {ret[1]}\n Описание: {ret[2]}\n Оборудование {ret[-1]}")


# запись данных в таблицу сотрудники
async def sql_add_emp(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO  employee VALUES(?,?,?,?,?,?)", tuple(data.values()))
        base.commit()


# вывод данных из таблицы сотрудники
async def sql_emp_read(message):
    for ret in cur.execute("SELECT*FROM employee").fetchall():
        await bot.send_message(message.from_user.id,
                               f"Имя:{ret[0]}\nФамилия: {ret[1]}\nОтчество: {ret[2]}\nРоль: {ret[3]}\nПочта: {ret[4]}\nПароль: {ret[5]}  ")


# вывод данных из таблицы помещения, для функции удаления помещений через инлайн кнопку ФУНКЦИЯ НЕ РАБОТАЕТ
async def sql_read2():
    return cur.execute('SELECT * FROM room').fetchall()


# удаления данных из таблицы помещения НЕ РАБОТАЕТ
async def sql_delete_command(data):
    cur.execute(f'DELETE FROM room WHERE name = ?', (data,))
    base.commit()


# запись данных в таблицу клиенты
async def sql_client_add(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO client VALUES(?,?,?,?,?,?,?,?)", tuple(data.values()))
        base.commit()


# вывод данных из таблицы клиенты
async def sql_client_read(message):
    for ret in cur.execute("SELECT*FROM client").fetchall():
        await bot.send_message(message.from_user.id,
                               f"ID:{ret[0]}\nИмя: {ret[1]}\nФамилия: {ret[2]}\nОтчество: {ret[3]}\nОрганизация: {ret[4]}\nПочта: {ret[5]}\nПароль: {ret[6]}\nНомер телефона: {ret[7]}  ")


# запись данных в таблицу мероприятия
async def sql_event_add(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO event VALUES(?,?,?,?,?)", tuple(data.values()))
    base.commit()


# вывод данных из таблицы мероприятия
async def sql_list_event(message):
    for ret in cur.execute("SELECT*FROM event").fetchall():
        await bot.send_message(message.from_user.id,
                               f"Название:{ret[0]}\n Помещение:{ret[1]}\n Организация:{ret[2]}\n Дата:{ret[3]}, Время:{ret[4]}")


# удаление записи из таблицы помещения по имени помещения
def sql_delete_room(name_room):
    name_room = name_room
    cur.execute(f"DELETE FROM room WHERE name={name_room}")
    base.commit()


###########для бронирования НЕ РАБОТАЕТ################
async def sql_add_book(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO book VALUES(?,?,?,?,?,?)", tuple(data.values()))
    base.commit()


async def sql_book_copy_lient(user_id):
    user_id = user_id
    cur.execute(
        f"INSERT INTO book(name_client, fam_client, org_client) SELECT name, fam, org FROM client WHERE id={user_id}")


async def book_list(message):
    for ret in cur.execute("SELECT*FROM book").fetchall():
        await bot.send_message(message.from_user.id,
                               f"Помещение:{ret[0]}\n Дата:{ret[1]}\n Время:{ret[2]}\n Имя клиента:{ret[3]}, Фамилия клиента:{ret[4]}\n Организация:{ret[5]}")
