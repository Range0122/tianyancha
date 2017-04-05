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

        next_url = "http://www.tianyancha.com/expanse/staff.json?id=" + str(item["company_id"]) + "&ps=20&pn=1"
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

        next_url = "http://www.tianyancha.com/expanse/holder.json?id=" + str(item["company_id"]) + "&ps=20&pn=1"
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
                shareholder_id.append(dic["id"])
                shareholder_name.append(dic["name"])

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
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
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

            next_url = "http://www.tianyancha.com/expanse/inverst.json?id=" + str(item["company_id"]) + "&ps=20&pn=1"
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
                invested_company_id.append(dic["id"])
                invested_company_name.append(dic["name"])

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

                date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["estiblishTime"])[:10])))
                registered_date.append(str(date))
                condit.append(dic["regStatus"])

        item["invested_company_id"] = invested_company_id
        item["invested_company_name"] = invested_company_name
        item["invested_representative"] = invested_representative
        item["registered_cap"] = registered_cap
        item["investment_amount"] = investment_amount
        item["investment_prop"] = investment_prop
        item["registered_date"] = registered_date
        item["condit"] = condit

        if len(response.body) > 3000:
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_investment)
            yield request

        else:
            item["change_time"] = ['None']
            item["change_item"] = ['None']
            item["before_change"] = ['None']
            item["after_change"] = ['None']

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
                before_change.append(dic["contentBefore"])
                after_change.append(dic["contentAfter"])

        item["change_time"] = change_time
        item["change_item"] = change_item
        item["before_change"] = before_change
        item["after_change"] = after_change

        if len(response.body) > 800:
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
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
                url = 'http://www.tianyancha.com/reportContent/' + str(item["company_id"]) + '/' + str(dic["reportYear"])
                annual_year.append(dic["reportYear"])
                annual_url.append(url)

        item["annual_year"] = annual_year
        item["annual_url"] = annual_url

        item["branch_id"] = ['None']
        item["branch_name"] = ['None']
        item["branch_legalrep"] = ['None']
        item["branch_cond"] = ['None']
        item["branch_regtime"] = ['None']

        next_url = 'http://www.tianyancha.com/expanse/branch.json?id=' + str(item["company_id"])+ '&ps=10&pn=1'
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
                branch_id.append(dic["id"])
                branch_name.append(dic["name"])
                branch_legalrep.append(u'暂无')
                branch_cond.append(u'暂无')
                branch_regtime.append(u'暂无')

        item["branch_id"] = branch_id
        item["branch_name"] = branch_name
        item["branch_legalrep"] = branch_legalrep
        item["branch_cond"] = branch_cond
        item["branch_regtime"] = branch_regtime

        if len(response.body) > 500:
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
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
                date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["date"])[:10])))
                finance_date.append(str(date))
                finance_round.append(dic["round"])

                try:
                    valuation.append(dic["value"] or u'无')
                except:
                    valuation.append(u'无')

                finance_amount.append(dic["money"])

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
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_finance_history)
            yield request

        else:
            item["member_name"] = ['None']
            item["member_pos"] = ['None']
            item["member_intro"] = ['None']
            item["member_icon"] = ['None']

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
                member_name.append(dic["name"])
                member_pos.append(dic["title"])
                member_intro.append(dic["desc"])

                try:
                    member_icon.append(dic["icon"] or u'无')
                except:
                    member_icon.append(u'无')

        item["member_name"] = member_name
        item["member_pos"] = member_pos
        item["member_intro"] = member_intro
        item["member_icon"] = member_icon

        if len(response.body) > 3000:
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_core_team)
            yield request
        else:
            item["business_name"] = ['None']
            item["business_type"] = ['None']
            item["business_intro"] = ['None']
            item["business_logo"] = ['None']

            next_url = 'http://www.tianyancha.com/expanse/findProduct.json?name=' + str(item["company_name"]) + '&ps=15&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_enterprise_business)
            yield request

    def parse_enterprise_business(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]

        product_name = item["business_name"]
        product_type = item["business_type"]
        product_intro = item["business_intro"]
        product_logo = item["business_logo"]

        if flag[10] == 1:
            data = json.loads(response.body)
            for dic in data["data"]["page"]["rows"]:
                product_name.append(dic["product"])
                product_type.append(dic["hangye"])
                product_intro.append(dic["yewu"])

                try:
                    product_logo.append(dic["logo"] or u'无')
                except:
                    product_logo.append(u'无')

        item["business_name"] = product_name
        item["business_type"] = product_type
        item["business_intro"] = product_intro
        item["business_logo"] = product_logo

        if len(response.body) > 7000:
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
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
                date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["tzdate"])[:10])))
                invest_time.append(str(date))
                invest_round.append(dic["lunci"])
                try:
                    invest_amount.append(dic["money"] or u'无')
                except:
                    invest_amount.append(u'无')
                try:
                    invest_company.append(("，".join(re.findall(r'[\{|\,](.*?)\:', dic["rongzi_map"])) or u'无'))
                except:
                    invest_company.append(u'无')

                invest_product.append(dic["product"])
                try:
                    invest_pro_icon.append(dic["icon"] or u'无')
                except:
                    invest_pro_icon.append(u'无')
                try:
                    invest_area.append(dic["location"] or u'无')
                except:
                    invest_area.append(u'无')

                invest_industry.append(dic["hangye1"])
                invest_business.append(dic["yewu"])

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
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
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
                product_name.append(dic["jingpinProduct"])
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
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
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
                announce_time.append(dic["publishdate"])
                try:
                    appeal.append(dic["party1"] or u'无')
                except:
                    appeal.append(u'无')
                try:
                    respondent.append(dic["party2"] or u'无')
                except:
                    respondent.append(u'无')
                announce_type.append(dic["bltntypename"])
                court.append(dic["courtcode"])
                announce_content.append(dic["content"])

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
                dis_company.append(dic["iname"])
                dic_legalrepre.append(dic["businessentity"])
                dis_code.append(dic["cardnum"])
                execute_number.append(dic["casecode"])
                case_number.append(dic["gistid"])
                execute_unite.append(dic["gistunit"])
                legal_obligation.append(dic["duty"])
                performance.append(dic["performance"])
                execute_court.append(dic["courtname"])
                province.append(dic["areaname"])
                date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["regdate"])[:10])))
                filing_time.append(date)
                date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["publishdate"])[:10])))
                pub_time.append(date)

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
                date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["caseCreateTime"])[:10])))
                filing_date.append(date)
                executed_target.append(dic["execMoney"])
                case_code.append(dic["caseCode"])
                executed_court.append(dic["execCourtName"])

        item["filing_date"] = filing_date
        item["executed_target"] = executed_target
        item["case_code"] = case_code
        item["executed_court"] = executed_court

        if len(response.body) > 700:
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_the_executed)
            yield request
        else:
            item["include_date"] = ['None']
            item["include_reason"] = ['None']
            item["include_authority"] = ['None']

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
                include_date.append(dic["putDate"])
                include_reason.append(dic["putReason"])
                include_authority.append(dic["putDepartment"])

        item["include_date"] = include_date
        item["include_reason"] = include_reason
        item["include_authority"] = include_authority

        if len(response.body) > 900:
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_abnormal_management)
            yield request
        else:
            item["pub_code"] = ['None']
            item["pub_type"] = ['None']
            item["pub_content"] = ['None']
            item["pub_date"] = ['None']
            item["pub_authority"] = ['None']
            item["pub_people"] = ['None']

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
                pub_code.append(dic["punishNumber"])
                pub_type.append(dic["type"])
                try:
                    pub_content.append(dic["content"] or u'未公示')
                except:
                    pub_content.append(u'未公示')
                pub_date.append(dic["decisionDate"])
                pub_authority.append(dic["departmentName"])
                pub_people.append(dic["legalPersonName"])

        item["pub_code"] = pub_code
        item["pub_type"] = pub_type
        item["pub_content"] = pub_content
        item["pub_date"] = pub_date
        item["pub_authority"] = pub_authority
        item["pub_people"] = pub_people

        if len(response.body) > 1500:
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_adminis_pubnish)
            yield request
        else:
            item["set_time"] = ['None']
            item["set_reason"] = ['None']
            item["set_department"] = ['None']

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
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
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
                date = time.strftime("%Y-%m-%d", time.localtime(int(str(dic["regDate"])[:10])))
                regist_date.append(date)
                regist_num.append(dic["regNumber"])
                regist_cond.append(dic["state"])
                pledged_amount.append(dic["equityAmount"])
                pledgor.append(dic["pledgor"])
                pledged_code.append(dic["certifNumber"])
                pledgee.append(dic["pledgee"])
                pledgee_code.append(dic["certifNumberR"])

        item["regist_date"] = regist_date
        item["regist_num"] = regist_num
        item["regist_cond"] = regist_cond
        item["pledged_amount"] = pledged_amount
        item["pledgor"] = pledgor
        item["pledged_code"] = pledged_code
        item["pledgee"] = pledgee
        item["pledgee_code"] = pledgee_code

        if len(response.body) > 900:
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
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
            item["mortgagee_name"] = ['None']
            item["mortgagee_type"] = ['None']
            item["id_number"] = ['None']
            item["cancel_date"] = ['None']
            item["cancel_reason"] = ['None']
            item["pawn_name"] = ['None']
            item["pawn_belong"] = ['None']
            item["pawn_condition"] = ['None']

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
                registed_num.append(dic["baseInfo"]["regNum"])
                registed_depart.append(dic["baseInfo"]["regDepartment"])
                registed_date.append(dic["baseInfo"]["regDate"])
                registed_cond.append(dic["baseInfo"]["status"])
                vouched_type.append(dic["baseInfo"]["type"])
                vouched_amount.append(dic["baseInfo"]["amount"])
                debt_deadline.append(dic["baseInfo"]["term"])
                vouched_range.append(dic["baseInfo"]["scope"])
                for sub_dic in dic["peopleInfo"]:
                    mortgagee_name.append(sub_dic["peopleName"])
                    mortgagee_type.append(sub_dic["liceseType"])
                    id_number.append(sub_dic["licenseNum"])
                try:
                    cancel_date.append(dic["baseInfo"]["cancelDate"])
                    cancel_reason.append(dic["baseInfo"]["cancelReason"])
                except:
                    cancel_date.append(u'无')
                    cancel_reason.append(u'无')
                for sub_dic in dic["pawnInfoList"]:
                    pawn_name.append(sub_dic["pawnName"])
                    pawn_belong.append(sub_dic["ownership"])
                    pawn_condition.append(sub_dic["detail"])

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
            next_url = str(response.url)[:-1] + str(int(str(response.url)[-1]) + 1)
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_chattel_mortgage)
            yield request
        else:


            next_url = 'http://www.tianyancha.com/expanse/owntax.json?id=' + str(item["company_id"]) + '&ps=5&pn=1'
            request = scrapy.Request(url=next_url, meta={"item": item, "flag": flag}, callback=self.parse_owe_tax)
            yield request

    def parse_owe_tax(self, response):
        flag = response.meta["flag"]
        item = response.meta["item"]
        return item
