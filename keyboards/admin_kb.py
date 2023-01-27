from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


button_tab_room = KeyboardButton("/Помещения")
button_load = KeyboardButton("/Добавить_помещение")
button_list_room = KeyboardButton("/Список_помещений")
button_tab_emp = KeyboardButton("/Сотрудники")
button_add_emp = KeyboardButton("/Добавить_сотрудника")
button_list_emp = KeyboardButton("/Список_Сотрудников")
button_list_user = KeyboardButton("/Список_пользователей")

button_case_admin_room = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load) \
    .add(button_list_room)

button_main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(button_tab_room) \
    .add(button_tab_emp).add(button_list_user)


button_case_admin_emp=ReplyKeyboardMarkup(resize_keyboard=True).add(button_add_emp) \
    .add(button_list_emp)