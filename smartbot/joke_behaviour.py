# coding: utf-8

from smartbot import Behaviour
from smartbot import Utils

import re
import random

class JokeBehaviour(Behaviour):
    def __init__(self, bot):
        super(JokeBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher;

    def addHandlers(self):
        self.dispatcher.addTelegramCommandHandler('joke', self.jokeSearch)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('joke', self.jokeSearch)

    def jokeSearch(self, telegramBot, update):
        p = re.compile('([^ ]*) (.*)')
        query = (p.match(update.message.text).groups()[1] or '').strip()
        self.logDebug('Joke search (chat_id: %s, query: %s)' % (update.message.chat_id, query or 'None'))
        if query:
            tree = Utils.crawlUrl('http://www.piadasnet.com/index.php?pesquisaCampo=%s&btpesquisa=OK&pesquisaInicio=0' % query)
        else:
            tree = Utils.crawlUrl('http://www.piadasnet.com/')
        jokeTags = tree.xpath('//*[contains(@class, "piada")]')
        if jokeTags:
            telegramBot.sendMessage(chat_id=update.message.chat_id, text=random.choice(jokeTags).text_content())
