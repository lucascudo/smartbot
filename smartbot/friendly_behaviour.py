# coding: utf-8

from smartbot import Behaviour
from smartbot import ExternalAPI

import re
import os
from threading import Thread

class DynObject(object):
    pass

class FriendlyBehaviour(Behaviour):
    __active_chats = []

    def __init__(self, bot, behaviourControl, vocabulary={}):
        super(FriendlyBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher
        self.behaviourControl = behaviourControl
        self.vocabulary = vocabulary

    def addHandlers(self):
        info = self.bot.getInfo()
        self.botInfo = info
        self.mentionMatcher = re.compile('.*(^|\W)@?(%s|%s)(\W|$).*' % (info.username, info.username.lower().replace('bot', '')), re.IGNORECASE)
        # self.dispatcher.addTelegramRegexHandler(self.mentionMatcher, self.mention)
        self.dispatcher.addTelegramMessageHandler(self.mention)

    def removeHandlers(self):
        # self.dispatcher.removeTelegramRegexHandler(self.mentionMatcher, self.mention)
        self.dispatcher.removeTelegramMessageHandler(self.mention)

    def mention(self, telegramBot, update):
        message = update.message.text
        words = re.compile('\s+', re.UNICODE).split(message)
        words = filter(lambda word: word.strip() and not self.mentionMatcher.match(word), words)
        words = map(lambda word: word.lower(), words)
        keywords = self.vocabulary.keys()
        if len(words) >= 1 and words[0] in keywords:
            command = self.vocabulary[words[0]]
            params = words[1:]
            self.logDebug(u'Friendly mention (chat_id: %s, command: %s, params: %s)' % (update.message.chat_id, command, (' ').join(params or ['None'])))
            updateMock = DynObject()
            updateMock.message = DynObject()
            updateMock.message.chat_id = update.message.chat_id
            updateMock.message.text = '/%s %s' % (command, ' '.join(params))
            self.dispatcher.dispatchTelegramCommand(updateMock)
        elif len(words) == 1:
            telegramBot.sendMessage(chat_id=update.message.chat_id, text='Não entendi')
        else:
            sentence = ' '.join(words)
            bc = self.behaviourControl
            results = []
            sentenceEnglish = ExternalAPI.translate(sentence, fromLanguage='pt') or ''
            target = lambda behaviour, sentence: bc.getStatus(behaviour) == 'loaded' and results.append({'source': behaviour, 'answer': bc.get(behaviour).query(sentence)})
            t1 = Thread(target=target, args=('evi', sentenceEnglish))
            t2 = Thread(target=target, args=('wolfram', sentenceEnglish))
            map(lambda t: t.start(), [t1, t2])
            map(lambda t: t.join(), [t1, t2])
            results = filter(lambda result: result['answer'] and result['answer'].strip(), results)
            results = sorted(results, lambda x, y: len(x['answer']) - len(y['answer']))
            if results:
                result = results[0]
                self.logDebug(u'Friendly answer (chat_id: %s, sentence: %s, sentenceEnglish: %s, answers: %s, choosen: %s)' % (update.message.chat_id, sentence, sentenceEnglish.decode('utf-8'), results, result['source']))
                answerEnglish = result['answer']
                answerEnglish = re.sub('(Wolfram\|Alpha|Evi)', self.bot.getInfo().username, answerEnglish)
                answerPortuguese = ExternalAPI.translate(answerEnglish, fromLanguage='en')
                telegramBot.sendMessage(chat_id=update.message.chat_id, text=answerPortuguese)
            else:
                self.logDebug(u'Friendly answer (chat_id: %s, sentence: %s, sentenceEnglish: %s, answers: None)' % (update.message.chat_id, sentence, sentenceEnglish.decode('utf-8')))
                telegramBot.sendMessage(chat_id=update.message.chat_id, text='Prefiro não comentar')
