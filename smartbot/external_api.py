# coding: utf-8

from smartbot import Utils

import re
import os
import tempfile
import subprocess
import requests
from lxml import etree
from lxml import html
from urllib import quote

class ExternalAPI:
    @staticmethod
    def translate(text, fromLanguage='en', toLanguage=None):
        if not toLanguage:
            toLanguage = 'pt' if fromLanguage == 'en' else 'en'
        text = text.encode('utf-8')
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36' }
        text = re.sub('\s+', ' ', text, re.UNICODE)
        response = requests.get('https://translate.google.com/translate_a/single?client=t&sl=' + fromLanguage + '&tl=' + toLanguage + '&hl=en&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&ie=UTF-8&oe=UTF-8&otf=1&ssel=6&tsel=3&kc=7&tk=3271.403467&q=' + quote(text), headers=headers)
        try:
            piecesRaw = response.text
            piecesRawFirst = re.split('(\[\[|\]\])', piecesRaw)[2]
            piecesRawFirst = re.sub(',{2,}', ',', piecesRawFirst)
            piecesRawFirst = piecesRawFirst + ']'
            piecesRawFirst = re.sub('\[,', '[', piecesRawFirst)
            piecesRawFirst = re.sub(',\]', ']', piecesRawFirst)
            pieces = eval('[%s]' % piecesRawFirst)
            result = text
            for piece in pieces:
                if type(piece) is list and len(piece) >= 2:
                    result = result.replace(piece[1], piece[0], 1)
            result = result.decode('utf-8')
        except:
            result = None
        return result

    @staticmethod
    def textToSpeech(text, language='pt', encode='mp3'):
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36' }
        baseName = tempfile.mkstemp()[1]
        mp3Name = baseName + '.mp3'
        fd = file(mp3Name, 'ab')
	text = text.encode('utf-8')
        words = re.split('\s+', text, re.UNICODE)
        words = filter(lambda word: word.strip(), words)
        if len(words) < 50:
            response = requests.get('https://translate.google.com/translate_tts?ie=UTF-8&q=' + quote(text) + '&tl=' + language + '&total=1&idx=0&textlen=4&tk=597433.997738&client=t&prev=input', headers=headers)
            fd.write(response.content)
        else:
            for wordPos in range(0, len(words), 40):
                piece = ' '.join(words[wordPos:wordPos+40])
                pieceFileName = ExternalAPI.textToSpeech(piece, language, encode)
                pieceFile = file(pieceFileName, 'rb')
                fd.write(pieceFile.read())
                pieceFile.close()
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
            tree = Utils.crawlUrl('http://www.piadasnet.com/index.php?pesquisaCampo=%s&btpesquisa=OK&pesquisaInicio=0' % quote(query.encode('utf-8')))
        else:
            tree = Utils.crawlUrl('http://www.piadasnet.com/')
        jokeTags = tree.xpath('//p[contains(@class, "piada")]')
        return map(lambda t: t.text_content(), jokeTags)

    @staticmethod
    def searchGoogleImage(query):
        query = query.encode('utf-8')
        tree = Utils.crawlUrl('https://www.google.com.br/search?site=&tbm=isch&q=%s&oq=%s&tbs=isz:l' % (quote(query), quote(query)))
        imageTags = tree.xpath('//img[contains(@src, "gstatic")]')
        imageSources = map(lambda img: img.attrib.get('src'), imageTags)
        return imageSources

    @staticmethod
    def searchBingImage(query):
        tree = Utils.crawlUrl('http://www.bing.com/images/search?q=%s' % quote(query.encode('utf-8')))
        imageTags = tree.xpath('//img[contains(@src, "bing.net")]')
        imageSources = map(lambda img: img.attrib.get('src'), imageTags)
        return imageSources

    @staticmethod
    def getNasaIOD():
        tree = Utils.crawlUrl('http://apod.nasa.gov')
        imageTags = tree.xpath('//img[contains(@src,"image")]')
        pTags = tree.xpath('//p')
        if imageTags and len(pTags) >= 3:
            result = { 'imageSource': 'http://apod.nasa.gov/%s' % imageTags[0].attrib['src'], 'explanation': pTags[2].text_content() }
            return result
        else:
            return None

    @staticmethod
    def wolframQuery(query, appId=None):
        query = query.encode('utf-8')
        response = requests.get('http://api.wolframalpha.com/v2/query?input=%s&appid=%s' % (quote(query), appId))
        try:
            tree = etree.fromstring(response.content)
            results = []
            results += tree.xpath('//pod[contains(@title, "Solution")]/subpod/plaintext')
            results += tree.xpath('//pod[contains(@title, "Result")]/subpod/plaintext')
            results += tree.xpath('//pod[contains(@scanner, "Data")]/subpod/plaintext')
            if len(results) >= 0 and results[0].text and results[0].text.strip():
                return results[0].text.decode('utf-8')
            else:
                return None
        except:
            return None

    @staticmethod
    def eviQuery(query):
        query = query.encode('utf-8')
        query = re.sub('(\?|&)', ' ', query)
        query = re.sub('\s+', '_', query.strip().lower())
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36' }
        response = requests.get('https://www.evi.com/q/%s' % quote(query), headers=headers)
        tree = html.fromstring(response.text)
        results = tree.xpath('//*[contains(@class, "tk_text") or contains(@class, "tk_common")]')
        results = map(lambda tag: tag.text_content(), results)
        results = filter(lambda text: text.strip(), results)
        try:
            if len(results) >= 1 and results[0] and results[0].strip():
                result = results[0].strip()
                if result != 'Sorry, I don\'t yet have an answer to that question.':
                    return result.decode('utf-8')
                else:
                    return None
            else:
                return None
        except:
            return None
