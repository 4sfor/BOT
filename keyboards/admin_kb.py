from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#кнопки, которые используются в панели администратора
button_tab_room = KeyboardButton("/Помещения")
button_load = KeyboardButton("/Добавить_помещение")
button_list_room = KeyboardButton("/Список_помещений")
button_delete_room=KeyboardButton("/Удалить_помещение")
button_tab_emp = KeyboardButton("/Сотрудники")
button_add_emp = KeyboardButton("/Добавить_сотрудника")
button_list_emp = KeyboardButton("/Список_Сотрудников")
button_list_user = KeyboardButton("/Список_пользователей")
button_tab_event=KeyboardButton("/Мероприятия")
button_add_event=KeyboardButton("/Добавить_мероприятие")
button_list_event=KeyboardButton("/Список_мероприятий")
#вкладка помещения
button_case_admin_room = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load) \
    .add(button_list_room).add(button_delete_room)
#основное меню
button_main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(button_tab_room) \
    .add(button_tab_emp).add(button_list_user).add(button_tab_event)

#вкладка сотрудники
button_case_admin_emp=ReplyKeyboardMarkup(resize_keyboard=True).add(button_add_emp) \
    .add(button_list_emp)
#вкладка мероприятия
button_case_admin_event=ReplyKeyboardMarkup(resize_keyboard=True).add(button_add_event)\
    .add(button_list_event)