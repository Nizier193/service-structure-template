from telebot import TeleBot

from src.helpers.ping_api import PingAPI

api = PingAPI()

def ping_scenario(bot: TeleBot):
    @bot.message_handler(commands=["ping"])
    def ping(message):
        response = api.ping()

        if response:
            bot.send_message(
                message.chat.id,
                text=f"Ping succesfully executed. Ping ID: {response.get("connection", {}).get("id")}."
            )
        else:
            bot.send_message(
                message.chat.id,
                text="Something went wrong while executing ping. Probably backend is offline."
            )

    return ping
