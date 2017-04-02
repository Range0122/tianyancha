# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TianyanchaItem(scrapy.Item):
    flag = scrapy.Field()

    #企业背景-基本信息
    company_id = scrapy.Field()
    company_name = scrapy.Field()
    legal_representative = scrapy.Field()
    registered_capital = scrapy.Field()
    registered_time = scrapy.Field()
    condition = scrapy.Field()
    registered_number = scrapy.Field()
    organization_number = scrapy.Field()
    credit_number = scrapy.Field()
    enterprise_type = scrapy.Field()
    industry = scrapy.Field()
    operating_period = scrapy.Field()
    approved_date = scrapy.Field()
    registration_authority = scrapy.Field()
    registered_address = scrapy.Field()
    business_scope = scrapy.Field()
    telephone = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    logo_location = scrapy.Field()
    address = scrapy.Field()
    score = scrapy.Field()
    former_name = scrapy.Field()

    #企业背景-主要人员
    person_id = scrapy.Field()
    person_name = scrapy.Field()
    position = scrapy.Field()

    #企业背景-股东信息
    shareholder_id = scrapy.Field()
    shareholder_name = scrapy.Field()
    investment_proportion = scrapy.Field()
    subscribed_contribution = scrapy.Field()
    subscribed_contribution_time = scrapy.Field()
    really_contribution = scrapy.Field()

    #企业背景-对外投资
    invested_company_id = scrapy.Field()
    invested_company_name = scrapy.Field()
    invested_representative = scrapy.Field()
    registered_cap = scrapy.Field()
    investment_amount = scrapy.Field()
    investment_prop = scrapy.Field()
    registered_date = scrapy.Field()
    condit = scrapy.Field()

    #企业背景-变更记录
    change_time = scrapy.Field()
    change_item = scrapy.Field()
    before_change = scrapy.Field()
    after_change = scrapy.Field()

    #企业背景-企业年报
    annual_year = scrapy.Field()
    annual_url = scrapy.Field()

    #企业背景-分支机构
    branch_id = scrapy.Field()
    branch_name = scrapy.Field()
    branch_legalrep = scrapy.Field()
    branch_cond = scrapy.Field()
    branch_regtime = scrapy.Field()

