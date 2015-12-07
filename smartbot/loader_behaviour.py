# coding: utf-8

from smartbot import Behaviour

import re

class LoaderBehaviour(Behaviour):
    def __init__(self, bot, behaviourControl):
        super(LoaderBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher;
        self.behaviourControl = behaviourControl

    def addHandlers(self):
        self.dispatcher.addTelegramCommandHandler('load', self.loadBehaviour)
        self.dispatcher.addTelegramCommandHandler('unload', self.unloadBehaviour)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('load', self.loadBehaviour)
        self.dispatcher.removeTelegramCommandHandler('unload', self.unloadBehaviour)

    def loadBehaviour(self, telegramBot, update):
        p = re.compile('([^ ]*) (.*)')
        behaviourName = (p.match(update.message.text).groups()[1] or '').strip()
        if behaviourName == 'all':
            self.behaviourControl.loadAll()
        elif self.behaviourControl.getStatus(behaviourName) == 'unloaded':
            self.behaviourControl.load(behaviourName)

    def unloadBehaviour(self, telegramBot, update):
        p = re.compile('(.*) (.*)')
        behaviourName = (p.match(update.message.text).groups()[1] or '').strip()
        if self.behaviourControl.getStatus(behaviourName) == 'loaded':
            self.behaviourControl.unload(behaviourName)
