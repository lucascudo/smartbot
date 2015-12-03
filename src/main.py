# coding: utf-8

import telegram
from telegram import Updater
updater = Updater(token='177224385:AAHwrklE9Yx-nrPvNaXRtGiEM5qH2UWuAKM')
dispatcher = updater.dispatcher

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="tâmo junto")

dispatcher.addTelegramCommandHandler('start', start)

updater.start_polling()
