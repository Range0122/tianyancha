#  -*- coding: utf-8 -*-

#  Define here the models for your scraped items
# 
#  See documentation in:
#  http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TianyanchaItem(scrapy.Item):
    flag = scrapy.Field()
    page = scrapy.Field()

    # 企业背景-基本信息
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

    # 企业背景-主要人员
    person_id = scrapy.Field()
    person_name = scrapy.Field()
    position = scrapy.Field()

    # 企业背景-股东信息
    shareholder_id = scrapy.Field()
    shareholder_name = scrapy.Field()
    investment_proportion = scrapy.Field()
    subscribed_contribution = scrapy.Field()
    subscribed_contribution_time = scrapy.Field()
    really_contribution = scrapy.Field()

    # 企业背景-对外投资
    invested_company_id = scrapy.Field()
    invested_company_name = scrapy.Field()
    invested_representative = scrapy.Field()
    registered_cap = scrapy.Field()
    investment_amount = scrapy.Field()
    investment_prop = scrapy.Field()
    registered_date = scrapy.Field()
    condit = scrapy.Field()

    # 企业背景-变更记录
    change_time = scrapy.Field()
    change_item = scrapy.Field()
    before_change = scrapy.Field()
    after_change = scrapy.Field()

    # 企业背景-企业年报
    annual_year = scrapy.Field()
    annual_url = scrapy.Field()

    # 企业背景-分支机构
    branch_id = scrapy.Field()
    branch_name = scrapy.Field()
    branch_legalrep = scrapy.Field()
    branch_cond = scrapy.Field()
    branch_regtime = scrapy.Field()

    # 企业发展-融资历史
    finance_date = scrapy.Field()
    finance_round = scrapy.Field()
    valuation = scrapy.Field()
    finance_amount = scrapy.Field()
    finance_proportion = scrapy.Field()
    investor = scrapy.Field()
    news_title = scrapy.Field()
    news_url = scrapy.Field()

    # 企业发展-核心团队
    member_name = scrapy.Field()
    member_pos = scrapy.Field()
    member_intro = scrapy.Field()
    member_icon = scrapy.Field()

    # 企业发展-企业业务
    business_name = scrapy.Field()
    business_type = scrapy.Field()
    business_intro = scrapy.Field()
    business_logo = scrapy.Field()

    # 企业发展-投资事件
    invest_time = scrapy.Field()
    invest_round = scrapy.Field()
    invest_amount = scrapy.Field()
    invest_company = scrapy.Field()
    invest_product = scrapy.Field()
    invest_pro_icon = scrapy.Field()
    invest_area = scrapy.Field()
    invest_industry = scrapy.Field()
    invest_business = scrapy.Field()

    # 企业发展-竞品信息
    product_name = scrapy.Field()
    product_logo = scrapy.Field()
    product_area = scrapy.Field()
    product_round = scrapy.Field()
    product_industry = scrapy.Field()
    product_business = scrapy.Field()
    setup_date = scrapy.Field()
    product_valuation = scrapy.Field()

    # 司法风险-法律诉讼
    

    # 司法风险-法院公告
    announce_time = scrapy.Field()
    appeal = scrapy.Field()
    respondent = scrapy.Field()
    announce_type = scrapy.Field()
    court = scrapy.Field()
    announce_content = scrapy.Field()

    # 司法风险-失信人
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

    # 司法风险-被执行人
    filing_date = scrapy.Field()
    executed_target = scrapy.Field()
    case_code = scrapy.Field()
    executed_court = scrapy.Field()

    # 经营风险-经营异常
    include_date = scrapy.Field()
    include_reason = scrapy.Field()
    include_authority = scrapy.Field()

    # 经营风险-行政处罚
    pub_code = scrapy.Field()
    pub_type = scrapy.Field()
    pub_content = scrapy.Field()
    pub_date = scrapy.Field()
    pub_authority = scrapy.Field()
    pub_people = scrapy.Field()

    # 经营风险-严重违法
    set_time = scrapy.Field()
    set_reason = scrapy.Field()
    set_department = scrapy.Field()

    # 经营风险-股权出质
    regist_date = scrapy.Field()
    regist_num = scrapy.Field()
    regist_cond = scrapy.Field()
    pledged_amount = scrapy.Field()
    pledgor = scrapy.Field()
    pledged_code = scrapy.Field()
    pledgee = scrapy.Field()
    pledgee_code = scrapy.Field()

    # 经营风险-动产抵押
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

    # 经营风险-欠税公告
    tax_date = scrapy.Field()
    tax_num = scrapy.Field()
    tax_type = scrapy.Field()
    tax_current = scrapy.Field()
    tax_balance = scrapy.Field()
    tax_depart = scrapy.Field()

    # 经营状况-招投标
    bid_url = scrapy.Field()
    bid_time = scrapy.Field()
    bid_title = scrapy.Field()
    bid_purchaser = scrapy.Field()

    # 经营状况-债券信息
    bond_name = scrapy.Field()
    bond_code = scrapy.Field()
    bond_publisher = scrapy.Field()
    bond_type = scrapy.Field()
    bond_start = scrapy.Field()
    bond_end = scrapy.Field()
    bond_duration = scrapy.Field()
    trading_day = scrapy.Field()
    interest_mode = scrapy.Field()
    bond_delisting = scrapy.Field()
    credit_agency = scrapy.Field()
    bond_rating = scrapy.Field()
    face_value = scrapy.Field()
    reference_rate = scrapy.Field()
    coupon_rate = scrapy.Field()
    actual_circulation = scrapy.Field()
    planned_circulation = scrapy.Field()
    issue_price = scrapy.Field()
    spread = scrapy.Field()
    frequency = scrapy.Field()
    bond_date = scrapy.Field()
    exercise_type = scrapy.Field()
    exercise_date = scrapy.Field()
    trustee = scrapy.Field()
    circulation_scope = scrapy.Field()

    # 经营状况-购地信息
    admini_region = scrapy.Field()
    supervision_num = scrapy.Field()
    pruchase_trustee = scrapy.Field()
    trasaction_price = scrapy.Field()
    signed_date = scrapy.Field()
    total_area = scrapy.Field()
    parcel_location = scrapy.Field()
    purchase_assignee = scrapy.Field()
    superior_company = scrapy.Field()
    land_use = scrapy.Field()
    supply_mode = scrapy.Field()
    max_volume = scrapy.Field()
    min_volume = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    link_url = scrapy.Field()

    # 经营状况-招聘
    employ_position = scrapy.Field()
    employ_city = scrapy.Field()
    employ_area = scrapy.Field()
    employ_company = scrapy.Field()
    wage = scrapy.Field()
    experience = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    education = scrapy.Field()
    employ_num = scrapy.Field()
    position_desc = scrapy.Field()

    # 经营状况-税务评级
    rating_year = scrapy.Field()
    rating_level = scrapy.Field()
    rating_type = scrapy.Field()
    rating_num = scrapy.Field()
    rating_office = scrapy.Field()

    # 经营状况-抽查检查
    check_date = scrapy.Field()
    check_type = scrapy.Field()
    check_result = scrapy.Field()
    check_office = scrapy.Field()

    # 经营状况-产品信息
    product_icon = scrapy.Field()
    product_title = scrapy.Field()
    product_short = scrapy.Field()
    product_type = scrapy.Field()
    product_field = scrapy.Field()
    product_desc = scrapy.Field()

    # 经营状况-资质证书
    device_name = scrapy.Field()
    cert_type = scrapy.Field()
    cert_start = scrapy.Field()
    cert_end = scrapy.Field()
    device_num = scrapy.Field()
    permit_num = scrapy.Field()

    # 知识产权-商标信息
    brand_date = scrapy.Field()
    brand_icon = scrapy.Field()
    brand_name = scrapy.Field()
    brand_num = scrapy.Field()
    brand_type = scrapy.Field()
    brand_cond = scrapy.Field()

    # 知识产权-专利
    patent_id = scrapy.Field()
    patent_pic = scrapy.Field()
    app_num = scrapy.Field()
    patent_num = scrapy.Field()
    category_num = scrapy.Field()
    patent_name = scrapy.Field()
    patent_address = scrapy.Field()
    inventor = scrapy.Field()
    applicant = scrapy.Field()
    apply_date = scrapy.Field()
    publish_date = scrapy.Field()
    agency = scrapy.Field()
    agent = scrapy.Field()
    abstracts = scrapy.Field()

    # 知识产权-著作权
    full_name = scrapy.Field()
    simple_name = scrapy.Field()
    reg_num = scrapy.Field()
    cat_num = scrapy.Field()
    version = scrapy.Field()
    author_nationality = scrapy.Field()
    first_publish = scrapy.Field()
    reg_time = scrapy.Field()

    # 知识产权-网站备案
    record_date = scrapy.Field()
    web_name = scrapy.Field()
    web_url = scrapy.Field()
    record_num = scrapy.Field()
    web_status = scrapy.Field()
    unit_nature = scrapy.Field()