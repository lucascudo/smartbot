# coding: utf-8

import sys
import os
import argparse
import smartbot

arg_parser = argparse.ArgumentParser(description='Run smartbot')
arg_parser.add_argument('--wolfram-app-id', required=False, dest='wolfram_app_id', type=str, help='The wolfram app id (or env[WOLFRAM_APP_ID])')
arg_parser.add_argument('--telegram-bot-token', required=False, dest='telegram_bot_token', type=str, help='The telegram bot token (or env[TELEGRAM_BOT_TOKEN])')
args = arg_parser.parse_args()

wolfram_app_id = args.wolfram_app_id or os.environ.get('WOLFRAM_APP_ID')
token = args.telegram_bot_token or os.environ.get('TELEGRAM_BOT_TOKEN')

if not token:
    sys.stderr.write('Please set the telegram bot token (see --help for details).\n')
    exit(0)

bot = smartbot.Bot(token)

vocabulary = {
    'standup': 'jalk',
    'diga': 'talk',
    'fale': 'talk',
    'traduz': 'translateen',
    'traduza': 'translateen',
    'nasa': 'nasa',
    'piada': 'joke',
    'manda': 'gimage',
    'quero': 'bimage'
}

bc = smartbot.BehaviourControl(bot)
bc.add('basic', smartbot.BasicBehaviour(bot))
bc.add('loader', smartbot.LoaderBehaviour(bot, bc))
bc.add('friendly', smartbot.FriendlyBehaviour(bot, bc, vocabulary))
bc.add('translate', smartbot.TranslateBehaviour(bot))
bc.add('joke', smartbot.JokeBehaviour(bot))
bc.add('google_image', smartbot.GoogleImageBehaviour(bot))
bc.add('bing_image', smartbot.BingImageBehaviour(bot))
bc.add('nasa', smartbot.NasaBehaviour(bot))
bc.add('talk', smartbot.TalkBehaviour(bot))
bc.add('wolfram', smartbot.WolframBehaviour(bot, wolfram_app_id))
bc.add('evi', smartbot.EviBehaviour(bot))
bc.load('basic')
bc.load('loader')
bc.load('friendly')
bc.load('translate')
bc.load('joke')
bc.load('google_image')
bc.load('bing_image')
bc.load('nasa')
bc.load('talk')
if wolfram_app_id:
    bc.load('wolfram')
bc.load('evi')

smartbot.Utils.logInfo(bot, 'MAIN', 'Starting bot')

if not wolfram_app_id:
    smartbot.Utils.logWarning(bot, 'MAIN', 'The Wolfram|Alpha APP ID was not provided. Behaviour disabled')

bot.listen()
