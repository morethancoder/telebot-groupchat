import telebot
from decouple import config

BOT_TOKEN = config("BOT_TOKEN")
bot= telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start","help"])
def startBot(message):
    bot.send_message(message.chat.id,"welcome to stone بوت مجموعة تيليجرام 😀")

bot.infinity_polling()