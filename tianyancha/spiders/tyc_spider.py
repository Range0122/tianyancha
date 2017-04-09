# -*- coding:utf-8 -*-

import scrapy
import codecs
import time
import re
import json
from tianyancha.items import TianyanchaItem
from scrapy.spiders import CrawlSpider
from scrapy.loader import ItemLoader
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class TianYanCha_Spider(CrawlSpider):
    name = 'tyc_spider'
    start_urls = ['http://www.tianyancha.com                 ']

    def parse(self, response):
        with codecs.open('../company_test.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                url = str(line.replace('\r', '').replace('\n', '').replace('=', ''))
                requests = scrapy.Request(url, callback=self.parse_basic_info)
                yield requests

    def parse_basic_info(self, response):
        item = TianyanchaItem()
        company_id = response.url[34:]
        company_name = response.selector.xpath('//div[@class="company_info_text"]/div[1]/text()').extract()[0]
        legal_representative = response.selector.xpath(u'//div[text()="法定代表人"]/following-sibling::div[1]/a/text()').extract_first(default=u'未公开')
        registered_capital = response.selector.xpath(u'//div[text()="注册资本"]/following-sibling::div[1]/text()').extract_first(default=u'未公开')
        registered_time = response.selector.xpath(u'//div[text()="注册时间"]/following-sibling::div[1]/text()').extract_first(default=u'未公开')
        condition = response.selector.xpath(u'//div[text()="状态"]/following-sibling::div[1]/text()').extract_first(default=u'未公开')
        temp_items = response.selector.xpath('//td[@class="basic-td"]/div[1]/span/text()').extract()
        registered_number = temp_items[0]
        organization_number = temp_items[1]
        credit_number = temp_items[2]
        enterprise_type = temp_items[3]
        industry = temp_items[4]
        operating_period = temp_items[5]
        approved_date = temp_items[6]
        registration_authority = temp_items[7]
        registered_address = response.selector.xpath('//td[@class="basic-td ng-scope"]/div/span/text()').extract_first(default=u'暂无')
        business_scope = response.selector.xpath('//td[@class="basic-td ng-scope"]/div/span/span/text()').extract_first(default=u'暂无')
        telephone = response.selector.xpath('//div[@class="company_info_text"]/span[1]/text()').extract_first(default=u'暂无')
        email = response.selector.xpath('//div[@class="company_info_text"]/span[2]/text()').extract_first(default=u'暂无')
        address = response.selector.xpath('//div[@class="company_info_text"]/span[4]/text()').extract_first(default=u'暂无')
        website = response.selector.xpath('//div[@class="company_info_text"]/span[3]/a/text()').extract_first(default=u'暂无')
        score = response.selector.xpath('//td[@class="td-score position-rel"]/img/@ng-alt | //img[@class="td-score-img"]/@ng-alt').extract()[0][-2:]
        logo_location = response.selector.xpath('//div[@class="company_info"]/div[1]/img/@src').extract()[0]
        former_name = response.selector.xpath(u'//span[text()="曾用名"]/following-sibling::span[2]/text()').extract_first(default=u'无')

        flag = response.selector.xpath('//div[@class="company_container"]/div/div/div/@class').extract()
        for i in range(0, len(flag)):
            if flag[i][-7:] == u'disable':
                flag[i] = 0
            else:
                flag[i] = 1

        item["flag"] = flag
        item["company_name"] = company_name
        item["legal_representative"] = legal_representative
        item["registered_capital"] = registered_capital
        item["registered_time"] = registered_time
        item["condition"] = condition
        item["registered_number"] = registered_number
        item["organization_number"] = organization_number
        item["credit_number"] = credit_number
        item["enterprise_type"] = enterprise_type
        item["industry"] = industry
        item["operating_period"] = operating_period
        item["approved_date"] = approved_date
        item["registration_authority"] = registration_authority
        item["registered_address"] = registered_address
        item["business_scope"] = business_scope
        item["telephone"] = telephone
        item["email"] = email
        item["website"] = website
        item["logo_location"] = logo_location
        item["address"] = address
        item["score"] = score
        item["company_id"] = company_id
        item["former_name"] = former_name

        next_url = 'http://www.tianyancha.com/expanse/staff.json?id=' + str(item["company_id"]) + '&ps=20&pn=1'
        request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_main_person)
        yield request

    def parse_main_person(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        person_id = ['None']
        person_name = ['None']
        position = ['None']

        if flag[2] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["result"]:
                person_id.append(dic["id"])
                person_name.append(dic["name"])
                position.append(dic["typeJoin"][0])

        item["person_id"] = person_id
        item["person_name"] = person_name
        item["position"] = position

        item["shareholder_id"] = ['None']
        item["shareholder_name"] = ['None']
        item["investment_proportion"] = ['None']
        item["subscribed_contribution"] = ['None']
        item["subscribed_contribution_time"] = ['None']
        item["really_contribution"] = ['None']
        item["page"] = 1

        next_url = 'http://www.tianyancha.com/expanse/holder.json?id=' + str(item["company_id"]) + '&ps=20&pn=1'
        request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_shareholder_info)
        yield request

    def parse_shareholder_info(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        shareholder_id = item["shareholder_id"]
        shareholder_name = item["shareholder_name"]
        investment_proportion = item["investment_proportion"]
        subscribed_contribution = item["subscribed_contribution"]
        subscribed_contribution_time = item["subscribed_contribution_time"]
        really_contribution = item["really_contribution"]

        if flag[3] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["result"]:
                try:
                    shareholder_id.append(dic["id"] or u'无')
                except:
                    shareholder_id.append(u'无')

                try:
                    shareholder_name.append(dic["name"] or u'无')
                except:
                    shareholder_name.append(u'无')

                try:
                    investment_proportion.append(dic["capital"][0]["percent"] or u'无')
                except:
                    investment_proportion.append(u'无')

                try:
                    subscribed_contribution.append(dic["capital"][0]["amomon"] or u'无')
                except:
                    subscribed_contribution.append(u'无')

                try:
                    subscribed_contribution_time.append(dic["capital"][0]["time"] or u'无')
                except:
                    subscribed_contribution_time.append(u'无')

                try:
                    really_contribution.append(dic["capitalActl"][0]["amomon"] or u'无')
                except:
                    really_contribution.append(u'无')

        item["shareholder_id"] = shareholder_id
        item["shareholder_name"] = shareholder_name
        item["investment_proportion"] = investment_proportion
        item["subscribed_contribution"] = subscribed_contribution
        item["subscribed_contribution_time"] = subscribed_contribution_time
        item["really_contribution"] = really_contribution

        if len(response.body) > 1000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/holder.json?id=' + str(item["company_id"]) + '&ps=20&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_shareholder_info)
            yield request
        else:
            item["invested_company_id"] = ['None']
            item["invested_company_name"] = ['None']
            item["invested_representative"] = ['None']
            item["registered_cap"] = ['None']
            item["investment_amount"] = ['None']
            item["investment_prop"] = ['None']
            item["registered_date"] = ['None']
            item["condit"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/inverst.json?id=' + str(item["company_id"]) + '&ps=20&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_investment)
            yield request

    def parse_investment(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        invested_company_id = item["invested_company_id"]
        invested_company_name = item["invested_company_name"]
        invested_representative = item["invested_representative"]
        registered_cap = item["registered_cap"]
        investment_amount = item["investment_amount"]
        investment_prop = item["investment_prop"]
        registered_date = item["registered_date"]
        condit = item["condit"]

        if flag[4] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["result"]:
                try:
                    invested_company_id.append(dic["id"] or u'无')
                except:
                    invested_company_id.append(u'无')

                try:
                    invested_company_name.append(dic["name"] or u'无')
                except:
                    invested_company_name.append(u'无')

                try:
                    invested_representative.append(dic["legalPersonName"] or  u'无')
                except:
                    invested_representative.append(u'无')

                try:
                    registered_cap.append(dic["regCapital"] or u'无')
                except:
                    registered_cap.append(u'无')

                if dic["amount"] == 0:
                    investment_amount.append(u'无')
                else:
                    try:
                        investment_amount.append(str(dic["amount"]) + u'万元人民币')
                    except:
                        investment_amount.append(u'无')

                try:
                    investment_prop.append(dic["percent"] or u'无')
                except:
                    investment_prop.append(u'无')

                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["estiblishTime"])[:10])))
                    registered_date.append(str(date))
                except:
                    registered_date.append(u'无')

                try:
                    condit.append(dic["regStatus"] or u'无')
                except:
                    condit.append(u'无')

        item["invested_company_id"] = invested_company_id
        item["invested_company_name"] = invested_company_name
        item["invested_representative"] = invested_representative
        item["registered_cap"] = registered_cap
        item["investment_amount"] = investment_amount
        item["investment_prop"] = investment_prop
        item["registered_date"] = registered_date
        item["condit"] = condit

        if len(response.body) > 3000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/inverst.json?id=' + str(item["company_id"]) + '&ps=20&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_investment)
            yield request
        else:
            item["change_time"] = ['None']
            item["change_item"] = ['None']
            item["before_change"] = ['None']
            item["after_change"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/changeinfo.json?id=' + str(item["company_id"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_change_record)
            yield request

    def parse_change_record(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        change_time = item["change_time"]
        change_item = item["change_item"]
        before_change = item["before_change"]
        after_change = item["after_change"]

        if flag[5] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["result"]:
                try:
                    change_time.append(dic["changeTime"] or u'无')
                except:
                    change_time.append(u'无')
                try:
                    change_item.append(dic["changeItem"] or u'无')
                except:
                    change_item.append(u'无')
                try:
                    before_change.append(dic["contentBefore"] or u'无')
                except:
                    before_change.append(u'无')

                try:
                    after_change.append(dic["contentAfter"] or u'无')
                except:
                    after_change.append(u'无')

        item["change_time"] = change_time
        item["change_item"] = change_item
        item["before_change"] = before_change
        item["after_change"] = after_change

        if len(response.body) > 800:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/changeinfo.json?id=' + str(item["company_id"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_change_record)
            yield request
        else:
            next_url = 'http://www.tianyancha.com/expanse/annu.json?id=' + str(item["company_id"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_annual_reports)
            yield request

    def parse_annual_reports(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        annual_year = ['None']
        annual_url = ['None']

        if flag[6] == 1:
            data = json.loads(response.body)
            for dic in data["data"]:
                try:
                    url = 'http://www.tianyancha.com/reportContent/' + str(item["company_id"]) + '/' + str(dic["reportYear"])
                    annual_url.append(url)
                except:
                    annual_url.append(u'无')
                try:
                    annual_year.append(dic["reportYear"] or u'无')
                except:
                    annual_year.append(u'无')


        item["annual_year"] = annual_year
        item["annual_url"] = annual_url

        item["branch_id"] = ['None']
        item["branch_name"] = ['None']
        item["branch_legalrep"] = ['None']
        item["branch_cond"] = ['None']
        item["branch_regtime"] = ['None']
        item["page"] = 1

        next_url = 'http://www.tianyancha.com/expanse/branch.json?id=' + str(item["company_id"]) + '&ps=10&pn=1'
        request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_branch)
        yield request

    def parse_branch(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        branch_id = item["branch_id"]
        branch_name = item["branch_name"]
        branch_legalrep = item["branch_legalrep"]
        branch_cond = item["branch_cond"]
        branch_regtime = item["branch_regtime"]

        if flag[7] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["result"]:
                try:
                    branch_id.append(dic["id"] or u'无')
                except:
                    branch_id.append(u'无')

                try:
                    branch_name.append(dic["name"] or u'无')
                except:
                    branch_name.append(u'无')
                branch_legalrep.append(u'暂无')
                branch_cond.append(u'暂无')
                branch_regtime.append(u'暂无')

        item["branch_id"] = branch_id
        item["branch_name"] = branch_name
        item["branch_legalrep"] = branch_legalrep
        item["branch_cond"] = branch_cond
        item["branch_regtime"] = branch_regtime

        if len(response.body) > 500:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/branch.json?id=' + str(item["company_id"]) + '&ps=10&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_branch)
            yield request
        else:
            item["finance_date"] = ['None']
            item["finance_round"] = ['None']
            item["valuation"] = ['None']
            item["finance_amount"] = ['None']
            item["finance_proportion"] = ['None']
            item["investor"] = ['None']
            item["news_title"] = ['None']
            item["news_url"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/findHistoryRongzi.json?name=' + str(item["company_name"]) + '&ps=10&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_finance_history)
            yield request

    def parse_finance_history(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        finance_date = item["finance_date"]
        finance_round = item["finance_round"]
        valuation = item["valuation"]
        finance_amount = item["finance_amount"]
        finance_proportion = item["finance_proportion"]
        investor = item["investor"]
        news_title = item["news_title"]
        news_url = item["news_url"]

        if flag[8] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["page"]["rows"]:
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["date"])[:10])))
                    finance_date.append(str(date))
                except:
                    finance_date.append(u'无')
                try:
                    finance_round.append(dic["round"] or u'无')
                except:
                    finance_round.append(u'无')

                try:
                    valuation.append(dic["value"] or u'无')
                except:
                    valuation.append(u'无')

                try:
                    finance_amount.append(dic["money"] or u'无')
                except:
                    finance_amount.append(u'无')

                try:
                    finance_proportion.append(dic["share"] or u'无')
                except:
                    finance_proportion.append(u'无')

                try:
                    investor.append(("，".join(re.findall(r'[\{|\,](.*?)\:', dic["rongziMap"]))) or u'无')
                except:
                    investor.append(u'无')

                try:
                    news_title.append(dic["newsTitle"] or u'无')
                except:
                    news_title.append(u'无')

                try:
                    news_url.append(dic["newsUrl"] or u'无')
                except:
                    news_url.append(u'无')

        if len(response.body) > 6000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/findHistoryRongzi.json?name=' + str(item["company_name"]) + '&ps=10&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_finance_history)
            yield request

        else:
            item["member_name"] = ['None']
            item["member_pos"] = ['None']
            item["member_intro"] = ['None']
            item["member_icon"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/findTeamMember.json?name=' + str(item["company_name"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_core_team)
            yield request

    def parse_core_team(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        member_name = item["member_name"]
        member_pos = item["member_pos"]
        member_intro = item["member_intro"]
        member_icon = item["member_icon"]

        if flag[9] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["page"]["rows"]:
                try:
                    member_name.append(dic["name"] or u'无')
                except:
                    member_name.append(u'无')

                try:
                    member_pos.append(dic["title"] or u'无')
                except:
                    member_pos.append(u'无')

                try:
                    member_intro.append(dic["desc"] or u'无')
                except:
                    member_intro.append(u'无')

                try:
                    member_icon.append(dic["icon"] or u'无')
                except:
                    member_icon.append(u'无')

        item["member_name"] = member_name
        item["member_pos"] = member_pos
        item["member_intro"] = member_intro
        item["member_icon"] = member_icon

        if len(response.body) > 3000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/findTeamMember.json?name=' + str(item["company_name"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_core_team)
            yield request
        else:
            item["business_name"] = ['None']
            item["business_type"] = ['None']
            item["business_intro"] = ['None']
            item["business_logo"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/findProduct.json?name=' + str(item["company_name"]) + '&ps=15&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_enterprise_business)
            yield request

    def parse_enterprise_business(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        product_name = item["business_name"]
        product_type = item["business_type"]
        product_short = item["business_intro"]
        product_logo = item["business_logo"]

        if flag[10] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["page"]["rows"]:
                try:
                    product_name.append(dic["product"] or u'无')
                except:
                    product_name.append(u'无')

                try:
                    product_type.append(dic["hangye"] or u'无')
                except:
                    product_type.append(u'无')

                try:
                    product_short.append(dic["yewu"] or u'无')
                except:
                    product_short.append(u'无')

                try:
                    product_logo.append(dic["logo"] or u'无')
                except:
                    product_logo.append(u'无')

        item["business_name"] = product_name
        item["business_type"] = product_type
        item["business_intro"] = product_short
        item["business_logo"] = product_logo

        if len(response.body) > 7000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/findProduct.json?name=' + str(item["company_name"]) + '&ps=15&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_enterprise_business)
            yield request
        else:
            item["invest_time"] = ['None']
            item["invest_round"] = ['None']
            item["invest_amount"] = ['None']
            item["invest_company"] = ['None']
            item["invest_product"] = ['None']
            item["invest_pro_icon"] = ['None']
            item["invest_area"] = ['None']
            item["invest_industry"] = ['None']
            item["invest_business"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/findTzanli.json?name=' + str(item["company_name"]) + '&ps=10&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_investment_event)
            yield request

    def parse_investment_event(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        invest_time = item["invest_time"]
        invest_round = item["invest_round"]
        invest_amount = item["invest_amount"]
        invest_company = item["invest_company"]
        invest_product = item["invest_product"]
        invest_pro_icon = item["invest_pro_icon"]
        invest_area = item["invest_area"]
        invest_industry = item["invest_industry"]
        invest_business = item["invest_business"]

        if flag[11] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["page"]["rows"]:
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["tzdate"])[:10])))
                    invest_time.append(str(date))
                except:
                    invest_time.append(u'无')
                try:
                    invest_round.append(dic["lunci"] or u'无')
                except:
                    invest_round.append(u'无')
                try:
                    invest_amount.append(dic["money"] or u'无')
                except:
                    invest_amount.append(u'无')
                try:
                    invest_company.append(("，".join(re.findall(r'[\{|\,](.*?)\:', dic["rongzi_map"])) or u'无'))
                except:
                    invest_company.append(u'无')

                try:
                    invest_pro_icon.append(dic["icon"] or u'无')
                except:
                    invest_pro_icon.append(u'无')
                try:
                    invest_area.append(dic["location"] or u'无')
                except:
                    invest_area.append(u'无')
                try:
                    invest_product.append(dic["product"] or u'无')
                except:
                    invest_product.append(u'无')

                try:
                    invest_industry.append(dic["hangye1"] or u'无')
                except:
                    invest_industry.append(u'无')

                try:
                    invest_business.append(dic["yewu"] or u'无')
                except:
                    invest_business.append(u'无')

        item["invest_time"] = invest_time
        item["invest_round"] = invest_round
        item["invest_amount"] = invest_amount
        item["invest_company"] = invest_company
        item["invest_product"] = invest_product
        item["invest_pro_icon"] = invest_pro_icon
        item["invest_area"] = invest_area
        item["invest_industry"] = invest_industry
        item["invest_business"] = invest_business

        if len(response.body) > 3000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/findTzanli.json?name=' + str(item["company_name"]) + '&ps=10&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_investment_event)
            yield request
        else:
            item["product_name"] = ['None']
            item["product_logo"] = ['None']
            item["product_area"] = ['None']
            item["product_round"] = ['None']
            item["product_industry"] = ['None']
            item["product_business"] = ['None']
            item["setup_date"] = ['None']
            item["product_valuation"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/findJingpin.json?name=' + str(item["company_name"]) + '&ps=10&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_competing_product)
            yield request

    def parse_competing_product(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        product_name = item["product_name"]
        product_logo = item["product_logo"]
        product_area = item["product_area"]
        product_round = item["product_round"]
        product_industry = item["product_industry"]
        product_business = item["product_business"]
        setup_date = item["setup_date"]
        product_valuation = item["product_valuation"]

        if flag[12] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["page"]["rows"]:
                try:
                    product_name.append(dic["jingpinProduct"] or u'无')
                except:
                    product_name.append(u'无')
                try:
                    product_logo.append(dic["icon"] or u'无')
                except:
                    product_logo.append(u'无')
                try:
                    product_area.append(dic["location"] or u'无')
                except:
                    product_area.append(u'无')
                try:
                    product_round.append(dic["round"] or u'无')
                except:
                    product_round.append(u'无')
                try:
                    product_industry.append(dic["hangye"] or u'无')
                except:
                    product_industry.append(u'无')
                try:
                    product_business.append(dic["yewu"] or u'无')
                except:
                    product_business.append(u'无')
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["setupDate"])[:10])))
                    setup_date.append(date or u'无')
                except:
                    setup_date.append(u'无')
                try:
                    product_valuation.append(dic["value"] or u'无')
                except:
                    product_valuation.append(u'无')

        item["product_name"] = product_name
        item["product_logo"] = product_logo
        item["product_area"] = product_area
        item["product_round"] = product_round
        item["product_industry"] = product_industry
        item["product_business"] = product_business
        item["setup_date"] = setup_date
        item["product_valuation"] = product_valuation

        if len(response.body) > 3000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/findJingpin.json?name=' + str(item["company_name"]) + '&ps=10&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_competing_product)
            yield request
        else:
            next_url = 'http://www.tianyancha.com/v2/court/' + str(item["company_name"]) + '.json?'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_court_announcement)
            yield request

    def parse_court_announcement(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        announce_time = ['None']
        appeal = ['None']
        respondent = ['None']
        announce_type = ['None']
        court = ['None']
        announce_content = ['None']

        if flag[14] == 1:
            data = json.loads(response.body)
            for dic in data["courtAnnouncements"]:
                try:
                    announce_time.append(dic["publishdate"] or u'无')
                except:
                    announce_time.append(u'无')
                try:
                    appeal.append(dic["party1"] or u'无')
                except:
                    appeal.append(u'无')
                try:
                    respondent.append(dic["party2"] or u'无')
                except:
                    respondent.append(u'无')
                try:
                    announce_type.append(dic["bltntypename"] or u'无')
                except:
                    announce_type.append(u'无')

                try:
                    court.append(dic["courtcode"] or u'无')
                except:
                    court.append(u'无')

                try:
                    announce_content.append(dic["content"] or u'无')
                except:
                    announce_content.append(u'无')

        item["announce_time"] = announce_time
        item["appeal"] = appeal
        item["respondent"] = respondent
        item["announce_type"] = announce_type
        item["court"] = court
        item["announce_content"] = announce_content

        next_url = 'http://www.tianyancha.com/v2/dishonest/' + str(item["company_name"]) +'.json'
        request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_the_dishonest)
        yield request

    def parse_the_dishonest(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        dis_company = ['None']
        dic_legalrepre = ['None']
        dis_code = ['None']
        execute_number = ['None']
        case_number = ['None']
        execute_unite = ['None']
        legal_obligation = ['None']
        performance = ['None']
        execute_court = ['None']
        province = ['None']
        filing_time = ['None']
        pub_time = ['None']

        if flag[15] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["items"]:
                try:
                    dis_company.append(dic["iname"] or u'无')
                except:
                    dis_company.append(u'无')

                try:
                    dic_legalrepre.append(dic["businessentity"] or u'无')
                except:
                    dic_legalrepre.append(u'无')

                try:
                    dis_code.append(dic["cardnum"] or u'无')
                except:
                    dis_code.append(u'无')
                try:
                    execute_number.append(dic["casecode"] or u'无')
                except:
                    execute_number.append(u'无')

                try:
                    case_number.append(dic["gistid"] or u'无')
                except:
                    case_number.append(u'无')

                try:
                    execute_unite.append(dic["gistunit"] or u'无')
                except:
                    execute_unite.append(u'无')
                try:
                    legal_obligation.append(dic["duty"] or u'无')
                except:
                    legal_obligation.append(u'无')

                try:
                    performance.append(dic["performance"] or u'无')
                except:
                    performance.append(u'无')

                try:
                    execute_court.append(dic["courtname"] or u'无')
                except:
                    execute_court.append(u'无')
                try:
                    province.append(dic["areaname"] or u'无')
                except:
                    province.append(u'无')
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["regdate"])[:10])))
                    filing_time.append(date)
                except:
                    filing_time.append(u'无')
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["publishdate"])[:10])))
                    pub_time.append(date)
                except:
                    pub_time.append(u'无')

        item["dis_company"] = dis_company
        item["dic_legalrepre"] = dic_legalrepre
        item["dis_code"] = dis_code
        item["execute_number"] = execute_number
        item["case_number"] = case_number
        item["execute_unite"] = execute_unite
        item["legal_obligation"] = legal_obligation
        item["performance"] = performance
        item["execute_court"] = execute_court
        item["province"] = province
        item["filing_time"] = filing_time
        item["pub_time"] = pub_time

        item["filing_date"] = ['None']
        item["executed_target"] = ['None']
        item["case_code"] = ['None']
        item["executed_court"] = ['None']

        next_url = 'http://www.tianyancha.com/expanse/zhixing.json?id=' + str(item["company_id"]) + '&ps=5&pn=1'
        request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_the_executed)
        yield request

    def parse_the_executed(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        filing_date = item["filing_date"]
        executed_target = item["executed_target"]
        case_code = item["case_code"]
        executed_court = item["executed_court"]

        if flag[16] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["items"]:
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["caseCreateTime"])[:10])))
                    filing_date.append(date)
                except:
                    filing_date.append(u'无')
                try:
                    executed_target.append(dic["execMoney"] or u'无')
                except:
                    executed_target.append(u'无')

                try:
                    case_code.append(dic["caseCode"] or u'无')
                except:
                    case_code.append(u'无')

                try:
                    executed_court.append(dic["execCourtName"] or u'无')
                except:
                    executed_court.append(u'无')

        item["filing_date"] = filing_date
        item["executed_target"] = executed_target
        item["case_code"] = case_code
        item["executed_court"] = executed_court

        if len(response.body) > 700:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/zhixing.json?id=' + str(item["company_id"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_the_executed)
            yield request
        else:
            item["include_date"] = ['None']
            item["include_reason"] = ['None']
            item["include_authority"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/abnormal.json?id=' + str(item["company_id"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_abnormal_management)
            yield request

    def parse_abnormal_management(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]
        include_date = item["include_date"]
        include_reason = item["include_reason"]
        include_authority = item["include_authority"]

        if flag[17] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["result"]:
                try:
                    include_date.append(dic["putDate"] or u'无')
                except:
                    include_date.append(u'无')

                try:
                    include_reason.append(dic["putReason"] or u'无')
                except:
                    include_reason.append(u'无')

                try:
                    include_authority.append(dic["putDepartment"] or u'无')
                except:
                    include_authority.append(u'无')

        item["include_date"] = include_date
        item["include_reason"] = include_reason
        item["include_authority"] = include_authority

        if len(response.body) > 900:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/abnormal.json?id=' + str(item["company_id"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_abnormal_management)
            yield request
        else:
            item["pub_code"] = ['None']
            item["pub_type"] = ['None']
            item["pub_content"] = ['None']
            item["pub_date"] = ['None']
            item["pub_authority"] = ['None']
            item["pub_people"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/punishment.json?name=' + str(item["company_name"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_adminis_pubnish)
            yield request

    def parse_adminis_pubnish(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        pub_code = item["pub_code"]
        pub_type = item["pub_type"]
        pub_content = item["pub_content"]
        pub_date = item["pub_date"]
        pub_authority = item["pub_authority"]
        pub_people = item["pub_people"]

        if flag[18] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["items"]:
                try:
                    pub_code.append(dic["punishNumber"] or u'无')
                except:
                    pub_code.append(u'无')

                try:
                    pub_type.append(dic["type"] or u'无')
                except:
                    pub_type.append(u'无')
                try:
                    pub_content.append(dic["content"] or u'未公示')
                except:
                    pub_content.append(u'未公示')
                try:
                    pub_date.append(dic["decisionDate"] or u'无')
                except:
                    pub_date.append(u'无')

                try:
                    pub_authority.append(dic["departmentName"] or u'无')
                except:
                    pub_authority.append(u'无')

                try:
                    pub_people.append(dic["legalPersonName"] or u'无')
                except:
                    pub_people.append(u'无')

        item["pub_code"] = pub_code
        item["pub_type"] = pub_type
        item["pub_content"] = pub_content
        item["pub_date"] = pub_date
        item["pub_authority"] = pub_authority
        item["pub_people"] = pub_people

        if len(response.body) > 1500:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/punishment.json?name=' + str(item["company_name"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_adminis_pubnish)
            yield request
        else:
            item["set_time"] = ['None']
            item["set_reason"] = ['None']
            item["set_department"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/illegal.json?name=' + str(item["company_name"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_seriously_illegal)
            yield request

    def parse_seriously_illegal(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        set_time = item["set_time"]
        set_reason = item["set_reason"]
        set_department = item["set_department"]

        if flag[19] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["items"]:
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["putDate"])[:10])))
                    set_time.append(date)
                except:
                    set_time.append(u'无')
                try:
                    set_reason.append(dic["putReason"])
                except:
                    set_reason.append(u'无')
                try:
                    set_department.append(dic["putDepartment"])
                except:
                    set_department.append(u'无')

        item["set_time"] = set_time
        item["set_reason"] = set_reason
        item["set_department"] = set_department

        if len(response.body) > 700:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/illegal.json?name=' + str(item["company_name"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_seriously_illegal)
            yield request
        else:
            item["regist_date"] = ['None']
            item["regist_num"] = ['None']
            item["regist_cond"] = ['None']
            item["pledged_amount"] = ['None']
            item["pledgor"] = ['None']
            item["pledged_code"] = ['None']
            item["pledgee"] = ['None']
            item["pledgee_code"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/companyEquity.json?name=' + str(item["company_name"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_equity_pledge)
            yield request

    def parse_equity_pledge(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        regist_date = item["regist_date"]
        regist_num = item["regist_num"]
        regist_cond = item["regist_cond"]
        pledged_amount = item["pledged_amount"]
        pledgor = item["pledgor"]
        pledged_code = item["pledged_code"]
        pledgee = item["pledgee"]
        pledgee_code = item["pledgee_code"]

        if flag[20] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["items"]:
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["regDate"])[:10])))
                    regist_date.append(date)
                except:
                    regist_date.append(u'无')
                try:
                    regist_num.append(dic["regNumber"] or u'无')
                except:
                    regist_num.append(u'无')

                try:
                    regist_cond.append(dic["state"] or u'无')
                except:
                    regist_cond.append(u'无')

                try:
                    pledged_amount.append(dic["equityAmount"] or u'无')
                except:
                    pledged_amount.append(u'无')
                try:
                    pledgor.append(dic["pledgor"] or u'无')
                except:
                    pledgor.append(u'无')

                try:
                    pledged_code.append(dic["certifNumber"] or u'无')
                except:
                    pledged_code.append(u'无')

                try:
                    pledgee.append(dic["pledgee"] or u'无')
                except:
                    pledgee.append(u'无')
                try:
                    pledgee_code.append(dic["certifNumberR"] or u'无')
                except:
                    pledgee_code.append(u'无')

        item["regist_date"] = regist_date
        item["regist_num"] = regist_num
        item["regist_cond"] = regist_cond
        item["pledged_amount"] = pledged_amount
        item["pledgor"] = pledgor
        item["pledged_code"] = pledged_code
        item["pledgee"] = pledgee
        item["pledgee_code"] = pledgee_code

        if len(response.body) > 900:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/companyEquity.json?name=' + str(item["company_name"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_equity_pledge)
            yield request
        else:
            item["registed_num"] = ['None']
            item["registed_depart"] = ['None']
            item["registed_date"] = ['None']
            item["registed_cond"] = ['None']
            item["vouched_type"] = ['None']
            item["vouched_amount"] = ['None']
            item["debt_deadline"] = ['None']
            item["vouched_range"] = ['None']
            item["mortgagee_name"] = [['None']]
            item["mortgagee_type"] = [['None']]
            item["id_number"] = [['None']]
            item["cancel_date"] = ['None']
            item["cancel_reason"] = ['None']
            item["pawn_name"] = [['None']]
            item["pawn_belong"] = [['None']]
            item["pawn_condition"] = [['None']]
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/mortgageInfo.json?name=' + str(item["company_name"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_chattel_mortgage)
            yield request

    def parse_chattel_mortgage(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        registed_num = item["registed_num"]
        registed_depart = item["registed_depart"]
        registed_date = item["registed_date"]
        registed_cond = item["registed_cond"]
        vouched_type = item["vouched_type"]
        vouched_amount = item["vouched_amount"]
        debt_deadline = item["debt_deadline"]
        vouched_range = item["vouched_range"]
        mortgagee_name = item["mortgagee_name"]
        mortgagee_type = item["mortgagee_type"]
        id_number = item["id_number"]
        cancel_date = item["cancel_date"]
        cancel_reason = item["cancel_reason"]
        pawn_name = item["pawn_name"]
        pawn_belong = item["pawn_belong"]
        pawn_condition = item["pawn_condition"]

        if flag[21] == 1:
            data = json.loads(response.body)
            data = json.loads(data["data"])
            for dic in data["items"]:
                try:
                    registed_num.append(dic["baseInfo"]["regNum"] or u'无')
                except:
                    registed_num.append(u'无')

                try:
                    registed_depart.append(dic["baseInfo"]["regDepartment"] or u'无')
                except:
                    registed_depart.append(u'无')

                try:
                    registed_date.append(dic["baseInfo"]["regDate"] or u'无')
                except:
                    registed_date.append(u'无')

                try:
                    registed_cond.append(dic["baseInfo"]["status"] or u'无')
                except:
                    registed_cond.append(u'无')

                try:
                    vouched_type.append(dic["baseInfo"]["type"] or u'无')
                except:
                    vouched_type.append(u'无')

                try:
                    vouched_amount.append(dic["baseInfo"]["amount"] or u'无')
                except:
                    vouched_amount.append(u'无')

                try:
                    debt_deadline.append(dic["baseInfo"]["term"] or u'无')
                except:
                    debt_deadline.append(u'无')

                try:
                    vouched_range.append(dic["baseInfo"]["scope"] or u'无')
                except:
                    vouched_range.append(u'无')
                try:
                    cancel_date.append(dic["baseInfo"]["cancelDate"])
                    cancel_reason.append(dic["baseInfo"]["cancelReason"])
                except:
                    cancel_date.append(u'无')
                    cancel_reason.append(u'无')
                mortgagee_name_list = []
                mortgagee_type_list = []
                id_number_list = []
                for sub_dic in dic["peopleInfo"]:
                    try:
                        mortgagee_name_list.append(sub_dic["peopleName"] or u'无')
                    except:
                        mortgagee_name_list.append(u'无')

                    try:
                        mortgagee_type_list.append(sub_dic["liceseType"] or u'无')
                    except:
                        mortgagee_type_list.append(u'无')

                    try:
                        id_number_list.append(sub_dic["licenseNum"] or u'无')
                    except:
                        id_number_list.append(u'无')
                mortgagee_name.append(mortgagee_name_list)
                mortgagee_type.append(mortgagee_type_list)
                id_number.append(id_number_list)
                pawn_name_list = []
                pawn_belong_list = []
                pawn_condition_list = []
                for sub_dic in dic["pawnInfoList"]:
                    try:
                        pawn_name_list.append(sub_dic["pawnName"] or u'无')
                    except:
                        pawn_name_list.append(u'无')

                    try:
                        pawn_belong_list.append(sub_dic["ownership"] or u'无')
                    except:
                        pawn_belong_list.append(u'无')

                    try:
                        pawn_condition_list.append(sub_dic["detail"] or u'无')
                    except:
                        pawn_condition_list.append(u'无')
                pawn_name.append(pawn_name_list)
                pawn_belong.append(pawn_belong_list)
                pawn_condition.append(pawn_condition_list)

        item["registed_num"] = registed_num
        item["registed_depart"] = registed_depart
        item["registed_date"] = registed_date
        item["registed_cond"] = registed_cond
        item["vouched_type"] = vouched_type
        item["vouched_amount"] = vouched_amount
        item["debt_deadline"] = debt_deadline
        item["vouched_range"] = vouched_range
        item["mortgagee_name"] = mortgagee_name
        item["mortgagee_type"] = mortgagee_type
        item["id_number"] = id_number
        item["cancel_date"] = cancel_date
        item["cancel_reason"] = cancel_reason
        item["pawn_name"] = pawn_name
        item["pawn_belong"] = pawn_belong
        item["pawn_condition"] = pawn_condition

        if len(response.body) > 3000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/mortgageInfo.json?name=' + str(item["company_name"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_chattel_mortgage)
            yield request
        else:
            item["tax_date"] = ['None']
            item["tax_num"] = ['None']
            item["tax_type"] = ['None']
            item["tax_current"] = ['None']
            item["tax_balance"] = ['None']
            item["tax_depart"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/owntax.json?id=' + str(item["company_id"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_owe_tax)
            yield request

    def parse_owe_tax(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        tax_date = item["tax_date"]
        tax_num = item["tax_num"]
        tax_type = item["tax_type"]
        tax_current = item["tax_current"]
        tax_balance = item["tax_balance"]
        tax_depart = item["tax_depart"]

        if flag[22] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["items"]:
                try:
                    tax_date.append(dic["publishDate"] or u'无')
                except:
                    tax_date.append(u'无')
                try:
                    tax_num.append(dic["taxIdNumber"] or u'无')
                except:
                    tax_num.append(u'无')
                try:
                    tax_type.append(dic["taxCategory"] or u'无')
                except:
                    tax_type.append(u'无')
                try:
                    tax_current.append(dic[""] or u'无')
                except:
                    tax_current.append(u'无')
                try:
                    tax_balance.append(dic["ownTaxAmount"] or u'无')
                except:
                    tax_balance.append(u'无')
                try:
                    tax_depart.append(dic[""] or u'无')
                except:
                    tax_depart.append(u'无')

        item["tax_date"] = tax_date
        item["tax_num"] = tax_num
        item["tax_type"] = tax_type
        item["tax_current"] = tax_current
        item["tax_balance"] = tax_balance
        item["tax_depart"] = tax_depart

        if len(response.body) > 800:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/owntax.json?id=' + str(item["company_id"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_owe_tax)
            yield request
        else:
            item["bid_url"] = ['None']
            item["bid_time"] = ['None']
            item["bid_title"] = ['None']
            item["bid_purchaser"] = ['None']
            item["bid_content"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/bid.json?id=' + str(item["company_id"]) + '&ps=10&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_bidding)
            yield request

    def parse_bidding(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        bid_url = item["bid_url"]
        bid_time = item["bid_time"]
        bid_title = item["bid_title"]
        bid_purchaser = item["bid_purchaser"]
        bid_content = item["bid_content"]

        try:
            data = json.loads(response.body)
            test = data["data"]["items"]
        except:
            flag[23] = 0

        if flag[23] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["items"]:
                try:
                    url = 'http://www.tianyancha.com/bid/' + str(dic["uuid"])
                    bid_url.append(url)
                except:
                    bid_url.append(u'无')
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["publishTime"])[:10])))
                    bid_time.append(date)
                except:
                    bid_time.append(u'无')
                try:
                    bid_title.append(dic["title"] or u'无')
                except:
                    bid_title.append(u'无')

                try:
                    bid_purchaser.append(dic["purchaser"] or u'无')
                except:
                    bid_purchaser.append(u'无')

                try:
                    bid_content.append(dic["content"] or u'无')
                except:
                    bid_content.append(u'无')

        item["bid_url"] = bid_url
        item["bid_time"] = bid_time
        item["bid_title"] = bid_title
        item["bid_purchaser"] = bid_purchaser
        item["bid_content"] = bid_content

        if len(response.body) > 10000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/bid.json?id=' + str(item["company_id"]) + '&ps=10&pn=1' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_bidding)
            yield request
        else:
            item["bond_name"] = ['None']
            item["bond_code"] = ['None']
            item["bond_publisher"] = ['None']
            item["bond_type"] = ['None']
            item["bond_start"] = ['None']
            item["bond_end"] = ['None']
            item["bond_duration"] = ['None']
            item["trading_day"] = ['None']
            item["interest_mode"] = ['None']
            item["bond_delisting"] = ['None']
            item["credit_agency"] = ['None']
            item["bond_rating"] = ['None']
            item["face_value"] = ['None']
            item["reference_rate"] = ['None']
            item["coupon_rate"] = ['None']
            item["actual_circulation"] = ['None']
            item["planned_circulation"] = ['None']
            item["issue_price"] = ['None']
            item["spread"] = ['None']
            item["frequency"] = ['None']
            item["bond_date"] = ['None']
            item["exercise_type"] = ['None']
            item["exercise_date"] = ['None']
            item["trustee"] = ['None']
            item["circulation_scope"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/extend/getBondList.json?companyName=' + str(item["company_name"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_bond_infomation)
            yield request

    def parse_bond_infomation(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]
        bond_name = item["bond_name"]
        bond_code = item["bond_code"]
        bond_publisher = item["bond_publisher"]
        bond_type = item["bond_type"]
        bond_start = item["bond_start"]
        bond_end = item["bond_end"]
        bond_duration = item["bond_duration"]
        trading_day = item["trading_day"]
        interest_mode = item["interest_mode"]
        bond_delisting = item["bond_delisting"]
        credit_agency = item["credit_agency"]
        bond_rating = item["bond_rating"]
        face_value = item["face_value"]
        reference_rate = item["reference_rate"]
        coupon_rate = item["coupon_rate"]
        actual_circulation = item["actual_circulation"]
        planned_circulation = item["planned_circulation"]
        issue_price = item["issue_price"]
        spread = item["spread"]
        frequency = item["frequency"]
        bond_date = item["bond_date"]
        exercise_type = item["exercise_type"]
        exercise_date = item["exercise_date"]
        trustee = item["trustee"]
        circulation_scope = item["circulation_scope"]

        if flag[24] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["bondList"]:
                try:
                    bond_name.append(dic["bondName"] or u'无')
                except:
                    bond_name.append(u'无')

                try:
                    bond_code.append(dic["bondNum"] or u'无')
                except:
                    bond_code.append(u'无')

                try:
                    bond_publisher.append(dic["publisherName"] or u'无')
                except:
                    bond_publisher.append(u'无')
                try:
                    bond_type.append(dic["bondType"] or u'无')
                except:
                    bond_type.append(u'无')
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["publishTime"])[:10])))
                    bond_start.append(date)
                except:
                    bond_start.append(u'无')
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["publishExpireTime"])[:10])))
                    bond_end.append(date)
                except:
                    bond_end.append(u'无')
                try:
                    bond_duration.append(dic["bondTimeLimit"] or u'无')
                except:
                    bond_duration.append(u'无')

                try:
                    trading_day.append(dic["bondTradeTime"] or u'无')
                except:
                    trading_day.append(u'无')

                try:
                    interest_mode.append(dic["calInterestType"] or u'无')
                except:
                    interest_mode.append(u'无')

                try:
                    bond_delisting.append(dic["bondStopTime"] or u'无')
                except:
                    bond_delisting.append(u'无')
                try:
                    credit_agency.append(dic["creditRatingGov"] or u'未公示')
                except:
                    credit_agency.append(u'未公示')
                try:
                    bond_rating.append(dic["debtRating"] or u'未公示')
                except:
                    bond_rating.append(u'未公示')
                try:
                    face_value.append(dic["faceValue"] or u'无')
                except:
                    face_value.append(u'无')

                try:
                    reference_rate.append(dic["refInterestRate"] or u'未公示')
                except:
                    reference_rate.append(u'未公示')
                try:
                    coupon_rate.append(dic["faceInterestRate"] or u'无')
                except:
                    coupon_rate.append(u'无')

                try:
                    actual_circulation.append(dic["realIssuedQuantity"] or u'无')
                except:
                    actual_circulation.append(u'无')

                try:
                    planned_circulation.append(dic["planIssuedQuantity"] or u'无')
                except:
                    planned_circulation.append(u'无')

                try:
                    issue_price.append(dic["issuedPrice"] or u'无')
                except:
                    issue_price.append(u'无')

                try:
                    spread.append(dic["interestDiff"] or u'未公示')
                except:
                    spread.append(u'未公示')
                try:
                    frequency.append(dic["payInterestHZ"] or u'无')
                except:
                    frequency.append(u'无')

                try:
                    bond_date.append(dic["startCalInterestTime"] or u'无')
                except:
                    bond_date.append(u'无')

                try:
                    trustee.append(dic["escrowAgent"] or u'无')
                except:
                    trustee.append(u'无')

                try:
                    circulation_scope.append(dic["flowRange"] or u'无')
                except:
                    circulation_scope.append(u'无')
                try:
                    exercise_type.append(dic["exeRightType"] or u'未公示')
                except:
                    exercise_type.append(u'未公示')
                try:
                    exercise_date.append(dic["exeRightTime"] or u'未公示')
                except:
                    exercise_date.append(u'未公示')

        item["bond_name"] = bond_name
        item["bond_code"] = bond_code
        item["bond_publisher"] = bond_publisher
        item["bond_type"] = bond_type
        item["bond_start"] = bond_start
        item["bond_end"] = bond_end
        item["bond_duration"] = bond_duration
        item["trading_day"] = trading_day
        item["interest_mode"] = interest_mode
        item["bond_delisting"] = bond_delisting
        item["credit_agency"] = credit_agency
        item["bond_rating"] = bond_rating
        item["face_value"] = face_value
        item["reference_rate"] = reference_rate
        item["coupon_rate"] = coupon_rate
        item["actual_circulation"] = actual_circulation
        item["planned_circulation"] = planned_circulation
        item["issue_price"] = issue_price
        item["spread"] = spread
        item["frequency"] = frequency
        item["bond_date"] = bond_date
        item["exercise_type"] = exercise_type
        item["exercise_date"] = exercise_date
        item["trustee"] = trustee
        item["circulation_scope"] = circulation_scope

        if len(response.body) > 2000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/extend/getBondList.json?companyName=' + str(item["company_name"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_bond_infomation)
            yield request
        else:
            item["admini_region"] = ['None']
            item["supervision_num"] = ['None']
            item["pruchase_trustee"] = ['None']
            item["trasaction_price"] = ['None']
            item["signed_date"] = ['None']
            item["total_area"] = ['None']
            item["parcel_location"] = ['None']
            item["purchase_assignee"] = ['None']
            item["superior_company"] = ['None']
            item["land_use"] = ['None']
            item["supply_mode"] = ['None']
            item["max_volume"] = ['None']
            item["min_volume"] = ['None']
            item["start_time"] = ['None']
            item["end_time"] = ['None']
            item["link_url"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/purchaseland.json?name=' + str(item["company_name"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_purchase_island)
            yield request

    def parse_purchase_island(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        admini_region = item["admini_region"]
        supervision_num = item["supervision_num"]
        pruchase_trustee = item["pruchase_trustee"]
        trasaction_price = item["trasaction_price"]
        signed_date = item["signed_date"]
        total_area = item["total_area"]
        parcel_location = item["parcel_location"]
        purchase_assignee = item["purchase_assignee"]
        superior_company = item["superior_company"]
        land_use = item["land_use"]
        supply_mode = item["supply_mode"]
        max_volume = item["max_volume"]
        min_volume = item["min_volume"]
        start_time = item["start_time"]
        end_time = item["end_time"]
        link_url = item["link_url"]

        if flag[25] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["companyPurchaseLandList"]:
                try:
                    admini_region.append(dic["adminRegion"] or u'无')
                except:
                    admini_region.append(u'无')

                try:
                    supervision_num.append(dic["elecSupervisorNo"] or u'无')
                except:
                    supervision_num.append(u'无')

                try:
                    pruchase_trustee.append(dic["assignee"] or u'无')
                except:
                    pruchase_trustee.append(u'无')

                try:
                    trasaction_price.append(dic["dealPrice"] or u'无')
                except:
                    trasaction_price.append(u'无')
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["signedDate"])[:10])))
                    signed_date.append(date)
                except:
                    signed_date.append(u'无')
                try:
                    total_area.append(dic["totalArea"] or u'无')
                except:
                    total_area.append(u'无')

                try:
                    parcel_location.append(dic["location"] or u'无')
                except:
                    parcel_location.append(u'无')

                try:
                    purchase_assignee.append(dic["assignee"] or u'无')
                except:
                    purchase_assignee.append(u'无')

                try:
                    superior_company.append(dic["parentCompany"] or u'无')
                except:
                    superior_company.append(u'无')

                try:
                    land_use.append(dic["purpose"] or u'无')
                except:
                    land_use.append(u'无')

                try:
                    supply_mode.append(dic["supplyWay"] or u'无')
                except:
                    supply_mode.append(u'无')

                try:
                    max_volume.append(dic["maxVolume"] or u'无')
                except:
                    max_volume.append(u'无')

                try:
                    min_volume.append(dic["minVolume"] or u'无')
                except:
                    min_volume.append(u'无')
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["startTime"])[:10])))
                    start_time.append(date)
                except:
                    start_time.append(u'无')
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["endTime"])[:10])))
                    end_time.append(date)
                except:
                    end_time.append(u'无')
                try:
                    link_url.append(dic["linkUrl"] or u'无')
                except:
                    link_url.append(u'无')

        item["admini_region"] = admini_region
        item["supervision_num"] = supervision_num
        item["pruchase_trustee"] = pruchase_trustee
        item["trasaction_price"] = trasaction_price
        item["signed_date"] = signed_date
        item["total_area"] = total_area
        item["parcel_location"] = parcel_location
        item["purchase_assignee"] = purchase_assignee
        item["superior_company"] = superior_company
        item["land_use"] = land_use
        item["supply_mode"] = supply_mode
        item["max_volume"] = max_volume
        item["min_volume"] = min_volume
        item["start_time"] = start_time
        item["end_time"] = end_time
        item["link_url"] = link_url

        if len(response.body) > 2000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/purchaseland.json?name=' + str(item["company_name"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_purchase_island)
            yield request
        else:
            item["employ_position"] = ['None']
            item["employ_city"] = ['None']
            item["employ_area"] = ['None']
            item["employ_company"] = ['None']
            item["wage"] = ['None']
            item["experience"] = ['None']
            item["source"] = ['None']
            item["source_url"] = ['None']
            item["start_date"] = ['None']
            item["end_date"] = ['None']
            item["education"] = ['None']
            item["employ_num"] = ['None']
            item["position_desc"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/extend/getEmploymentList.json?companyName=' + str(item["company_name"]) + '&ps=10&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_the_employ)
            yield request

    def parse_the_employ(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        employ_position = item["employ_position"]
        employ_city = item["employ_city"]
        employ_area = item["employ_area"]
        employ_company = item["employ_company"]
        wage = item["wage"]
        experience = item["experience"]
        source = item["source"]
        source_url = item["source_url"]
        start_date = item["start_date"]
        end_date = item["end_date"]
        education = item["education"]
        employ_num = item["employ_num"]
        position_desc = item["position_desc"]

        if flag[26] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["companyEmploymentList"]:
                try:
                    employ_position.append(dic["title"] or u'无')
                except:
                    employ_position.append(u'无')

                try:
                    employ_city.append(dic["city"] or u'无')
                except:
                    employ_city.append(u'无')

                try:
                    employ_area.append(dic["district"] or u'无')
                except:
                    employ_area.append(u'无')

                try:
                    employ_company.append(dic["companyName"] or u'无')
                except:
                    employ_company.append(u'无')

                try:
                    wage.append(dic["oriSalary"] or u'无')
                except:
                    wage.append(u'无')

                try:
                    experience.append(dic["experience"] or u'无')
                except:
                    experience.append(u'无')

                try:
                    source.append(dic["source"] or u'无')
                except:
                    source.append(u'无')

                try:
                    source_url.append(dic["urlPath"] or u'无')
                except:
                    source_url.append(u'无')
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["startdate"])[:10])))
                    start_date.append(date)
                except:
                    start_date.append(u'无')
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["enddate"])[:10])))
                    end_date.append(date)
                except:
                    end_date.append(u'无')
                try:
                    education.append(dic["education"] or u'无')
                except:
                    education.append(u'无')

                try:
                    employ_num.append(dic["employerNumber"] or u'无')
                except:
                    employ_num.append(u'无')

                try:
                    position_desc.append(dic["description"] or u'无')
                except:
                    position_desc.append(u'无')

        item["employ_position"] = employ_position
        item["employ_city"] = employ_city
        item["employ_area"] = employ_area
        item["employ_company"] = employ_company
        item["wage"] = wage
        item["experience"] = experience
        item["source"] = source
        item["source_url"] = source_url
        item["start_date"] = start_date
        item["end_date"] = end_date
        item["education"] = education
        item["employ_num"] = employ_num
        item["position_desc"] = position_desc

        if len(response.body) > 6000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/extend/getEmploymentList.json?companyName=' + str(item["company_name"]) + '&ps=10&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_the_employ)
            yield request
        else:
            item["rating_year"] = ['None']
            item["rating_level"] = ['None']
            item["rating_type"] = ['None']
            item["rating_num"] = ['None']
            item["rating_office"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/taxcredit.json?id=' + str(item["company_id"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_rating_tax)
            yield request

    def parse_rating_tax(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        rating_year = item["rating_year"]
        rating_level = item["rating_level"]
        rating_type = item["rating_type"]
        rating_num = item["rating_num"]
        rating_office = item["rating_office"]

        if flag[27] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["items"]:
                try:
                    rating_year.append(dic["year"] or u'无')
                except:
                    rating_year.append(u'无')

                try:
                    rating_level.append(dic["grade"] or u'无')
                except:
                    rating_level.append(u'无')

                try:
                    rating_type.append(dic["type"] or u'无')
                except:
                    rating_type.append(u'无')

                try:
                    rating_num.append(dic["idNumber"] or u'无')
                except:
                    rating_num.append(u'无')

                try:
                    rating_office.append(dic["evalDepartment"] or u'无')
                except:
                    rating_office.append(u'无')

        if len(response.body) > 500:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/taxcredit.json?id=' + str(item["company_id"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_rating_tax)
            yield request
        else:
            item["check_date"] = ['None']
            item["check_type"] = ['None']
            item["check_result"] = ['None']
            item["check_office"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/companyCheckInfo.json?name=' + str(item["company_name"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_random_check)
            yield request

    def parse_random_check(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        check_date = item["check_date"]
        check_type = item["check_type"]
        check_result = item["check_result"]
        check_office = item["check_office"]

        if flag[28] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["items"]:
                try:
                    check_date.append(dic["checkDate"] or '无')
                except:
                    check_date.append('无')
                try:
                    check_type.append(dic["checkType"] or '无')
                except:
                    check_type.append('无')
                try:
                    check_result.append(dic["checkResult"] or '无')
                except:
                    check_result.append('无')
                try:
                    check_office.append(dic["checkOrg"] or '无')
                except:
                    check_office.append('无')

        item["check_date"] = check_date
        item["check_type"] = check_type
        item["check_result"] = check_result
        item["check_office"] = check_office

        if len(response.body) > 300:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/companyCheckInfo.json?name=' + str(item["company_name"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_random_check)
            yield request
        else:
            item["product_icon"] = ['None']
            item["product_title"] = ['None']
            item["product_short"] = ['None']
            item["product_type"] = ['None']
            item["product_field"] = ['None']
            item["product_desc"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/appbkinfo.json?id=' + str(item["company_id"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_product_info)
            yield request

    def parse_product_info(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        product_icon = item["product_icon"]
        product_title = item["product_title"]
        product_short = item["product_short"]
        product_type = item["product_type"]
        product_field = item["product_field"]
        product_desc = item["product_desc"]

        if flag[29] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["items"]:
                try:
                    product_icon.append(dic["icon"] or u'无')
                except:
                    product_icon.append(u'无')

                try:
                    product_title.append(dic["name"] or u'无')
                except:
                    product_title.append(u'无')

                try:
                    product_short.append(dic["filterName"] or u'无')
                except:
                    product_short.append(u'无')

                try:
                    product_type.append(dic["type"] or u'无')
                except:
                    product_type.append(u'无')

                try:
                    product_field.append(dic["classes"] or u'无')
                except:
                    product_field.append(u'无')

                try:
                    product_desc.append(dic["brief"] or u'无')
                except:
                    product_desc.append(u'无')

        item["product_icon"] = product_icon
        item["product_title"] = product_title
        item["product_short"] = product_short
        item["product_type"] = product_type
        item["product_field"] = product_field
        item["product_desc"] = product_desc

        if len(response.body) > 3000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/appbkinfo.json?id=' + str(item["company_id"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_product_info)
            yield request
        else:
            item["device_name"] = ['None']
            item["cert_type"] = ['None']
            item["cert_start"] = ['None']
            item["cert_end"] = ['None']
            item["device_num"] = ['None']
            item["permit_num"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/qualification.json?id=' + str(item["company_id"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_quality_cert)
            yield request

    def parse_quality_cert(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        device_name = item["device_name"]
        cert_type = item["cert_type"]
        cert_start = item["cert_start"]
        cert_end = item["cert_end"]
        device_num = item["device_num"]
        permit_num = item["permit_num"]

        if flag[30] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["items"]:
                try:
                    device_num.append(dic["deviceType"] or u'无')
                except:
                    device_num.append(u'无')

                try:
                    permit_num.append(dic["licenceNum"] or u'无')
                except:
                    permit_num.append(u'无')

                try:
                    device_name.append(dic["deviceName"] or u'无')
                except:
                    device_name.append(u'无')

                try:
                    cert_type.append(dic["licenceType"] or u'无')
                except:
                    cert_type.append(u'无')
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["issueDate"])[:10])))
                    cert_start.append(date)
                except:
                    cert_start.append(u'无')
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["toDate"])[:10])))
                    cert_end.append(date)
                except:
                    cert_end.append(u'无')


        item["device_name"] = device_name
        item["cert_type"] = cert_type
        item["cert_start"] = cert_start
        item["cert_end"] = cert_end
        item["device_num"] = device_num
        item["permit_num"] = permit_num

        if len(response.body) > 1000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/qualification.json?id=' + str(item["company_id"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_quality_cert)
            yield request
        else:
            item["brand_date"] = ['None']
            item["brand_icon"] = ['None']
            item["brand_name"] = ['None']
            item["brand_num"] = ['None']
            item["brand_type"] = ['None']
            item["brand_cond"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/tm/getTmList.json?id=' + str(item["company_id"]) + '&ps=5&&pageNum=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_brand_info)
            yield request

    def parse_brand_info(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        brand_date = item["brand_date"]
        brand_icon = item["brand_icon"]
        brand_name = item["brand_name"]
        brand_num = item["brand_num"]
        brand_type = item["brand_type"]
        brand_cond = item["brand_cond"]

        data = json.loads(response.body)
        try:
            test = data["data"]["items"]
        except:
            flag[31] = 0

        if flag[31] == 1:
            for dic in data["data"]["items"]:
                try:
                    date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["appDate"])[:10])))
                    brand_date.append(date)
                except:
                    brand_date.append(u'无')
                try:
                    brand_icon.append(dic["tmPic"] or u'无')
                except:
                    brand_icon.append(u'无')
                try:
                    brand_name.append(dic["tmName"] or u'无')
                except:
                    brand_name.append(u'无')
                try:
                    brand_num.append(dic["regNo"] or u'无')
                except:
                    brand_num.append(u'无')
                try:
                    brand_type.append(dic["intCls"] or u'无')
                except:
                    brand_type.append(u'无')
                try:
                    brand_cond.append(dic["category"] or u'无')
                except:
                    brand_cond.append(u'无')

        item["brand_date"] = brand_date
        item["brand_icon"] = brand_icon
        item["brand_name"] = brand_name
        item["brand_num"] = brand_num
        item["brand_type"] = brand_type
        item["brand_cond"] = brand_cond

        if len(response.body) > 800:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/tm/getTmList.json?id=' + str(item["company_id"]) + '&ps=5&&pageNum=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_brand_info)
            yield request
        else:
            item["patent_id"] = ['None']
            item["patent_pic"] = ['None']
            item["app_num"] = ['None']
            item["patent_num"] = ['None']
            item["category_num"] = ['None']
            item["patent_name"] = ['None']
            item["patent_address"] = ['None']
            item["inventor"] = ['None']
            item["applicant"] = ['None']
            item["apply_date"] = ['None']
            item["publish_date"] = ['None']
            item["agency"] = ['None']
            item["agent"] = ['None']
            item["abstracts"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/patent.json?id=' + str(item["company_id"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_patent_info)
            yield request

    def parse_patent_info(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        patent_id = item["patent_id"]
        patent_pic = item["patent_pic"]
        app_num = item["app_num"]
        patent_num = item["patent_num"]
        category_num = item["category_num"]
        patent_name = item["patent_name"]
        patent_address = item["patent_address"]
        inventor = item["inventor"]
        applicant = item["applicant"]
        apply_date = item["apply_date"]
        publish_date = item["publish_date"]
        agency = item["agency"]
        agent = item["agent"]
        abstracts = item["abstracts"]

        data = json.loads(response.body)
        try:
            test = data["data"]["items"]
        except:
            flag[32] = 0

        if flag[32] == 1:
            for dic in data["data"]["items"]:
                try:
                    patent_pic.append(dic["imgUrl"] or u'无')
                except:
                    patent_pic.append("u'无'")
                try:
                    app_num.append(dic["applicationPublishNum"] or u'无')
                except:
                    app_num.append(u'无')

                try:
                    patent_num.append(dic["patentNum"] or u'无')
                except:
                    patent_num.append(u'无')

                try:
                    category_num.append(dic["allCatNum"] or u'无')
                except:
                    category_num.append(u'无')

                try:
                    patent_name.append(dic["patentName"] or u'无')
                except:
                    patent_name.append(u'无')

                try:
                    patent_address.append(dic["address"] or u'无')
                except:
                    patent_address.append(u'无')

                try:
                    inventor.append(dic["inventor"] or u'无')
                except:
                    inventor.append(u'无')

                try:
                    applicant.append(dic["applicantName"] or u'无')
                except:
                    applicant.append(u'无')

                try:
                    apply_date.append(dic["applicationTime"] or u'无')
                except:
                    apply_date.append(u'无')

                try:
                    publish_date.append(dic["applicationPublishTime"] or u'无')
                except:
                    publish_date.append(u'无')

                try:
                    patent_id.append(dic["pid"] or u'无')
                except:
                    patent_id.append(u'无')
                try:
                    agency.append(dic["agency"] or u'无')
                except:
                    agency.append(u'无')
                try:
                    agent.append(dic["agent"] or u'无')
                except:
                    agent.append(u'无')
                try:
                    abstracts.append(dic["abstracts"] or u'无')
                except:
                    abstracts.append(u'无')

        item["patent_id"] = patent_id
        item["patent_pic"] = patent_pic
        item["app_num"] = app_num
        item["patent_num"] = patent_num
        item["category_num"] = category_num
        item["patent_name"] = patent_name
        item["patent_address"] = patent_address
        item["inventor"] = inventor
        item["applicant"] = applicant
        item["apply_date"] = apply_date
        item["publish_date"] = publish_date
        item["agency"] = agency
        item["agent"] = agent
        item["abstracts"] = abstracts

        if len(response.body) > 5000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/patent.json?id=' + str(item["company_id"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_patent_info)
            yield request
        else:
            item["full_name"] = ['None']
            item["simple_name"] = ['None']
            item["reg_num"] = ['None']
            item["cat_num"] = ['None']
            item["version"] = ['None']
            item["author_nationality"] = ['None']
            item["first_publish"] = ['None']
            item["reg_time"] = ['None']
            item["page"] = 1

            next_url = 'http://www.tianyancha.com/expanse/copyReg.json?id=' + str(item["company_id"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_copyright_info)
            yield request

    def parse_copyright_info(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        full_name = item["full_name"]
        simple_name = item["simple_name"]
        reg_num = item["reg_num"]
        cat_num = item["cat_num"]
        version = item["version"]
        author_nationality = item["author_nationality"]
        first_publish = item["first_publish"]
        reg_time = item["reg_time"]

        data = json.loads(response.body)
        try:
            test = data["data"]["items"]
        except:
            flag[33] = 0

        if flag[33] == 1:
            for dic in data["data"]["items"]:
                try:
                    simple_name.append(dic["simplename"] or u'无')
                except:
                    simple_name.append(u'无')
                try:
                    reg_num.append(dic["regnum"] or u'无')
                except:
                    reg_num.append(u'无')

                try:
                    cat_num.append(dic["catnum"] or u'无')
                except:
                    cat_num.append(u'无')

                try:
                    version.append(dic["version"] or u'无')
                except:
                    version.append(u'无')

                try:
                    author_nationality.append(dic["authorNationality"] or u'无')
                except:
                    author_nationality.append(u'无')

                try:
                    first_publish.append(dic["publishtime"] or u'无')
                except:
                    first_publish.append(u'无')

                try:
                    reg_time.append(dic["regtime"] or u'无')
                except:
                    reg_time.append(u'无')

                try:
                    full_name.append(dic["fullname"] or u'无')
                except:
                    full_name.append(u'无')

        item["full_name"] = full_name
        item["simple_name"] = simple_name
        item["reg_num"] = reg_num
        item["cat_num"] = cat_num
        item["version"] = version
        item["author_nationality"] = author_nationality
        item["first_publish"] = first_publish
        item["reg_time"] = reg_time

        if len(response.body) > 1000:
            item["page"] += 1
            next_url = 'http://www.tianyancha.com/expanse/copyReg.json?id=' + str(item["company_id"]) + '&ps=5&pn=' + str(item["page"])
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_copyright_info)
            yield request
        else:
            next_url = 'http://www.tianyancha.com/v2/IcpList/' + str(item["company_id"]) + '.json'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_website_filing)
            yield request

    def parse_website_filing(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        record_date = ['None']
        web_name = ['None']
        web_url = ['None']
        record_num = ['None']
        web_status = ['None']
        unit_nature = ['None']

        data = json.loads(response.body)
        try:
            test = data["data"]["items"]
        except:
            flag[34] = 0

        if flag[34] == 1:
            for dic in data["data"]:
                try:
                    record_date.append(dic["examineDate"] or u'无')
                except:
                    record_date.append(u'无')

                try:
                    web_name.append(dic["webName"] or u'无')
                except:
                    web_name.append(u'无')

                try:
                    record_num.append(dic["liscense"] or u'无')
                except:
                    record_num.append(u'无')

                try:
                    web_status.append(dic["webSite"] or u'无')
                except:
                    web_status.append(u'无')

                try:
                    unit_nature.append(dic["companyType"] or u'无')
                except:
                    unit_nature.append(u'无')
                try:
                    web = '，'.join(dic["webSite"])
                    web_url.append(web)
                except:
                    web_url.append(u'无')

        item["record_date"] = record_date
        item["web_name"] = web_name
        item["web_url"] = web_url
        item["record_num"] = record_num
        item["web_status"] = web_status
        item["unit_nature"] = unit_nature

        return item