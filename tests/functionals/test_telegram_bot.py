# coding: utf-8

import sys
sys.path.append('.')

from smartbot import TelegramBot

import unittest
import os

class TestTelegramBot(unittest.TestCase):
    def setUp(self):
        self.token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.assertTrue(self.token, msg='The telegram token was not provided')

    def testGetInfo(self):
        bot = TelegramBot(self.token)
        info = bot.getInfo()
        self.assertTrue(info.id)
        self.assertTrue(info.username)
        self.assertTrue(info.first_name)

if __name__ == '__main__':
    unittest.main()
