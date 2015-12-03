# coding: utf-8

import re
import telegram
from telegram import Updater
from telegram import Bot

bot = Bot(token='177224385:AAHwrklE9Yx-nrPvNaXRtGiEM5qH2UWuAKM')
updater = Updater(token='177224385:AAHwrklE9Yx-nrPvNaXRtGiEM5qH2UWuAKM')

dispatcher = updater.dispatcher

me = bot.getMe()

active_chats=[]

print me.username

bot_rec = re.compile('@' + me.username, re.IGNORECASE)

def start(bot, update):
    active_chats.append(update.message.chat_id)
    bot.sendMessage(chat_id=update.message.chat_id, text="tâmo junto")

def stop(bot, update):
    active_chats.remove(update.message.chat_id)
    bot.sendMessage(chat_id=update.message.chat_id, text="gudibai !")

def message(bot, update):
    if bot_rec.match(update.message.text):
        if update.message.chat_id in active_chats:
            bot.sendMessage(chat_id=update.message.chat_id, text="iscutei")
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="tô durminu")

dispatcher.addTelegramCommandHandler('start', start)
dispatcher.addTelegramCommandHandler('stop', stop)
dispatcher.addTelegramMessageHandler(message)

updater.start_polling()
