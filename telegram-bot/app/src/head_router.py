from telebot import TeleBot
from .scenarios.ping import router as ping_router

def initialize_routers(bot: TeleBot):
    ping_router.ping_scenario(bot)