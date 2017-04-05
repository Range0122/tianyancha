# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xml.dom.minidom
import codecs


class TianyanchaPipeline(object):
    def __init__(self):
        self.impl = xml.dom.minidom.getDOMImplementation()
        self.dom = self.impl.createDocument(None, 'root', None)
        self.root = self.dom.documentElement

        self.basic_info = ['company_name', 'company_id', 'legal_representative', 'registered_capital', 'registered_time',
                           'condition', 'registered_number', 'organization_number', 'credit_number', 'enterprise_type',
                           'industry', 'operating_period', 'approved_date', 'registration_authority', 'registered_address',
                           'business_scope', 'telephone', 'email', 'website', 'logo_location', 'address', 'score', 'former_name']
        self.main_person = ['person_id', 'person_name', 'position']
        self.shareholder_info = ['shareholder_id', 'shareholder_name', 'investment_proportion', 'subscribed_contribution',
                                 'subscribed_contribution_time', 'really_contribution']
        self.investment = ['invested_company_id', 'invested_company_name', 'invested_representative', 'registered_cap',
                           'investment_amount', 'investment_prop', 'registered_date', 'condit']
        self.change_record = ['change_time', 'change_item', 'before_change', 'after_change']
        self.annual_reports = ['annual_year', 'annual_url']
        self.branches = ['branch_id', 'branch_name', 'branch_legalrep', 'branch_cond', 'branch_regtime']
        self.finance_history = ['finance_date', 'finance_round', 'valuation', 'finance_amount', 'finance_proportion',
                                'investor', 'news_title', 'news_url']
        self.core_team = ['member_name', 'member_pos', 'member_intro', 'member_icon']
        self.enterprise_business = ['business_name', 'business_type', 'business_intro', 'business_logo']
        self.investment_event = ['invest_time', 'invest_round', 'invest_amount', 'invest_company', 'invest_product',
                                 'invest_pro_icon', 'invest_area', 'invest_industry', 'invest_business']
        self.court_announcement = ['announce_time', 'appeal', 'respondent', 'announce_type', 'court', 'announce_content']
        self.the_dishonest = ['dis_company', 'dic_legalrepre', 'dis_code', 'execute_number', 'case_number', 'execute_unite',
                             'legal_obligation', 'performance', 'execute_court', 'province', 'filing_time', 'pub_time']
        self.the_executed = ['filing_date', 'executed_target', 'case_code', 'executed_court']
        self.abnormal_management = ['include_date', 'include_reason', 'include_authority']
        self.adminis_pubnish = ['pub_code', 'pub_type', 'pub_content', 'pub_date', 'pub_authority', 'pub_people']
        self.seriously_illegal = ['set_time', 'set_reason', 'set_department']
        self.equity_pledge = ['regist_date', 'regist_num', 'regist_cond', 'pledged_amount', 'pledgor', 'pledged_code',
                              'pledgee', 'pledgee_code']
        self.chattel_mortgage = ['registed_num', 'registed_depart', 'registed_date', 'registed_cond', 'vouched_type',
                                 'vouched_amount', 'debt_deadline', 'vouched_range', 'cancel_date', 'cancel_reason']
        self.sub_chattel_mortgage1 = ['mortgagee_name', 'mortgagee_type', 'id_number']
        self.sub_chattel_mortgage2 = ['pawn_name', 'pawn_belong', 'pawn_condition']

    def process_item(self, item, spider):
        company = self.dom.createElement('company')
        basic_info = self.dom.createElement('basic_info')
        company.appendChild(basic_info)
        for item_name in self.basic_info:
            content = self.dom.createElement(str(item_name))
            data = self.dom.createTextNode(str(item[item_name]))
            content.appendChild(data)
            basic_info.appendChild(content)

        if len(item["person_id"]) > 1:
            main_person = self.dom.createElement('main_person')
            company.appendChild(main_person)
            for i in range(1, len(item["person_id"])):
                person = self.dom.createElement('person')
                main_person.appendChild(person)
                for item_name in self.main_person:
                    content = self.dom.createElement(str(item_name))
                    person.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["shareholder_id"]) > 1:
            shareholder_info = self.dom.createElement('shareholder_info')
            company.appendChild(shareholder_info)
            for i in range(1, len(item["shareholder_id"])):
                shareholder = self.dom.createElement('shareholder')
                shareholder_info.appendChild(shareholder)
                for item_name in self.shareholder_info:
                    content = self.dom.createElement(str(item_name))
                    shareholder.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["invested_company_id"]) > 1:
            investment = self.dom.createElement('investment')
            company.appendChild(investment)
            for i in range(1, len(item["invested_company_id"])):
                investment_company = self.dom.createElement('investment_company')
                investment.appendChild(investment_company)
                for item_name in self.investment:
                    content = self.dom.createElement(str(item_name))
                    investment_company.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["change_time"]) > 1:
            change_record = self.dom.createElement('change_record')
            company.appendChild(change_record)
            for i in range(1, len(item["change_time"])):
                change = self.dom.createElement('change')
                change_record.appendChild(change)
                for item_name in self.change_record:
                    content = self.dom.createElement(str(item_name))
                    change.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["annual_year"]) > 1:
            annual_reports = self.dom.createElement('annual_reports')
            company.appendChild(annual_reports)
            for i in range(1, len(item["annual_year"])):
                annual = self.dom.createElement('annual')
                annual_reports.appendChild(annual)
                for item_name in self.annual_reports:
                    content = self.dom.createElement(str(item_name))
                    annual.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["branch_id"]) > 1:
            branches = self.dom.createElement('branches')
            company.appendChild(branches)
            for i in range(1, len(item["branch_id"])):
                branch = self.dom.createElement('branch')
                branches.appendChild(branch)
                for item_name in self.branches:
                    content = self.dom.createElement(str(item_name))
                    branch.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["finance_date"]) > 1:
            finance_history = self.dom.createElement('finance_history')
            company.appendChild(finance_history)
            for i in range(1, len(item["finance_date"])):
                finance = self.dom.createElement('finance')
                finance_history.appendChild(finance)
                for item_name in self.finance_history:
                    content = self.dom.createElement(str(item_name))
                    finance.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["member_name"]) > 1:
            core_team = self.dom.createElement("core_team")
            company.appendChild(core_team)
            for i in range(1, len(item["member_name"])):
                member = self.dom.createElement('member')
                core_team.appendChild(member)
                for item_name in self.core_team:
                    content = self.dom.createElement(str(item_name))
                    member.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["business_name"]) > 1:
            enterprise_business = self.dom.createElement("enterprise_business")
            company.appendChild(enterprise_business)
            for i in range(1, len(item["business_name"])):
                business = self.dom.createElement("business")
                enterprise_business.appendChild(business)
                for item_name in self.enterprise_business:
                    content = self.dom.createElement(str(item_name))
                    business.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["invest_time"]) > 1:
            investment_event = self.dom.createElement("investment_event")
            company.appendChild(investment_event)
            for i in range(1, len(item["invest_time"])):
                invest = self.dom.createElement("invest")
                investment_event.appendChild(invest)
                for item_name in self.investment_event:
                    content = self.dom.createElement(str(item_name))
                    invest.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["announce_time"]) > 1:
            court_announcement = self.dom.createElement("court_announcement")
            company.appendChild(court_announcement)
            for i in range(1, len(item["announce_time"])):
                announce = self.dom.createElement("announce")
                court_announcement.appendChild(announce)
                for item_name in self.court_announcement:
                    content = self.dom.createElement(str(item_name))
                    announce.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["dis_company"]) > 1:
            print 'here'
            the_dishonest = self.dom.createElement("the_dishonest")
            company.appendChild(the_dishonest)
            for i in range(1, len(item["dis_company"])):
                dishonest = self.dom.createElement("dishonest")
                the_dishonest.appendChild(dishonest)
                for item_name in self.the_dishonest:
                    content = self.dom.createElement(str(item_name))
                    dishonest.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["filing_date"]) > 1:
            the_executed = self.dom.createElement("the_executed")
            company.appendChild(the_executed)
            for i in range(1, len(item["filing_date"])):
                executed = self.dom.createElement("executed")
                the_executed.appendChild(executed)
                for item_name in self.the_executed:
                    content = self.dom.createElement(str(item_name))
                    executed.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["include_date"]) > 1:
            abnormal_management = self.dom.createElement("abnormal_management")
            company.appendChild(abnormal_management)
            for i in range(1, len(item["include_date"])):
                abnormal = self.dom.createElement("abnormal")
                abnormal_management.appendChild(abnormal)
                for item_name in self.abnormal_management:
                    content = self.dom.createElement(str(item_name))
                    abnormal.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["pub_code"]) > 1:
            adminis_pubnish = self.dom.createElement("adminis_pubnish")
            company.appendChild(adminis_pubnish)
            for i in range(1, len(item["pub_code"])):
                pubnish = self.dom.createElement("pubnish")
                adminis_pubnish.appendChild(pubnish)
                for item_name in self.adminis_pubnish:
                    content = self.dom.createElement(str(item_name))
                    pubnish.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["set_time"]) > 1:
            seriously_illegal = self.dom.createElement("seriously_illegal")
            company.appendChild(seriously_illegal)
            for i in range(1, len(item["set_time"])):
                illegal = self.dom.createElement("illegal")
                seriously_illegal.appendChild(illegal)
                for item_name in self.seriously_illegal:
                    content = self.dom.createElement(str(item_name))
                    illegal.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["regist_date"]) > 1:
            equity_pledge = self.dom.createElement("equity_pledge")
            company.appendChild(equity_pledge)
            for i in range(1, len(item["regist_date"])):
                equity = self.dom.createElement("equity")
                equity_pledge.appendChild(equity)
                for item_name in self.equity_pledge:
                    content = self.dom.createElement(str(item_name))
                    equity.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        if len(item["registed_num"]) > 1:
            chattel_mortgage = self.dom.createElement("chattel_mortgage")
            company.appendChild(chattel_mortgage)
            for i in range(1, len(item["registed_num"])):
                mortgage = self.dom.createElement("mortgage")
                chattel_mortgage.appendChild(mortgage)
                for item_name in self.chattel_mortgage:
                    content = self.dom.createElement(str(item_name))
                    mortgage.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)
                mortgagee = self.dom.createElement("mortgagee")
                chattel_mortgage.appendChild(mortgagee)
                for i in range(1, len(item["mortgagee_name"])):
                    sub_mortgagee =self.dom.createElement("sub_mortgagee")
                    mortgage.appendChild(sub_mortgagee)
                    for item_name in self.sub_chattel_mortgage1:
                        content = self.dom.createElement(str(item_name))
                        sub_mortgagee.appendChild(content)
                        data = self.dom.createTextNode(str(item[item_name][i]))
                        content.appendChild(data)
                pawn = self.dom.createElement("pawn")
                chattel_mortgage.appendChild(pawn)
                for i in range(1, len(item["pawn_name"])):
                    sub_pawn = self.dom.createElement("sub_pawn")
                    pawn.appendChild(sub_pawn)
                    for item_name in self.sub_chattel_mortgage2:
                        content = self.dom.createElement(str(item_name))
                        sub_pawn.appendChild(content)
                        data = self.dom.createTextNode(str(item[item_name][i]))
                        content.appendChild(data)

        self.root.appendChild(company)
        return item

    def close_spider(self, spider):
        with open('..\\data.xml', 'w') as f:
            self.dom.writexml(f, addindent='  ', newl='\n', encoding='utf-8')
