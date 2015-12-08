# coding: utf-8

from smartbot import Utils

import re
import os
import tempfile
import subprocess
import requests

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
    def textToSpeech(text, language='pt', encode='mp3'):
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36' }
        response = requests.get('https://translate.google.com/translate_tts?ie=UTF-8&q=' + text + '&tl=' + language + '&total=1&idx=0&textlen=4&tk=597433.997738&client=t&prev=input', headers=headers)
        baseName = tempfile.mkstemp()[1]
        mp3Name = baseName + '.mp3'
        fd = file(mp3Name, 'wb')
        fd.write(response.content)
        fd.close()
        if encode == 'mp3':
            return mp3Name
        elif encode == 'ogg':
            oggName = baseName + '.ogg'
            subprocess.call(('ffmpeg -v -8 -i %s -acodec libvorbis %s' % (mp3Name, oggName)).split(' '))
            return oggName
        else:
            return None

    @staticmethod
    def searchJoke(query=None):
        if query:
            tree = Utils.crawlUrl('http://www.piadasnet.com/index.php?pesquisaCampo=%s&btpesquisa=OK&pesquisaInicio=0' % query)
        else:
            tree = Utils.crawlUrl('http://www.piadasnet.com/')
        jokeTags = tree.xpath('//p[contains(@class, "piada")]')
        return map(lambda t: t.text_content(), jokeTags)

    @staticmethod
    def searchImage(query):
        tree = Utils.crawlUrl('https://www.google.com.br/search?site=&tbm=isch&q=%s&oq=%s&tbs=isz:l' % (query, query))
        imageTags = tree.xpath('//img')
        imageSources = map(lambda img: img.attrib['src'], imageTags)
        p = re.compile('.*gstatic.*')
        imageSources = filter(lambda source: p.match(source), imageSources)
        return imageSources
