# coding: utf-8

from smartbot import Behaviour
from smartbot import ExternalAPI

import re
import random

class NasaBehaviour(Behaviour):
    def __init__(self, bot):
        super(NasaBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher;

    def addHandlers(self):
        self.dispatcher.addTelegramCommandHandler('nasa', self.nasaSearch)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('nasa', self.nasaSearch)

    def nasaSearch(self, telegramBot, update):
        self.logDebug(u'Nasa search (chat_id: %s)' % update.message.chat_id)
        nasaData = ExternalAPI.getNasaIOD()
        if nasaData:
            telegramBot.sendMessage(chat_id=update.message.chat_id, text=nasaData['imageSource'])
            telegramBot.sendMessage(chat_id=update.message.chat_id, text=nasaData['explanation'])
        else:
            telegramBot.sendMessage(chat_id=update.message.chat_id, text='Não encontrei imagem da nasa')
