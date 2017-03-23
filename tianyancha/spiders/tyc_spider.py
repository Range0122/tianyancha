# -*- coding:utf-8 -*-

import scrapy
import codecs
import time
from tianyancha.items import TianyanchaItem
from scrapy.spiders import CrawlSpider
from scrapy.loader import ItemLoader
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class TianYanCha_Spider(CrawlSpider):
    name = 'tyc_spider'
    start_urls = ['http://www.tianyancha.com/']

    def parse(self, response):
        basic_url = 'http://www.tianyancha.com/search?key='
        with codecs.open('test_list.txt', 'r', encoding='utf-8') as f:
        # with codecs.open('name_list.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                url = basic_url + str(line)
                url = url.replace('\r', '').replace('\n', '').replace('%0A', '') + '&checkFrom=searchBox'
                requests = scrapy.Request(url, callback=self.parse_search_page)
                yield requests

    def parse_search_page(self, response):
        url_list = response.xpath('//div[@class="b-c-white search_result_container ng-scope"]/div/div[2]/div[1]/div[1]/a/@href').extract()
        if not url_list:
            time_now = time.asctime(time.localtime(time.time()))
            with codecs.open('log.txt', 'a', encoding='utf-8') as f:
                f.write(str(response.url) + ' ' + str(time_now) + '\r')
            print "THE LIST IS EMPTY ", response.url
        for url in url_list:
            requests = scrapy.Request(url, callback=self.parse_info_page)
            yield requests

    def parse_info_page(self, response):
        try:
            item = TianyanchaItem()
            l = ItemLoader(item=item, response=response)

            company_id = response.url[34:]
            company_name = response.xpath('//div[@class="company_info_text"]/div[1]/text()').extract()[0]
            legal_representative = response.xpath(u'//div[text()="法定代表人"]/following-sibling::div[1]/a/text()').extract()[0]
            registered_capital = response.xpath(u'//div[text()="注册资本"]/following-sibling::div[1]/text()').extract()[0]
            registered_time = response.xpath(u'//div[text()="注册时间"]/following-sibling::div[1]/text()').extract()[0]
            condition = response.xpath(u'//div[text()="状态"]/following-sibling::div[1]/text()').extract()[0]
            temp_items = response.xpath('//td[@class="basic-td"]/div[1]/span/text()').extract()
            registered_number = temp_items[0]
            organization_number = temp_items[1]
            credit_number = temp_items[2]
            enterprise_type = temp_items[3]
            industry = temp_items[4]
            operating_period = temp_items[5]
            approved_date = temp_items[6]
            registration_authority = temp_items[7]
            registered_address = response.xpath('//td[@class="basic-td ng-scope"]/div/span/text()').extract()[0]
            business_scope = response.xpath('//td[@class="basic-td ng-scope"]/div/span/span/text()').extract()[0]
            temp_items = response.xpath('//div[@class="company_info_text"]/span/text()').extract()
            telephone = temp_items[0]
            email = temp_items[1]
            address = temp_items[5]
            website = response.xpath('//div[@class="company_info_text"]/span[3]/a/text()').extract()[0]
            score = response.xpath('//td[@class="td-score position-rel"]/img/@ng-alt').extract()[0][-2:]
            logo_location = response.xpath('//div[@class="company_info"]/div[1]/img/@src').extract()[0]
            # 有一些logo的链接坏掉了，网站给出了备用logo
            # logo_location = response.xpath('//div[@class="company_info"]/div[1]/img/@onerror').extract()[0].replace('this.src=', '').replace("'", '')
            # logo_location = http://static.tianyancha.com/wap/images/company_pic_v2.png

            l.add_value("company_name", company_name)
            l.add_value("legal_representative", legal_representative)
            l.add_value("registered_capital", registered_capital)
            l.add_value("registered_time", registered_time)
            l.add_value("condition", condition)
            l.add_value("registered_number", registered_number)
            l.add_value("organization_number", organization_number)
            l.add_value("credit_number", credit_number)
            l.add_value("enterprise_type", enterprise_type)
            l.add_value("industry", industry)
            l.add_value("operating_period", operating_period)
            l.add_value("approved_date", approved_date)
            l.add_value("registration_authority", registration_authority)
            l.add_value("registered_address", registered_address)
            l.add_value("business_scope", business_scope)
            l.add_value("telephone", telephone)
            l.add_value("email", email)
            l.add_value("website", website)
            l.add_value("logo_location", logo_location)
            l.add_value("address", address)
            l.add_value("score", score)
            l.add_value("company_id", company_id)
            print "ONE OK"

            yield l.load_item()

        except:
            print "ONE FAIL"
            with codecs.open('log.txt', 'a', encoding='utf-8') as f:
                time_now = time.asctime(time.localtime(time.time()))
                f.write(str(response.url) + ' ' + str(time_now) + '\r')
