# coding: utf-8

import telegram

class Bot:
    def __init__(self, token):
        self.telegramBot = telegram.Bot(token=token)
        self.updater = telegram.Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.info = None

    def getInfo(self):
        self.info = self.info or self.telegramBot.getMe()
        return self.info

    def listen(self):
        self.updater.start_polling()
