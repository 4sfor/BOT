import sqlite3 as sq
from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect("copp.db")
    cur = base.cursor()
    if base:
        print("Data base connected OK")
    base.execute("CREATE TABLE IF NOT EXISTS room(img TEXT, name TEXT PRIMARY KEY, description TEXT, device TEXT)")
    base.execute(
        "CREATE TABLE IF NOT EXISTS employee( name TEXT, fam TEXT , otch TEXT ,role TEXT, email TEXT, key TEXT)")
    base.execute("CREATE TABLE IF NOT EXISTS client(id TEXT PRIMARY KEY,name TEXT, fam TEXT , otch TEXT ,org TEXT, email TEXT, key TEXT, "
                 "PhoneNumber TEXT)")
    base.commit()


async def sql_add_room(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO room VALUES(?,?,?,?)", tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute("SELECT*FROM room").fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\n Описание: {ret[2]}\n Оборудование {ret[-1]}")


async def sql_add_emp(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO  employee VALUES(?,?,?,?,?,?)", tuple(data.values()))
        base.commit()


async def sql_emp_read(message):
    for ret in cur.execute("SELECT*FROM employee").fetchall():
        await bot.send_message(message.from_user.id,
                               f"Имя:{ret[0]}\nФамилия: {ret[1]}\nОтчество: {ret[2]}\nРоль: {ret[3]}\nПочта: {ret[4]}\nПароль: {ret[5]}  ")


async def sql_read2():
    return cur.execute('SELECT * FROM room').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM room WHERE name = ?', (data,))
    base.commit()

async def sql_client_add(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO client VALUES(?,?,?,?,?,?,?,?)", tuple(data.values()))
        base.commit()

async def sql_client_read(message):
    for ret in cur.execute("SELECT*FROM client").fetchall():
        await bot.send_message(message.from_user.id,
                               f"ID:{ret[0]}\nИмя: {ret[1]}\nФамилия: {ret[2]}\nОтчество: {ret[3]}\nОрганизация: {ret[4]}\nПочта: {ret[5]}\nПароль: {ret[6]}\nНомер телефона: {ret[7]}  ")



#async def sql_client_read_foruser(message)
    #cur.execute("SELECT*FROM client")


#sync def sql_delete_command(data):
    #cur.execute('DELETE')