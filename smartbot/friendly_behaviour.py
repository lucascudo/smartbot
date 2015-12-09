# coding: utf-8

from smartbot import Behaviour

import re

class DynObject(object):
    pass

class FriendlyBehaviour(Behaviour):
    __active_chats = []

    def __init__(self, bot, vocabulary={}):
        super(FriendlyBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher
        self.vocabulary = vocabulary

    def addHandlers(self):
        info = self.bot.getInfo()
        self.botInfo = info
        self.mentionMatcher = re.compile('.*(^|\W)@?(%s|%s)(\W|$).*' % (info.username, info.username.lower().replace('bot', '')), re.IGNORECASE)
        self.dispatcher.addTelegramRegexHandler(self.mentionMatcher, self.mention)

    def removeHandlers(self):
        self.dispatcher.removeTelegramRegexHandler(self.mentionMatcher, self.mention)

    def mention(self, telegramBot, update):
        message = update.message.text
        words = re.compile('\W', re.UNICODE).split(message)
        words = filter(lambda word: not self.mentionMatcher.match(word), words)
        words = map(lambda word: word.lower(), words)
        keywords = list(set(self.vocabulary.keys()).intersection(words))
        params = filter(lambda word: word and not word in keywords, words)
        if keywords:
            self.logDebug(u'Friendly mention (chat_id: %s, keywords: %s, params: %s)' % (update.message.chat_id, ('|').join(keywords), (' ').join(params or ['None'])))
            command = self.vocabulary[keywords[0]]
            updateMock = DynObject()
            updateMock.message = DynObject()
            updateMock.message.chat_id = update.message.chat_id
            updateMock.message.text = '/%s %s' % (command, ' '.join(params))
            self.dispatcher.dispatchTelegramCommand(updateMock)
