from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
registracia=KeyboardButton("/Регистрация")
save=KeyboardButton("/Сохранить")
room_list=KeyboardButton("/Список_помещений")

kb_client=ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(registracia)\
    .add(room_list)
client_save=ReplyKeyboardMarkup(resize_keyboard=True)
client_save.add(save)