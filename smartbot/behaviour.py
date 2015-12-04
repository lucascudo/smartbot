# coding: utf-8

class Behaviour(object):
    def __init__(self, bot):
        self.bot = bot

    def load(self):
        self.addHandlers()
        self.onLoad()

    def unload(self):
        self.removeHandlers()
        self.onUnload()

    def onLoad(self):
        None

    def onUnload(self):
        None

    def addHandlers(self):
        None

    def removeHandlers(self):
        None
