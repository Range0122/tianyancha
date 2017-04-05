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

    #企业发展-融资历史
    finance_date = scrapy.Field()
    finance_round = scrapy.Field()
    valuation = scrapy.Field()
    finance_amount = scrapy.Field()
    finance_proportion = scrapy.Field()
    investor = scrapy.Field()
    news_title = scrapy.Field()
    news_url = scrapy.Field()

    #企业发展-核心团队
    member_name = scrapy.Field()
    member_pos = scrapy.Field()
    member_intro = scrapy.Field()
    member_icon = scrapy.Field()

    #企业发展-企业业务
    business_name = scrapy.Field()
    business_type = scrapy.Field()
    business_intro = scrapy.Field()
    business_logo = scrapy.Field()

    #企业发展-投资事件
    invest_time = scrapy.Field()
    invest_round = scrapy.Field()
    invest_amount = scrapy.Field()
    invest_company = scrapy.Field()
    invest_product = scrapy.Field()
    invest_pro_icon = scrapy.Field()
    invest_area = scrapy.Field()
    invest_industry = scrapy.Field()
    invest_business = scrapy.Field()

    #企业发展-竞品信息
    product_name = scrapy.Field()
    product_logo = scrapy.Field()
    product_area = scrapy.Field()
    product_round = scrapy.Field()
    product_industry = scrapy.Field()
    product_business = scrapy.Field()
    setup_date = scrapy.Field()
    product_valuation = scrapy.Field()

    #司法风险-法院公告
    announce_time = scrapy.Field()
    appeal = scrapy.Field()
    respondent = scrapy.Field()
    announce_type = scrapy.Field()
    court = scrapy.Field()
    announce_content = scrapy.Field()

    #司法风险-失信人
    dis_company = scrapy.Field()
    dic_legalrepre = scrapy.Field()
    dis_code = scrapy.Field()
    execute_number = scrapy.Field()
    case_number = scrapy.Field()
    execute_unite = scrapy.Field()
    legal_obligation = scrapy.Field()
    performance = scrapy.Field()
    execute_court = scrapy.Field()
    province = scrapy.Field()
    filing_time = scrapy.Field()
    pub_time = scrapy.Field()

    #司法风险-被执行人
    filing_date = scrapy.Field()
    executed_target = scrapy.Field()
    case_code = scrapy.Field()
    executed_court = scrapy.Field()

    #经营风险-经营异常
    include_date = scrapy.Field()
    include_reason = scrapy.Field()
    include_authority = scrapy.Field()

    #经营风险-行政处罚
    pub_code = scrapy.Field()
    pub_type = scrapy.Field()
    pub_content = scrapy.Field()
    pub_date = scrapy.Field()
    pub_authority = scrapy.Field()
    pub_people = scrapy.Field()

    #经营风险-严重违法
    set_time = scrapy.Field()
    set_reason = scrapy.Field()
    set_department = scrapy.Field()

    #经营风险-股权出质
    regist_date = scrapy.Field()
    regist_num = scrapy.Field()
    regist_cond = scrapy.Field()
    pledged_amount = scrapy.Field()
    pledgor = scrapy.Field()
    pledged_code = scrapy.Field()
    pledgee = scrapy.Field()
    pledgee_code = scrapy.Field()

    #经营风险-动产抵押
    registed_num = scrapy.Field()
    registed_depart = scrapy.Field()
    registed_date = scrapy.Field()
    registed_cond = scrapy.Field()
    vouched_type = scrapy.Field()
    vouched_amount = scrapy.Field()
    debt_deadline = scrapy.Field()
    vouched_range = scrapy.Field()
    mortgagee_name = scrapy.Field()
    mortgagee_type = scrapy.Field()
    id_number = scrapy.Field()
    cancel_date = scrapy.Field()
    cancel_reason = scrapy.Field()
    pawn_name = scrapy.Field()
    pawn_belong = scrapy.Field()
    pawn_condition = scrapy.Field()






