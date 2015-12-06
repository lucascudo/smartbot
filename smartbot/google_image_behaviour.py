# coding: utf-8

from smartbot import Behaviour

import re
from lxml import html
import requests
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
        self.logDebug('Image search (chat_id: %s, query: %s)' % (update.message.chat_id, query or 'None'))
        response = requests.get('https://www.google.com.br/search?site=&tbm=isch&q=%s&oq=%s&tbs=isz:l' % (query, query))
        tree = html.fromstring(response.content)
        image_tags = tree.xpath('//img')
        image_sources = map(lambda img: img.attrib['src'], image_tags)
        p = re.compile('.*gstatic.*')
        image_sources = filter(lambda source: p.match(source), image_sources)
        telegramBot.sendMessage(chat_id=update.message.chat_id, text=random.choice(image_sources))
