# coding: utf-8

from smartbot import Behaviour
from smartbot import Utils
from smartbot import ExternalAPI

import re
import os
import random

class JokeBehaviour(Behaviour):
    def __init__(self, bot):
        super(JokeBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher;

    def addHandlers(self):
        self.dispatcher.addTelegramCommandHandler('joke', self.jokeSearch)
        self.dispatcher.addTelegramCommandHandler('jalk', self.jalkSearch)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('joke', self.jokeSearch)
        self.dispatcher.removeTelegramCommandHandler('jalk', self.jalkSearch)

    def jokeSearch(self, telegramBot, update):
        p = re.compile('([^ ]*) (.*)')
        query = (p.match(update.message.text).groups()[1] or '').strip()
        self.logDebug(u'Joke search (chat_id: %s, query: %s)' % (update.message.chat_id, query or 'None'))
        if query:
            tree = Utils.crawlUrl('http://www.piadasnet.com/index.php?pesquisaCampo=%s&btpesquisa=OK&pesquisaInicio=0' % query)
        else:
            tree = Utils.crawlUrl('http://www.piadasnet.com/')
        jokeTags = tree.xpath('//*[contains(@class, "piada")]')
        if jokeTags:
            telegramBot.sendMessage(chat_id=update.message.chat_id, text=random.choice(jokeTags).text_content())

    def jalkSearch(self, telegramBot, update):
        p = re.compile('([^ ]*) (.*)')
        query = (p.match(update.message.text).groups()[1] or '').strip()
        self.logDebug(u'Jalk search (chat_id: %s, query: %s)' % (update.message.chat_id, query or 'None'))
        if query:
            tree = Utils.crawlUrl('http://www.piadasnet.com/index.php?pesquisaCampo=%s&btpesquisa=OK&pesquisaInicio=0' % query)
        else:
            tree = Utils.crawlUrl('http://www.piadasnet.com/')
        jokeTags = tree.xpath('//*[contains(@class, "piada")]')
        if jokeTags:
            contents = map(lambda c: c.text_content(), jokeTags)
            contents = filter(lambda c: len(re.split('\W+', c, re.MULTILINE)) < 70, contents)
            contents = sorted(contents, lambda x, y: len(x) - len(y))
            if contents:
                content = contents[0]
                audioFile = ExternalAPI.talk(content, 'pt')
                if os.path.exists(audioFile) and os.path.getsize(audioFile) > 0:
                    self.bot.sendVoice(chat_id=update.message.chat_id, voice=audioFile)
                else:
                    telegramBot.sendMessage(chat_id=update.message.chat_id, text='Não consigo contar')
            else:
                telegramBot.sendMessage(chat_id=update.message.chat_id, text='Não encontrei piada curta')
