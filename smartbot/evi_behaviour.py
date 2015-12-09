# coding: utf-8

from smartbot import Behaviour
from smartbot import ExternalAPI

import re

class EviBehaviour(Behaviour):
    def __init__(self, bot):
        super(EviBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher;

    def addHandlers(self):
        self.dispatcher.addTelegramCommandHandler('evi', self.evi)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('evi', self.evi)

    def evi(self, telegramBot, update):
        p = re.compile('([^ ]*) (.*)')
        queryEnglish = (p.match(update.message.text).groups()[1] or '').strip()
        self.logDebug(u'Evi query (chat_id: %s, query: %s)' % (update.message.chat_id, queryEnglish or 'None'))
        answerEnglish = ExternalAPI.eviQuery(queryEnglish)
        answerEnglish = (answerEnglish or '').replace('\n', '. ')
        if answerEnglish:
            answerPortuguese = ExternalAPI.translate(answerEnglish, fromLanguage='en')
            if answerPortuguese:
                telegramBot.sendMessage(chat_id=update.message.chat_id, text=answerPortuguese)
            else:
                telegramBot.sendMessage(chat_id=update.message.chat_id, text='Não entendi')
