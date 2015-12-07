# coding: utf-8

import io
import requests
import telegram

class Bot:
    def __init__(self, token):
        self.token = token
        self.telegramBot = telegram.Bot(token=token)
        self.updater = telegram.Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.info = None

    def getInfo(self):
        self.info = self.info or self.telegramBot.getMe()
        return self.info

    def sendMessage(self, **params):
        return self.telegramBot.sendMessage(**params)

    def sendVoice(self, **kargs):
        files = { 'chat_id': ('', io.StringIO(unicode(str(kargs['chat_id'])))), 'voice': ('voice.ogg', open(kargs['voice'], 'rb'), 'application/octet-stream') }
        requests.post('https://api.telegram.org/bot' + self.token + '/sendVoice', files=files)

    def listen(self):
        self.updater.start_polling()
