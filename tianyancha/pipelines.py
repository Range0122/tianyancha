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
    #     self.item_zh_names = [
    #         u'企业名称', u'法定代表人', u'注册资本', u'注册时间', u'状态', u'工商注册号', u'组织机构代码', u'统一信用代码',
    #         u'企业类型', u'行业', u'营业期限', u'核准日期', u'登记机关', u'注册地址', u'经营范围', u'电话', u'邮箱',
    #         u'网址']
        self.item_en_names = ['company_name', 'company_id', 'legal_representative', 'registered_capital', 'registered_time', 'condition',
                              'registered_number', 'organization_number', 'credit_number', 'enterprise_type', 'industry',
                              'operating_period', 'approved_date', 'registration_authority', 'registered_address',
                              'business_scope', 'telephone', 'email', 'website', 'logo_location', 'address', 'score']

    def process_item(self, item, spider):
        page = self.dom.createElement('company')
        self.root.appendChild(page)

        for i in range(0, len(self.item_en_names)):
            content = self.dom.createElement(str(self.item_en_names[i]))
            data = self.dom.createTextNode(str(item[self.item_en_names[i]][0]))
            content.appendChild(data)
            page.appendChild(content)

        return item

    def close_spider(self, spider):
        with open('..\\data.xml', 'w') as f:
            self.dom.writexml(f, addindent='  ', newl='\n', encoding='utf-8')
