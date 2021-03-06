# coding: utf-8

import sys
sys.path.append('.')

from smartbot import ExternalAPI

import unittest
import os
import re

class TestExternalAPI(unittest.TestCase):
    def setUp(self):
        if not os.environ.get('SMARTBOT_WOLFRAM_APPID'):
            sys.stderr.write('\nWARNING: The wolfram app id was not provided. Some tests will fail.\n')

    def testTranslateShortInvalidWord(self):
        sentence = 'pi'
        result = ExternalAPI.translate(sentence)
        self.assertEqual(result, 'PI')

    def testTranslateSimpleSentence(self):
        sentence = u'O que é carro ?'
        result = ExternalAPI.translate(sentence, fromLanguage='pt')
        self.assertEqual(result, 'What is a car?')

    def testTranslateComplex(self):
        sentence = 'The fox jumps. But who the hell is the fox ? I don\'t know'
        result = ExternalAPI.translate(sentence)
        self.assertEqual(result, u'A raposa salta. Mas quem \xe9 a raposa? Eu n\xe3o sei')

    def textTextToSpeechAsMP3(self):
        sentence = 'ok'
        audioFile = ExternalAPI.textToSpeech(sentence, fromLanguage='en', encode='mp3')
        self.assertTrue(os.path.getsize(audioFile) > 0)

    def textTextToSpeechAsOGG(self):
        sentence = 'ok'
        audioFile = ExternalAPI.textToSpeech(sentence, fromLanguage='en', encode='ogg')
        self.assertTrue(os.path.getsize(audioFile) > 0)

    def testSearchJoke(self):
        result = ExternalAPI.searchJoke('amigo')
        self.assertItemsEqual(result, filter(lambda j: re.match('.*amigo.*', j, re.IGNORECASE), result))

    def testSearchGoogleImage(self):
        result = ExternalAPI.searchGoogleImage('amigo')
        self.assertItemsEqual(result, filter(lambda img: re.match('http.*gstatic.*', img), result))

    def testSearchBingImage(self):
        result = ExternalAPI.searchBingImage('amigo')
        self.assertItemsEqual(result, filter(lambda img: re.match('http.*bing.net.*', img), result))

    def testGetNasaIOD(self):
        result = ExternalAPI.getNasaIOD()
        self.assertTrue(result.get('imageSource'))
        self.assertTrue(result.get('explanation'))

    def testWolframQuery(self):
        result = ExternalAPI.wolframQuery('who are you ?', os.environ.get('SMARTBOT_WOLFRAM_APPID'))
        self.assertEqual(result, 'My name is Wolfram|Alpha.')

    def testWolframQueryForMathInNumbers(self):
        result = ExternalAPI.wolframQuery('calculate 1 + 1', os.environ.get('SMARTBOT_WOLFRAM_APPID'))
        self.assertEqual(result, '2')

    def testWolframQueryForMathInWords(self):
        result = ExternalAPI.wolframQuery('calculate one plus one', os.environ.get('SMARTBOT_WOLFRAM_APPID'))
        self.assertEqual(result, '2')

    def testEviQuery(self):
        result = ExternalAPI.eviQuery('who are you ?')
        self.assertEqual(result, 'I\'m Evi, your thinking, talking, computerised assistant.')

    def testEviQueryForMathInNumbers(self):
        result = ExternalAPI.eviQuery('calculate 1 + 1')
        self.assertEqual(result, 'Sorry, that looks like a maths question. Try asking it in words rather than using symbols like + or *.')

    def testEviQueryForMathInWords(self):
        result = ExternalAPI.eviQuery('calculate one plus one')
        self.assertEqual(result, 'The sum of 1 and 1 is 2.')

if __name__ == '__main__':
    unittest.main()
