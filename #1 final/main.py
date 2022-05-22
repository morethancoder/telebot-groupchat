
import telebot
from telebot import types,util
from decouple import config


BOT_TOKEN = config("BOT_TOKEN")
bot= telebot.TeleBot(BOT_TOKEN)

text_messages={
    "welcome": "welcome to stone بوت مجموعة تليجرام ☺",
    "welcomeNewMember" : 
                u"اهلا بك {name} في مجموعتنا الخاصة 🙋‍♂️",
    "saying goodbye":
                u"العضو {name} غادر المجموعة 🥺"
}

@bot.message_handler(commands=["start","help"])
def startBot(message):
    bot.send_message(message.chat.id,text_messages["welcome"])

#* saying Welcome to joined members
#* saying goodbye to left members
@bot.chat_member_handler()
def handleUserUpdates(message:types.ChatMemberUpdated):
    newResponse = message.new_chat_member
    if newResponse.status == "member":
        bot.send_message(message.chat.id,text_messages["welcomeNewMember"].format(name=newResponse.user.first_name))
    if newResponse.status == "left":
        bot.send_message(message.chat.id,text_messages["saying goodbye"].format(name=newResponse.user.first_name))
       

bot.infinity_polling(allowed_updates=util.update_types)