# coding: utf-8

from smartbot import Behaviour

import re

class BasicBehaviour(Behaviour):
    __active_chats = []

    def __init__(self, bot, updater):
        super(BasicBehaviour, self).__init__(bot, updater)
        self.dispatcher = updater.dispatcher;

    def addHandlers(self):
        self.me = self.bot.getMe()
        self.dispatcher.addTelegramCommandHandler('start', self.start)
        self.dispatcher.addTelegramCommandHandler('stop', self.stop)
        self.dispatcher.addTelegramMessageHandler(self.message)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('start', self.start)
        self.dispatcher.removeTelegramCommandHandler('stop', self.stop)
        self.dispatcher.removeTelegramMessageHandler(self.message)

    def start(self, bot, update):
        self.__active_chats.append(update.message.chat_id)
        bot.sendMessage(chat_id=update.message.chat_id, text="tâmu juntu")

    def stop(self, bot, update):
        self.__active_chats.remove(update.message.chat_id)
        bot.sendMessage(chat_id=update.message.chat_id, text="gudibai !")

    def message(self, bot, update):
        bot_rec = re.compile('@' + self.me.username, re.IGNORECASE)
        if bot_rec.match(update.message.text):
            if update.message.chat_id in self.__active_chats:
                bot.sendMessage(chat_id=update.message.chat_id, text="iscutei")
            else:
                bot.sendMessage(chat_id=update.message.chat_id, text="tô durminu")
