# coding: utf-8

from smartbot import Behaviour
from smartbot import Utils

import re
import random

class GoogleImageBehaviour(Behaviour):
    def __init__(self, bot):
        super(GoogleImageBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher;

    def addHandlers(self):
        self.dispatcher.addTelegramCommandHandler('image', self.imageSearch)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('image', self.imageSearch)

    def imageSearch(self, telegramBot, update):
        p = re.compile('([^ ]*) (.*)')
        query = (p.match(update.message.text).groups()[1] or '').strip()
        self.logDebug(u'Image search (chat_id: %s, query: %s)' % (update.message.chat_id, query or 'None'))
        tree = Utils.crawlUrl('https://www.google.com.br/search?site=&tbm=isch&q=%s&oq=%s&tbs=isz:l' % (query, query))
        imageTags = tree.xpath('//img')
        imageSources = map(lambda img: img.attrib['src'], imageTags)
        p = re.compile('.*gstatic.*')
        imageSources = filter(lambda source: p.match(source), imageSources)
        telegramBot.sendMessage(chat_id=update.message.chat_id, text=random.choice(imageSources))
