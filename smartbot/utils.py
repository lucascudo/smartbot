# coding: utf-8

import time
from lxml import html
import requests

class Utils:
    debug = False
    debugOutput = None

    @staticmethod
    def crawlUrl(url):
        response = requests.get(url)
        return html.fromstring(response.content)

    @staticmethod
    def logDebug(bot, className, message):
        output = u'%s %s: %s' % (time.strftime('%D %T'), className, message)
        print u'%s' % output
        if Utils.debug:
            bot.sendMessage(chat_id=Utils.debugOutput, text=output)
