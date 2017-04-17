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

class Annual_Spider(CrawlSpider):
    name = 'annual_spider'
    start_urls = ['http://www.tianyancha.com                 ']

    def parse(self, response):
        with codecs.open('../annual_test.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                url = str(line.replace('\r', '').replace('\n', ''))
                requests = scrapy.Request(url, callback=self.parse_annual)
                yield requests

    def parse_annual(self, response):
        asset_status_name_list = ['totalAssets', 'totalEquity', 'totalSales', 'totalProfit', 'primeBusProfit',
                                  'retainedProfit', 'totalTax', 'totalLiability']
        alter_event_name_list = ['changeItem', 'contentBefore', 'contentAfter', 'changeTime']

        for item_name in asset_status_name_list + alter_event_name_list:
            names[item_name] = ['None']

        data = json.loads(response.body)

        for item_name in asset_status_name_list:
            safe_append(names[item_name], data["data"]["baseInfo"], item_name)

        for dic in data["data"]["changeRecordList"]:
            for item_name in alter_event_name_list:
                safe_append(names[item_name], dic, item_name)

