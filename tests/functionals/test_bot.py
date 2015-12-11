# coding: utf-8

import sys
sys.path.append('.')

from smartbot import Bot

import unittest
import os

class TestBot(unittest.TestCase):
    def testGetInfo(self):
        bot = Bot(os.environ['TELEGRAM_BOT_TOKEN'])
        info = bot.getInfo()
        self.assertTrue(info.id)
        self.assertTrue(info.username)
        self.assertTrue(info.first_name)

if __name__ == '__main__':
    unittest.main()
