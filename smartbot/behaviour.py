# coding: utf-8

class Behaviour(object):
    def __init__(self, bot):
        self.bot = bot
        self.loaded = False

    def load(self):
        if not self.loaded:
            self.addHandlers()
            self.onLoad()
            self.loaded = True

    def unload(self):
        if self.loaded:
            self.removeHandlers()
            self.onUnload()
            self.loaded = False

    def onLoad(self):
        None

    def onUnload(self):
        None

    def addHandlers(self):
        None

    def removeHandlers(self):
        None
