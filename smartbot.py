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

vocabulary = {
    'diga': 'talk',
    'fale': 'talk',
    'traduz': 'translateen',
    'traduza': 'translateen',
    'nasa': 'nasa',
    'piada': 'joke',
    'manda': 'image'
}

bc = smartbot.BehaviourControl(bot)
bc.add('basic', smartbot.BasicBehaviour(bot))
bc.add('loader', smartbot.LoaderBehaviour(bot, bc))
bc.add('friendly', smartbot.FriendlyBehaviour(bot, vocabulary))
bc.add('translate', smartbot.TranslateBehaviour(bot))
bc.add('joke', smartbot.JokeBehaviour(bot))
bc.add('google_image', smartbot.GoogleImageBehaviour(bot))
bc.add('nasa', smartbot.NasaBehaviour(bot))
bc.add('talk', smartbot.TalkBehaviour(bot))
bc.load('basic')
bc.load('loader')
bc.load('friendly')
bc.load('translate')
bc.load('joke')
bc.load('google_image')
bc.load('nasa')

info = bot.getInfo()
print 'Botname: %s' % info.username

bot.listen()
