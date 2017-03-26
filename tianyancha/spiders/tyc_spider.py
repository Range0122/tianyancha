# -*- coding:utf-8 -*-

import scrapy
import codecs
import time
import re
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
        with codecs.open('../company_test.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                url = str(line.replace('\r', '').replace('\n', ''))
                requests = scrapy.Request(url, callback=self.parse_page)
                yield requests

    def parse_page(self, response):
        # try:

        item = TianyanchaItem()
        l = ItemLoader(item=item, response=response)
        company_id = response.url[34:]
        company_name = (response.selector.xpath('//div[@class="company_info_text"]/div[1]/text()').extract() or
                        response.selector.xpath('//span[@class="base-company f16 ng-binding"]/text()').extract())[0]
        legal_representative = (response.selector.xpath(u'//div[text()="法定代表人"]/following-sibling::div[1]/a/text()').extract() or
                                response.selector.xpath('//a[@ng-if="company.baseInfo.legalPersonName"]/text()').extract())[0]
        registered_capital = (response.selector.xpath(u'//div[text()="注册资本"]/following-sibling::div[1]/text()').extract() or
                              response.selector.xpath('//td[@class="td-regCapital-value"]/p/text()').extract())[0]
        registered_time = (response.selector.xpath(u'//div[text()="注册时间"]/following-sibling::div[1]/text()').extract() or
                           response.selector.xpath('//td[@class="td-regTime-value"]/p/text()').extract())[0]
        condition = (response.selector.xpath(u'//div[text()="状态"]/following-sibling::div[1]/text()').extract() or
                     response.selector.xpath('//td[@class="td-regStatus-value"]/p/text()').extract())[0]
        temp_items = response.selector.xpath('//td[@class="basic-td"]/div[1]/span/text()').extract()
        if temp_items:
            registered_number = temp_items[0]
            organization_number = temp_items[1]
            credit_number = temp_items[2]
            enterprise_type = temp_items[3]
            industry = temp_items[4]
            operating_period = temp_items[5]
            approved_date = temp_items[6]
            registration_authority = temp_items[7]
        else: 
            registered_number = response.selector.xpath('//p[@ng-if="company.baseInfo.regNumber"]/text()').extract_first(default=u'未公开')
            organization_number = response.selector.xpath('//p[@ng-if="company.baseInfo.orgNumber"]/text()').extract_first(default=u'未公开')
            credit_number = response.selector.xpath('//p[@ng-if="company.baseInfo.creditCode"]/text()').extract_first(default=u'未公开')
            enterprise_type = response.selector.xpath('//p[@ng-if="company.baseInfo.companyOrgType"]/text()').extract_first(default=u'未公开')
            industry = response.selector.xpath('//p[@ng-if="company.baseInfo.industry"]/text()').extract_first(default=u'未公开')
            operating_period = response.selector.xpath('//p[@ng-if="company.baseInfo.fromTime"]/text()').extract_first(default=u'未公开')
            approved_date = response.selector.xpath('//p[@ng-if="company.baseInfo.estiblishTime"]/text()').extract_first(default=u'未公开')
            registration_authority = response.selector.xpath('//p[@ng-if="company.baseInfo.regInstitute"]/text()').extract_first(default=u'未公开')
        registered_address = (response.selector.xpath('//td[@class="basic-td ng-scope"]/div/span/text()').extract() or
                              response.selector.xpath('//p[@ng-if="company.baseInfo.regLocation"]/text()').extract())[0]
        business_scope = (response.selector.xpath('//td[@class="basic-td ng-scope"]/div/span/span/text()').extract() or
                         response.selector.xpath('//span[@ng-if="company.baseInfo.businessScope"]/text()').extract())[0]
        temp_items = response.selector.xpath('//div[@class="company_info_text"]/span/text()').extract()
        if temp_items:
            telephone = temp_items[0]
            email = temp_items[1]
            address = temp_items[5]
        else:
            telephone = u'暂无'
            email = u'暂无'
            address = u'暂无'
        website = (response.selector.xpath('//div[@class="company_info_text"]/span[3]/a/text()').extract() or
                   response.selector.xpath('//div[@class="company_info_text"]/span[3]/span[2]/text()').extract() or
                   response.selector.xpath('//span[@ng-hide="company.websiteList"]/text()').extract())
        if website:
            website = website[0]
        else:
            website = u'暂无'
        score = (response.selector.xpath('//td[@class="td-score position-rel"]/img/@ng-alt').extract() or
                 response.selector.xpath('//img[@class="td-score-img"]/@ng-alt').extract())[0][-2:]
        logo_location = response.selector.xpath('//div[@class="company_info"]/div[1]/img/@src').extract()[0]
        former_name = response.selector.xpath(u'//span[text()="曾用名"]/following-sibling::span[2]/text()').extract_first(default='None')

        # 有一些logo的链接坏掉了，网站给出了备用logo
        # logo_location = response.xpath('//div[@class="company_info"]/div[1]/img/@onerror').extract()[0].replace('this.src=', '').replace("'", '')
        # logo_location = http://static.tianyancha.com/wap/images/company_pic_v2.png
        person_id = response.selector.xpath(
            '//div[@class="staffinfo-module-container ng-scope"]/div/div/div[2]/div[1]/a/@href').extract()
        person_name = response.selector.xpath(
            '//div[@class="staffinfo-module-container ng-scope"]/div/div/div[2]/div[1]/a/text()').extract()
        position = response.selector.xpath(
            '//div[@class="staffinfo-module-container ng-scope"]/div/div/div[2]/div[2]/span/text()').extract()
        if person_id:
            for i in range(0, len(person_id)):
                person_id[i] = person_id[i][7:]
        else:
            person_id = 'None'
            person_name = 'None'
            position = 'None'
        if not position:
            position = ['None']

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
        l.add_value("person_id", person_id)
        l.add_value("person_name", person_name)
        l.add_value("position", position)
        l.add_value("former_name", former_name)
        print "ONE OK"
        yield l.load_item()
        # except Exception as e:
        #     pass
            # print e
            # print response.body



        # except Exception as e:
        #     print "ONE FAIL"
        #     with codecs.open('log.txt', 'a', encoding='utf-8') as f:
        #         time_now = time.asctime(time.localtime(time.time()))
        #         f.write(str(response.url) + ' ' + str(e) + ' ' + str(time_now) + '\r')


