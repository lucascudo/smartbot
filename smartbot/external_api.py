# coding: utf-8

from smartbot import Utils

import requests
import re

class ExternalAPI:
    @staticmethod
    def translate(text, fromLanguage=None, toLanguage=None):
        fromLanguage = fromLanguage or 'en'
        if not toLanguage:
            toLanguage = 'pt' if fromLanguage == 'en' else 'en'
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36' }
        response = requests.get('https://translate.google.com/translate_a/single?client=t&sl=' + fromLanguage + '&tl=' + toLanguage + '&hl=en&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&otf=1&ssel=6&tsel=3&kc=7&tk=3271.403467&q=' + text, headers=headers)
        try:
            translatePiece = re.search('\[[^\[\]]+\]', response.text).group()
            translatePiece = re.sub(',{2,}', ',', translatePiece)
            resultParsed = eval(translatePiece)
        except Error as e:
            resultParsed = [text, 'Não consigo traduzir']
        result = resultParsed[0]
        return result
