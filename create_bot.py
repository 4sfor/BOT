from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
#токен бота
API_TOKEN = '5886185523:AAH-wn1VoceFcRlDxOgzJvPYUy27tNk_6FM'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)