# coding: utf-8

import io
import re
import sys
import time
import requests
import slackclient
from smartbot import Bot
from smartbot import Utils

class DynObject(object):
    pass

class SlackBot(Bot):
    def __init__(self, token, name='bot'):
        super(SlackBot, self).__init__(token)
        self.name = name
        self.slackClient = slackclient.SlackClient(token)
        self._commandMatcher = re.compile('^_(\w+)( .*)?$')
        self._messageHandlers = []
        self._regexHandlers = []
        self._commandHandlers = []
        self.info = None

    def getInfo(self):
        info = DynObject()
        info.username = info.first_name = self.name
        return info

    def addMessageHandler(self, handler):
        self._messageHandlers.append((handler,))

    def removeMessageHandler(self, handler):
        self._messageHandlers.remove((handler,))

    def addRegexHandler(self, matcher, handler):
        self._regexHandlers.append((matcher, handler))

    def removeRegexHandler(self, matcher, handler):
        self._regexHandlers.remove((matcher, handler))

    def addCommandHandler(self, command, handler):
        self._commandHandlers.append((command, handler))

    def removeCommandHandler(self, command, handler):
        self._commandHandlers.remove((command, handler))

    def sendMessage(self, **kargs):
        channel = kargs.get('chat_id')
        text = kargs.get('text') or ''
        Utils.logDebug(self, self.__class__.__name__, 'sendMessage %s' % kargs)
        self.slackClient.api_call('chat.postMessage', channel=channel, text=text.encode('utf-8'))

    def sendVoice(self, **kargs):
        Utils.logDebug(self, self.__class__.__name__, 'sendVoice %s' % kargs)

    def sendAudio(self, **kargs):
        Utils.logDebug(self, self.__class__.__name__, 'sendAudio %s' % kargs)

    def dispatchMessage(self, update):
        for messageHandler in self._messageHandlers:
            handler = messageHandler[0]
            handler(self, update)

    def dispatchRegex(self, update):
        for regexHandler in self._regexHandlers:
            regex = regexHandler[0]
            handler = regexHandler[1]
            if regex.match(update.message.text):
                handler(self, update)

    def dispatchCommand(self, update, command=None):
        commandMatches = self._commandMatcher.match(update.message.text)
        if command or commandMatches:
            for commandHandler in self._commandHandlers:
                command = command or commandHandler[0]
                handler = commandHandler[1]
                if command == commandMatches.groups()[0]:
                    handler(self, update)

    def processUpdate(self, update):
        if update.type == 'message':
            self.dispatchMessage(update)
            self.dispatchRegex(update)
            self.dispatchCommand(update)

    def convertToUpdate(self, slackEvent):
        update = DynObject()
        if slackEvent.get(u'type') == 'message':
            update.type = 'message'
            update.message = DynObject()
            update.message.text = slackEvent.get(u'text') or ''
            update.message.chat_id = slackEvent.get(u'channel')
        else:
            update.type = 'unknown'
        return update

    def listen(self):
        mentionMatcher = re.compile('.*(^|\W)(%s)($|\W).*' % self.name, re.IGNORECASE)
        try:
            if self.slackClient.rtm_connect():
                while True:
                    events = self.slackClient.rtm_read()
                    for event in events:
                        self.processUpdate(self.convertToUpdate(event))
                    time.sleep(1)
        except:
            Utils.logError(self, self.__class__.__name__, sys.exc_info())
