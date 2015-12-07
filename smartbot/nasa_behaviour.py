# coding: utf-8

from smartbot import Behaviour
from smartbot import Utils

import re
import random

class NasaBehaviour(Behaviour):
    def __init__(self, bot):
        super(NasaBehaviour, self).__init__(bot)
        self.dispatcher = bot.dispatcher;

    def addHandlers(self):
        self.dispatcher.addTelegramCommandHandler('nasa', self.nasaSearch)

    def removeHandlers(self):
        self.dispatcher.removeTelegramCommandHandler('nasa', self.nasaSearch)

    def nasaSearch(self, telegramBot, update):
        self.logDebug('Nasa search (chat_id: %s)' % update.message.chat_id)
        tree = Utils.crawlUrl('http://apod.nasa.gov')
        image_tags = tree.xpath('//img[contains(@src,"image")]')
        p_tags = tree.xpath('//p')
        if image_tags:
            telegramBot.sendMessage(chat_id=update.message.chat_id, text='http://apod.nasa.gov/%s' % random.choice(image_tags).attrib['src'])
            telegramBot.sendMessage(chat_id=update.message.chat_id, text=p_tags[2].text_content())
