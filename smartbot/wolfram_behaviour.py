# coding: utf-8

from smartbot import Behaviour
from smartbot import ExternalAPI

import re

class WolframBehaviour(Behaviour):
    def __init__(self, bot, wolframAppId):
        super(WolframBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher;
        self.wolframAppId = wolframAppId

    def addHandlers(self):
        self.dispatcher.addTelegramCommandHandler('wolfram', self.wolfram)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('wolfram', self.wolfram)

    def query(self, queryEnglish):
        return ExternalAPI.wolframQuery(queryEnglish, appId=self.wolframAppId)

    def wolfram(self, telegramBot, update):
        p = re.compile('([^ ]*) (.*)')
        queryEnglish = (p.match(update.message.text).groups()[1] or '').strip()
        self.logDebug(u'Wolfram query (chat_id: %s, query: %s)' % (update.message.chat_id, queryEnglish or 'None'))
        answerEnglish = self.query(queryEnglish)
        answerEnglish = (answerEnglish or '').replace('\n', '. ')
        if answerEnglish:
            answerPortuguese = ExternalAPI.translate(answerEnglish, fromLanguage='en')
            if answerPortuguese:
                self.bot.sendMessage(chat_id=update.message.chat_id, text=answerPortuguese)
            else:
                self.bot.sendMessage(chat_id=update.message.chat_id, text='Não entendi')
