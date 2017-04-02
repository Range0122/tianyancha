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
        self.business_product = ['product_name', 'product_type', 'product_intro', 'product_logo']

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

        if len(item["product_name"]) > 1:
            business_product = self.dom.createElement("business_product")
            company.appendChild(business_product)
            for i in range(1, len(item["product_name"])):
                product = self.dom.createElement("product")
                business_product.appendChild(product)
                for item_name in self.business_product:
                    content = self.dom.createElement(str(item_name))
                    product.appendChild(content)
                    data = self.dom.createTextNode(str(item[item_name][i]))
                    content.appendChild(data)

        self.root.appendChild(company)
        return item

    def close_spider(self, spider):
        with open('..\\data.xml', 'w') as f:
            self.dom.writexml(f, addindent='  ', newl='\n', encoding='utf-8')
