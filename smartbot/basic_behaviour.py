# coding: utf-8

from smartbot import Behaviour

import re

class BasicBehaviour(Behaviour):
    __active_chats = []

    def __init__(self, bot):
        super(BasicBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher;

    def onLoad(self):
        self.botInfo = self.bot.getInfo()

    def addHandlers(self):
        self.dispatcher.addTelegramCommandHandler('start', self.start)
        self.dispatcher.addTelegramCommandHandler('stop', self.stop)
        self.dispatcher.addTelegramMessageHandler(self.message)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('start', self.start)
        self.dispatcher.removeTelegramCommandHandler('stop', self.stop)
        self.dispatcher.removeTelegramMessageHandler(self.message)

    def start(self, telegramBot, update):
        self.__active_chats.append(update.message.chat_id)
        telegramBot.sendMessage(chat_id=update.message.chat_id, text="tâmu juntu")

    def stop(self, telegramBot, update):
        self.__active_chats.remove(update.message.chat_id)
        telegramBot.sendMessage(chat_id=update.message.chat_id, text="gudibai !")

    def message(self, telegramBot, update):
        bot_rec = re.compile('@' + self.botInfo.username, re.IGNORECASE)
        if bot_rec.match(update.message.text):
            if update.message.chat_id in self.__active_chats:
                telegramBot.sendMessage(chat_id=update.message.chat_id, text="iscutei")
            else:
                telegramBot.sendMessage(chat_id=update.message.chat_id, text="tô durminu")
