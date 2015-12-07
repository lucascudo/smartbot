# coding: utf-8

from smartbot import Behaviour
from smartbot import ExternalAPI

import re

class TranslateBehaviour(Behaviour):
    def __init__(self, bot):
        super(TalkBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher;

    def addHandlers(self):
        self.dispatcher.addTelegramCommandHandler('talk', self.talk)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('talk', self.talk)

    def talk(self, telegramBot, update):
        p = re.compile('([^ ]*) (.*)')
        query = (p.match(update.message.text).groups()[1] or '').strip()
        self.logDebug(u'Talk (chat_id: %s, query: %s, source_language: pt)' % (update.message.chat_id, query or 'None'))
        audioFile = ExternalAPI.talk(query, 'pt')
        telegramBot.sendAudio(chat_id=update.message.chat_id, audio=audioFile)
