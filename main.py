# coding: utf-8

import sys
import re
import telegram
from telegram import Updater
from telegram import Bot

import smartbot

token = '177224385:AAHwrklE9Yx-nrPvNaXRtGiEM5qH2UWuAKM'
bot = Bot(token=token)
updater = Updater(token=token)

bc = smartbot.BehaviourControl(bot, updater)
bc.add('basic', smartbot.BasicBehaviour)
bc.load('basic')

me = bot.getMe()

print me.username

updater.start_polling()
