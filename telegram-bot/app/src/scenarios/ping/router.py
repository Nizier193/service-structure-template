from telebot import TeleBot

def ping_scenario(bot: TeleBot):
    @bot.message_handler(commands=["ping"])
    def ping(message):
        bot.send_message(
            message.chat.id,
            text="Hi!"
        )

    return ping
