from settings import BOT_TOKEN, PAY_TOKEN
from aiogram import Bot, Dispatcher, executor

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

from app.handlers.handler import *

if __name__ == '__main__':
    executor.start_polling(dp)

# Main file, that run all application
