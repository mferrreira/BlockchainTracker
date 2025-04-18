import telebot # type: ignore

bot = telebot.TeleBot('YOUR_TOKEN')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Eu sou um bot.")

bot.polling()
