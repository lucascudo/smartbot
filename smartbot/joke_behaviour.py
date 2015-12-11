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
        jokes = ExternalAPI.searchJoke(query.encode('utf-8'))
        if jokes:
            telegramBot.sendMessage(chat_id=update.message.chat_id, text=random.choice(jokes))

    def jalkSearch(self, telegramBot, update):
        p = re.compile('([^ ]*) (.*)')
        query = (p.match(update.message.text).groups()[1] or '').strip()
        self.logDebug(u'Jalk search (chat_id: %s, query: %s)' % (update.message.chat_id, query or 'None'))
        jokes = ExternalAPI.searchJoke(query.encode('utf-8'))
        if jokes:
            jokes = filter(lambda c: len(re.split('\W+', c, re.MULTILINE)) < 200, jokes)
            jokes = sorted(jokes, lambda x, y: len(x) - len(y))
            if jokes:
                joke = jokes[0]
                audioFile = ExternalAPI.textToSpeech(joke.encode('utf-8'), language='pt', encode='mp3')
                if os.path.exists(audioFile) and os.path.getsize(audioFile) > 0:
                    self.bot.sendAudio(chat_id=update.message.chat_id, audio=audioFile, performer=self.bot.getInfo().username)
                else:
                    telegramBot.sendMessage(chat_id=update.message.chat_id, text='Não consigo contar')
            else:
                telegramBot.sendMessage(chat_id=update.message.chat_id, text='Não encontrei piada curta')
