# coding: utf-8

class Behaviour(object):
    def __init__(self, bot):
        self.bot = bot
        self.loaded = False

    def load(self):
        if not self.loaded:
            self.addHandlers()
            self.loaded = True
            self.onLoad()

    def unload(self):
        if self.loaded:
            self.removeHandlers()
            self.loaded = False
            self.onUnload()

    def onLoad(self):
        None

    def onUnload(self):
        None

    def addHandlers(self):
        None

    def removeHandlers(self):
        None
