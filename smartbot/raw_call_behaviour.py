# coding: utf-8

from smartbot import Behaviour
from smartbot import ExternalAPI

import re

class RawCallBehaviour(Behaviour):
    def __init__(self, bot):
        super(RawCallBehaviour, self).__init__(bot)

    def addHandlers(self):
        self.bot.addCommandHandler('raw_call', self.rawCall)

    def removeHandlers(self):
        self.bot.removeCommandHandler('raw_call', self.rawCall)

    def rawCall(self, telegramBot, update):
        p = re.compile('([^ ]*) (.*)')
        paramSentence = p.match(update.message.text).groups()[1]
        if paramSentence:
            q = re.compile('\s+')
            paramsRaw = q.split(paramSentence)
            if len(paramsRaw) > 0:
                self.logDebug(u'RawCall (chat_id: %s, query: %s, source_language: pt)' % (update.message.chat_id, paramSentence or 'None'))
                params = filter(lambda paramRaw: not re.search('=', paramRaw), paramsRaw)
                kparams = filter(lambda paramRaw: re.search('=', paramRaw), paramsRaw)
                kparams = dict(map(lambda paramRaw: tuple(re.split('=', paramRaw)), kparams))
                self.bot.executeRawCall(*params, **kparams)
