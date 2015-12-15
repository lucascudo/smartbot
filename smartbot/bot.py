# coding: utf-8

import io
import requests
import telegram

class Bot:
    def __init__(self, token):
        self.baseUrl = 'https://api.telegram.org/bot'
        self.token = token
        self.telegramBot = telegram.Bot(token=token)
        self.updater = telegram.Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.info = None

    def getInfo(self):
        self.info = self.info or self.telegramBot.getMe()
        return self.info

    def addMessageHandler(self, handler):
        self.dispatcher.addTelegramMessageHandler(handler)

    def removeMessageHandler(self, handler):
        self.dispatcher.removeTelegramMessageHandler(handler)

    def addCommandHandler(self, command, handler):
        self.dispatcher.addTelegramCommandHandler(command, handler)

    def removeCommandHandler(self, command, handler):
        self.dispatcher.removeTelegramCommandHandler(command, handler)

    def sendMessage(self, **params):
        return self.telegramBot.sendMessage(**params)

    def sendVoice(self, **kargs):
        files = { 'chat_id': ('', io.StringIO(unicode(str(kargs['chat_id'])))),
                'voice': ('voice.ogg', open(kargs['voice'], 'rb'), 'application/octet-stream') }
        return requests.post('%s%s/sendVoice' % (self.baseUrl, self.token), files=files)

    def sendAudio(self, **kargs):
        files = { 'chat_id': ('', io.StringIO(unicode(str(kargs['chat_id'])))),
                'performer': ('', io.StringIO(unicode(str(kargs.get('performer') or 'bot')))),
                'title': ('', io.StringIO(unicode(str(kargs.get('title') or 'talk')))),
                'mime_type': ('', io.StringIO(u'audio/mpeg')),
                'audio': ('audio.mp3', open(kargs['audio'], 'rb'), 'application/octet-stream') }
        return requests.post('%s%s/sendAudio' % (self.baseUrl, self.token), files=files)

    def listen(self):
        self.updater.start_polling()
