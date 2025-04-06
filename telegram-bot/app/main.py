from telebot import TeleBot
from core.config import config

from src.head_router import initialize_routers

bot = TeleBot(
    token=config.TELEGRAM_TOKEN
)

initialize_routers(bot)

bot.polling(
    non_stop=True
)