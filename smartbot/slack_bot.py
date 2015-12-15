# coding: utf-8

import io
import re
import sys
import time
import json
import requests
import slackclient
from smartbot import Bot
from smartbot import Utils

class DynObject(object):
    pass

class SlackBot(Bot):
    def __init__(self, token):
        super(SlackBot, self).__init__(token)
        self.slackClient = slackclient.SlackClient(token)
        self._commandMatcher = re.compile('^_(\w+)( .*)?$')
        self._messageHandlers = []
        self._regexHandlers = []
        self._commandHandlers = []
        self.info = None

    def getInfo(self):
        if not self.info:
            slackInfo = json.loads(self.slackClient.api_call('auth.test'))
            self.info = DynObject()
            self.info.id = slackInfo.get('user_id')
            self.info.username = self.info.first_name = slackInfo.get('user')
        return self.info

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
        self.slackClient.api_call('chat.postMessage', channel=channel, username=self.getInfo().username, icon_emoji=':robot_face:', text=text.encode('utf-8'))

    def sendVoice(self, **kargs):
        Utils.logDebug(self, self.__class__.__name__, 'sendVoice %s' % kargs)

    def sendAudio(self, **kargs):
        Utils.logDebug(self, self.__class__.__name__, 'sendAudio %s' % kargs)

    def dispatchMessage(self, update):
        dispatched = False
        for messageHandler in self._messageHandlers:
            handler = messageHandler[0]
            handler(self, update)
            dispatched = True
        return dispatched

    def dispatchRegex(self, update):
        dispatched = False
        for regexHandler in self._regexHandlers:
            regex = regexHandler[0]
            handler = regexHandler[1]
            if regex.match(update.message.text):
                handler(self, update)
                dispatched = True
        return dispatched

    def dispatchCommand(self, update, command=None):
        dispatched = False
        commandMatches = self._commandMatcher.match(update.message.text)
        if command or commandMatches:
            for commandHandler in self._commandHandlers:
                commandCurrent = commandHandler[0]
                handler = commandHandler[1]
                if command == commandCurrent or commandCurrent == commandMatches.groups()[0]:
                    handler(self, update)
                    dispatched = True
        return dispatched

    def processUpdate(self, update):
        if update.type == 'message':
            if not self.dispatchCommand(update):
                self.dispatchMessage(update)
                self.dispatchRegex(update)

    def convertToUpdate(self, slackEvent):
        update = DynObject()
        if slackEvent.get(u'type') == 'message' and not slackEvent.get(u'subtype') == 'bot_message':
            update.type = 'message'
            update.message = DynObject()
            update.message.text = slackEvent.get(u'text') or ''
            update.message.chat_id = slackEvent.get(u'channel')
        else:
            update.type = 'unknown'
        return update

    def listen(self):
        try:
            if self.slackClient.rtm_connect():
                while True:
                    events = self.slackClient.rtm_read()
                    for event in events:
                        self.processUpdate(self.convertToUpdate(event))
                    time.sleep(0.5)
        except:
            Utils.logError(self, self.__class__.__name__, sys.exc_info())
