# coding: utf-8

from smartbot import Utils

import requests
import re
import tempfile

class ExternalAPI:
    @staticmethod
    def translate(text, fromLanguage='en', toLanguage=None):
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

    @staticmethod
    def talk(text, language='pt'):
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36' }
        response = requests.get('https://translate.google.com/translate_tts?ie=UTF-8&q=' + text + '&tl=' + language + '&total=1&idx=0&textlen=4&tk=597433.997738&client=t&prev=input', headers=headers)
        fileName = tempfile.mkstemp()[1]
        fd = file(fileName, 'wb')
        fd.write(response.content)
        fd.close()
        return fileName
