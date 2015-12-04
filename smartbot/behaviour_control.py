# coding: utf-8

class BehaviourControl(object):
    def __init__(self, bot):
        self.bot = bot
        self.behaviours = {}
        self.loaded_behaviours = {}

    def add(self, behaviour_name, behaviour_class):
        self.behaviours[behaviour_name] = behaviour_class

    def remove(self, behaviour_name):
        self.behaviours.pop(behaviour_name)

    def load(self, behaviour_name):
        behaviour = self.behaviours[behaviour_name](self.bot)
        behaviour.load()
        self.loaded_behaviours[behaviour_name] = behaviour
        return behaviour

    def unload(self, behaviour_name):
        self.loaded_behaviours[behaviour_name].unload()
        self.loaded_behaviours.pop(behaviour_name)
