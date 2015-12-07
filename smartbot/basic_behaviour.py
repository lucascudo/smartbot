# coding: utf-8

from smartbot import Behaviour
from smartbot import Utils

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
        self.dispatcher.addTelegramCommandHandler('debug', self.debug)
        self.dispatcher.addTelegramMessageHandler(self.message)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('start', self.start)
        self.dispatcher.removeTelegramCommandHandler('stop', self.stop)
        self.dispatcher.removeTelegramCommandHandler('debug', self.debug)
        self.dispatcher.removeTelegramMessageHandler(self.message)

    def start(self, telegramBot, update):
        self.__active_chats.append(update.message.chat_id)
        telegramBot.sendMessage(chat_id=update.message.chat_id, text="tâmu juntu")

    def stop(self, telegramBot, update):
        self.__active_chats.remove(update.message.chat_id)
        telegramBot.sendMessage(chat_id=update.message.chat_id, text="gudibai !")

    def debug(self, telegramBot, update):
        matcher = re.compile('([^ ]*) ?(here|\d+)? ?(on|off)?')
        groups = matcher.match(update.message.text).groups()
        if groups[2]:
            Utils.debug = True if (groups[2].lower() == 'on') else False
        elif groups[1]:
            Utils.debug = True
        else:
            Utils.debug = not Utils.debug
        if Utils.debug:
            Utils.debugOutput = update.message.chat_id if (groups[1] or 'here') == 'here' else groups[1]
            telegramBot.sendMessage(chat_id=update.message.chat_id, text="debug ON in %s" % Utils.debugOutput)
        else:
            Utils.debugOutput = None
            telegramBot.sendMessage(chat_id=update.message.chat_id, text="debug OFF")

    def message(self, telegramBot, update):
        bot_rec = re.compile('@' + self.botInfo.username, re.IGNORECASE)
        if bot_rec.match(update.message.text):
            if update.message.chat_id in self.__active_chats:
                telegramBot.sendMessage(chat_id=update.message.chat_id, text="iscutei")
            else:
                telegramBot.sendMessage(chat_id=update.message.chat_id, text="tô durminu")
