from core.logger import setup_logging, get_logger
from telebot import TeleBot
from core.config import config
from src.head_router import initialize_routers

setup_logging(
    level=config.LOG_LEVEL
)
logger = get_logger(__name__)
logger.debug("Starting with configuration:")
for key, value in config.model_dump().items():
    logger.debug(f"{key} = {value}")

bot = TeleBot(token=config.TELEGRAM_TOKEN)

initialize_routers(bot)

bot.polling(non_stop=True)