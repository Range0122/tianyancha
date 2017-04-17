# -*- coding:utf-8 -*-

import scrapy
import codecs
import time
import re
import json
from tianyancha.items import TianyanchaItem
from scrapy.spiders import CrawlSpider
from tianyancha.middlewares import safe_append, safe_append_date
from scrapy.loader import ItemLoader
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

names = globals()

class Lawsuit_Spider(CrawlSpider):
    name = 'lawsuit_spider'
    start_urls = ['http://www.tianyancha.com                 ']

    def parse(self, response):
        with codecs.open('../lawsuit_test.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                url = 'http://www.tianyancha.com/lawsuit/detail/' + str(line.replace('\r', '').replace('\n', '')) + '.json'
                requests = scrapy.Request(url, callback=self.parse_annual)
                yield requests

    def parse_annual(self, response):
        'relative_comp',
        'title',
        'case_No',
        'body_title',
        'content'





