# coding: utf-8

BEHAVIOURS = []
LOADED_BEHAVIOURS = []

class Behaviour(object):
    name = None

    def __init__(self, bot, updater):
        self.bot = bot
        self.updater = updater

    def load(self):
        self.addHandlers()

    def unload(self):
        self.removeHandlers()

    def addHandlers(self):
        None

    def removeHandlers(self):
        None
