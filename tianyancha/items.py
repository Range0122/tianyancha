# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TianyanchaItem(scrapy.Item):
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
