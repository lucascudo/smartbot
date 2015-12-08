# coding: utf-8

from smartbot import Behaviour
from smartbot import ExternalAPI

import re

class GoogleImageBehaviour(Behaviour):
    def __init__(self, bot):
        super(GoogleImageBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher;

    def addHandlers(self):
        self.dispatcher.addTelegramCommandHandler('image', self.imageSearch)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('image', self.imageSearch)

    def imageSearch(self, telegramBot, update):
        p = re.compile('([^ ]*) (.*)')
        query = (p.match(update.message.text).groups()[1] or '').strip()
        self.logDebug(u'Image search (chat_id: %s, query: %s)' % (update.message.chat_id, query or 'None'))
        imageSources = ExternalAPI.searchImage(query)
        if imageSources:
            telegramBot.sendMessage(chat_id=update.message.chat_id, text=imageSources[0])
        else:
            telegramBot.sendMessage(chat_id=update.message.chat_id, text='Não encontrei imagem relacionada')
