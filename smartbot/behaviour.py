# coding: utf-8

import time

class Behaviour(object):
    def __init__(self, bot):
        self.bot = bot
        self.loaded = False
        self.debug = True

    def load(self):
        if not self.loaded:
            self.addHandlers()
            self.loaded = True
            self.logDebug('Behaviour loaded')
            self.onLoad()

    def unload(self):
        if self.loaded:
            self.removeHandlers()
            self.loaded = False
            self.logDebug('Behaviour unloaded')
            self.onUnload()

    def logDebug(self, message):
        if self.debug:
            print '%s %s: %s' % (time.strftime('%D %T'), self.__class__.__name__, message)

    def onLoad(self):
        None

    def onUnload(self):
        None

    def addHandlers(self):
        None

    def removeHandlers(self):
        None
