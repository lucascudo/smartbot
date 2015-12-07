# coding: utf-8

class BehaviourControl(object):
    def __init__(self, bot):
        self.bot = bot
        self.behaviours = {}
        self.loaded_behaviours = {}

    def add(self, behaviour_name, behaviour):
        behaviour = self.behaviours[behaviour_name] = behaviour
        return behaviour

    def remove(self, behaviour_name):
        return self.behaviours.pop(behaviour_name)

    def hasBehaviour(self, behaviour_name):
        return not not self.behaviours.get(behaviour_name)

    def getStatus(self, behaviour_name):
        if not self.hasBehaviour(behaviour_name):
            return 'unknown'
        elif behaviour_name in self.loaded_behaviours:
            return 'loaded'
        else:
            return 'unloaded'

    def load(self, behaviour_name):
        behaviour = self.behaviours[behaviour_name]
        behaviour.load()
        self.loaded_behaviours[behaviour_name] = behaviour
        return behaviour

    def unload(self, behaviour_name):
        self.loaded_behaviours[behaviour_name].unload()
        return self.loaded_behaviours.pop(behaviour_name)
