# coding: utf-8

from lxml import html
import requests

class Utils:
    @staticmethod
    def crawlUrl(url):
        response = requests.get(url)
        return html.fromstring(response.content)
