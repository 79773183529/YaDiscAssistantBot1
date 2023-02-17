from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# AnkiAssistantBot
TOKEN = "6119151293:AAGClhfpBk4qU80-m5F5E8rEPEN00WCkQZE"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

id_creator = 1068817703
