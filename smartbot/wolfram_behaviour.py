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

    def wolfram(self, telegramBot, update):
        p = re.compile('([^ ]*) (.*)')
        queryPortuguese = (p.match(update.message.text).groups()[1] or '').strip()
        self.logDebug(u'Wolfram query (chat_id: %s, query: %s)' % (update.message.chat_id, queryPortuguese or 'None'))
        print queryPortuguese
        queryEnglish = ExternalAPI.translate(queryPortuguese, fromLanguage='pt')
        print queryEnglish
        answerEnglish = ExternalAPI.wolframQuery(queryEnglish, appId=self.wolframAppId)
        answerEnglish = answerEnglish.replace('\n', '. ')
        print answerEnglish
        if answerEnglish:
            answerPortuguese = ExternalAPI.translate(answerEnglish, fromLanguage='en')
            print answerPortuguese
            if answerPortuguese:
                telegramBot.sendMessage(chat_id=update.message.chat_id, text=answerPortuguese)
            else:
                telegramBot.sendMessage(chat_id=update.message.chat_id, text='Não entendi')
