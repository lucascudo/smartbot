# coding: utf-8

import sys
import re
import argparse
import smartbot

arg_parser = argparse.ArgumentParser(description='Run smartbot')
arg_parser.add_argument('--token', required=True, dest='token', type=str, help='The telegram bot token')
args = arg_parser.parse_args()

token = args.token

bot = smartbot.Bot(token)

bc = smartbot.BehaviourControl(bot)
bc.add('basic', smartbot.BasicBehaviour(bot))
bc.add('loader', smartbot.LoaderBehaviour(bot, bc))
bc.add('google_image', smartbot.GoogleImageBehaviour(bot))
bc.load('basic')
bc.load('loader')
bc.load('google_image')

info = bot.getInfo()
print 'Botname: %s' % info.username

bot.listen()
