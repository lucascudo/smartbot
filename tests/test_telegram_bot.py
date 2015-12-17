# coding: utf-8

import sys
sys.path.append('.')

from smartbot import TelegramBot

import unittest
from mock import patch, Mock
import os

class TestTelegramBot(unittest.TestCase):
    def testGetInfo(self):
        bot = TelegramBot('FAKE-TOKEN')
        info = Mock()
        bot.telegramBot = Mock()
        bot.telegramBot.getMe = Mock(return_value=info)
        infoResult = bot.getInfo()
        self.assertEqual(infoResult, info)

    def testSendMessage(self):
        bot = TelegramBot('FAKE-TOKEN')
        params = { 'chat_id': 'a', 'text': 'b'}
        bot.telegramBot = Mock()
        bot.telegramBot.sendMessage = Mock(return_value=True)
        self.assertTrue(bot.sendMessage(**params))
        bot.telegramBot.sendMessage.assert_called_once_with(**params)

    def testSendVoice(self):
        bot = TelegramBot('FAKE-TOKEN')
        params = { 'chat_id': 'a', 'voice': 'b'}
        with patch('requests.post') as mockRequestPost, patch('__builtin__.open') as mockOpen:
            mockRequestPost.return_value = True
            self.assertTrue(bot.sendVoice(**params))
            mockOpen.assert_called_once_with('b', 'rb')
            self.assertEqual(mockRequestPost.call_count, 1)

    def testSendAudio(self):
        bot = TelegramBot('FAKE-TOKEN')
        params = { 'chat_id': 'a', 'audio': 'b'}
        with patch('requests.post') as mockRequestPost, patch('__builtin__.open') as mockOpen:
            mockRequestPost.return_value = True
            self.assertTrue(bot.sendAudio(**params))
            mockOpen.assert_called_once_with('b', 'rb')
            self.assertEqual(mockRequestPost.call_count, 1)

    def testListen(self):
        bot = TelegramBot('FAKE-TOKEN')
        bot.updater = Mock()
        bot.updater.start_polling = Mock()
        bot.listen()
        bot.updater.start_polling.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()
