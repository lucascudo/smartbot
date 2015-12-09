# coding: utf-8

from smartbot import Behaviour
from smartbot import ExternalAPI

import re
import os

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
        if len(words) > 1 and words[0] in self.vocabulary.keys():
            params = words[1:]
            self.logDebug(u'Friendly mention (chat_id: %s, keywords: %s, params: %s)' % (update.message.chat_id, ('|').join(keywords), (' ').join(params or ['None'])))
            command = self.vocabulary[keywords[0]]
            updateMock = DynObject()
            updateMock.message = DynObject()
            updateMock.message.chat_id = update.message.chat_id
            updateMock.message.text = '/%s %s' % (command, ' '.join(params))
            self.dispatcher.dispatchTelegramCommand(updateMock)
        elif len(words) == 1:
            telegramBot.sendMessage(chat_id=update.message.chat_id, text='Não entendi')
        else:
            sentence = ' '.join(words)
            sentenceEnglish = ExternalAPI.translate(sentence.encode('utf-8'), fromLanguage='pt')
            answerEnglish = ExternalAPI.wolframQuery(sentenceEnglish, appId=os.environ.get('WOLFRAM_APP_ID'))
            if answerEnglish:
                answerEnglish = re.sub('Wolfram\|Alpha', self.bot.getInfo().username, answerEnglish)
                answerPortuguese = ExternalAPI.translate(answerEnglish.encode('utf-8'), fromLanguage='en')
                telegramBot.sendMessage(chat_id=update.message.chat_id, text=answerPortuguese)
            else:
                telegramBot.sendMessage(chat_id=update.message.chat_id, text='Nada a dizer sobre isso')
