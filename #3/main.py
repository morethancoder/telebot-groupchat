import json
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
    "call" : "كيف يمكنني المساعدة ؟ 😀",
    "warn": u"❌ لقد استعمل {name} احد الكلمات المحظورة ❌\n"
            u" 🔴 تبقى لديك {safeCounter} فرص اذا تم تجاوز العدد سيتم طردك 🔴",
    "kicked": u"👮‍♂️⚠ لقد تم طرد العضو {name} صاحب المعرف {username} بسبب مخالفته لاحد قواعد المجموعة 👮‍♂️⚠"
            

}

text_list={
    "offensive":["cat","puppy"]
}

commands = {
    "translate":["translate","trans","ترجم","ترجملي"]
}
def handleNewUserData(message):
    id = str(message.new_chat_member.user.id)
    name = message.new_chat_member.user.first_name
    username =  message.new_chat_member.user.username

    with open("data.json","r") as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    
    users = data["users"]
    if id not in users:
        print("new user detected !")
        users[id] = {"safeCounter":5}
        users[id]["username"] = username
        users[id]["name"] = name
        print("new user data saved !")

    data["users"] = users
    with open("data.json","w") as editedFile:
        json.dump(data,editedFile,indent=3)
    editedFile.close()    

def handleOffensiveMessage(message):
    id = str(message.from_user.id)
    name = message.from_user.first_name
    username =  message.from_user.username
    
    with open("data.json","r") as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    
    users = data["users"]
    if id not in users:
        print("new user detected !")
        users[id] = {"safeCounter":5}
        users[id]["username"] = username
        users[id]["name"] = name
        print("new user data saved !")

    for index in users:
        if index == id :
            print("guilty user founded !")
            users[id]["safeCounter"] -= 1

    safeCounterFromJson = users[id]["safeCounter"]
    if safeCounterFromJson == 0:
        bot.kick_chat_member(message.chat.id,id)
        users.pop(id)
        bot.send_message(message.chat.id,text_messages["kicked"].format(name=name , username = username))
    else:
        bot.send_message(message.chat.id,text_messages["warn"].format(name=name , safeCounter = safeCounterFromJson))

    data["users"] = users
    with open("data.json","w") as editedFile:
        json.dump(data,editedFile,indent=3)
    editedFile.close()

    return bot.delete_message(message.chat.id,message.message_id)
       
@bot.message_handler(commands=["start","help"])
def startBot(message):
    bot.send_message(message.chat.id,text_messages["welcome"])

#* saying Welcome to joined members
#* saying goodbye to left members
@bot.chat_member_handler()
def handleUserUpdates(message:types.ChatMemberUpdated):
    newResponse = message.new_chat_member
    if newResponse.status == "member":
        handleNewUserData(message=message)
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
    
    for word in words:
        if word in text_list["offensive"]:
            handleOffensiveMessage(message=message)
        

#* : checking if any word in message is offensive print("offensive")
#* : creating a data json file reading/writing 
#* : saving users info from message (id,name,username)
#* : adding safeCounter data to each user safeCounter = TRIES
#* : kick chat member that break the rules

bot.infinity_polling(allowed_updates=util.update_types)