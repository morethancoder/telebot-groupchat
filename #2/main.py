import telebot
from telebot import types,util
from decouple import config
from googletrans import Translator

BOT_TOKEN = config("BOT_TOKEN")
bot= telebot.TeleBot(BOT_TOKEN)
bot_data={
    "name" : ["stone","حجر"]
    
}
text_messages={
    "welcome": "welcome to stone بوت مجموعة تليجرام ☺",
    "welcomeNewMember" : 
                u"اهلا بك {name} في مجموعتنا الخاصة 🙋‍♂️",
    "saying goodbye":
                u"العضو {name} غادر المجموعة 🥺",

    "leave":"لقد تم اضافتي الى مجموعة غير المجموعة التي صممت لها , وداعاً 🧐",
    "call" : "كيف يمكنني المساعدة ؟ 😀"
}

commands = {
    "translate":["translate","trans","ترجم","ترجملي"]
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
        


#* leave anychat thats not mine
@bot.my_chat_member_handler()
def leave(message:types.ChatMemberUpdated):
    update = message.new_chat_member
    if update.status == "member":
        bot.send_message(message.chat.id,text_messages["leave"])
        bot.leave_chat(message.chat.id)


#* listening to group messages
#* respond to bot name
@bot.message_handler(func=lambda m:True)
def reply(message):
    words = message.text.split()
    if words[0] in bot_data["name"]:
        bot.reply_to(message,text_messages["call"])
    
#* adding googletrans api
#* translating word to arabic
#* translating sentence to arabic
    if words[0] in commands["translate"]:
        translator = Translator()
        translation = translator.translate(" ".join(words[1:]),dest="ar")
        bot.reply_to(message,translation.text)
    
        




bot.infinity_polling(allowed_updates=util.update_types)