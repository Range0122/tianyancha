# -*- coding:utf-8 -*-

import scrapy
import codecs
from tianyancha.items import TianyanchaItem
from scrapy.spider import CrawlSpider
from scrapy.loader import ItemLoader
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class TianYanCha_Spider(CrawlSpider):
    name = 'tyc_spider'
    start_urls = ['http://www.tianyancha.com/']

    def parse(self, response):
        basic_url = 'http://www.tianyancha.com/search?key='
        f = codecs.open('name_list.txt', 'r', encoding='utf-8')
        for line in f.readlines():
            url = basic_url + str(line)
            requests = scrapy.Request(url.replace('\r', ''), callback=self.parse_search_page)
            yield requests

    def parse_search_page(self, response):
        url_list = response.selector.xpath('//div[@class="b-c-white search_result_container ng-scope"]/div/div[2]/div[1]/div[1]/a/@href')
        for url in url_list:
            requests = scrapy.Request(url, callback=self.parse_info_page)

    def parse_info_page(self, response):
        l = ItemLoader(item=TianyanchaItem(), response=response)
        # l.add_xpath('parameter_name', 'xpath')
        # yield l.load_item()
