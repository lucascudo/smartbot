# coding: utf-8

from smartbot import Behaviour

import re

class LoaderBehaviour(Behaviour):
    def __init__(self, bot, behaviour_control):
        super(LoaderBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher;
        self.behaviour_control = behaviour_control

    def addHandlers(self):
        self.dispatcher.addTelegramCommandHandler('load', self.load_behaviour)
        self.dispatcher.addTelegramCommandHandler('unload', self.unload_behaviour)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('load', self.load_behaviour)
        self.dispatcher.removeTelegramCommandHandler('unload', self.unload_behaviour)

    def load_behaviour(self, telegramBot, update):
        p = re.compile('(.*) (.*)')
        behaviour_name = p.match(update.message.text).groups()[1]
        self.behaviour_control.load(behaviour_name)

    def unload_behaviour(self, telegramBot, update):
        p = re.compile('(.*) (.*)')
        behaviour_name = p.match(update.message.text).groups()[1]
        self.behaviour_control.unload(behaviour_name)
