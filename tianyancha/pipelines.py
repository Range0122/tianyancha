# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import traceback
class TianyanchaPipeline(object):
    # def date_insert(self, item, db_name, selfcol):
    #     memory = []
    #     value = ',%s'
    #     for i in xrange(len(selfcol)):
    #         memory.append(item[selfcol[i]])
    #     value_number = len(memory)
    #     while (value_number > 0):
    #         value += value
    #         value_number = value_number - 1
    #     for i in xrange(0, len(memory[0])):
    #         try:
    #             self.cursor.execute("INSERT INTO " + db_name + " "
    #                                                            "VALUES(NULL," + item["company_id"]+value + ")",
    #                                 tuple(str(x[i]) for x in memory))
    #         except Exception,e:
    #             print (tuple(str(x[i]) for x in memory) + "insert not success")
    #             pass

    def __init__(self):
        self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="Kbase", port=3306,
                                    charset="utf8")
        self.cursor = self.conn.cursor()

        self.company = ['company_id',
                        'company_name',
                        'legal_representative',
                        'registered_number',
                        'organization_number',
                        'credit_number',
                        'enterprise_type',
                        'industry',
                        'registered_capital',
                        'registered_time',
                        'registered_address',
                        'business_scope',
                        'operating_start',
                        'operating_end',
                        'condition',
                        'approved_date',
                        'registration_authority',
                        'telephone',
                        'website',
                        'email',
                        'address',
                        'logo_location',
                        'score',
                        'former_name']
        self.person = ['person_id',
                       'person_name']
        self.main_person = ['person_id',
                            'position']
        self.shareholder_info = [
            'investment_proportion',
            'subscribed_contribution',
            'subscribed_contribution_time',
            'really_contribution']
        self.investment = [
            'invested_company_id',
            'investment_amount',
            'investment_prop',
            'invested_company_name',
            'invested_representative',
            'registered_cap',
            'registered_date',
            'condit']
        self.change_record = ['change_time',
                              'change_item',
                              'before_change',
                              'after_change']
        self.annual_reports = ['annual_year',
                               'annual_url']
        self.detailed_report = ['total_assets',
                                'total_sales',
                                'mainbusiness_income',
                                'total_tax',
                                'total_ownersequity',
                                'total_profit',
                                'retained_profits',
                                'total_liabilities']
        self.amendment = ['amend_date',
                          'amend_event',
                          'before_amend',
                          'after_amend', ]
        self.branches = ['branch_id',
                         'branch_name',
                         'branch_legalrep',
                         'branch_cond',
                         'branch_regtime']
        self.finance_history = [
            'finance_date',
            'finance_round',
            'valuation',
            'finance_amount',
            'investor',
            'finance_proportion',
            'news_url',]
        self.core_team = ['member_icon',
                          'member_name',
                          'member_pos',
                          'member_intro']
        self.enterprise_business = ['business_name',
                                    'business_type',
                                    'business_intro',
                                    'business_logo']
        self.investment_event = ['invest_time',
                                 'invest_round',
                                 'invest_amount',
                                 'invest_company',
                                 'invest_product',
                                 'invest_pro_icon',
                                 'invest_area',
                                 'invest_industry',
                                 'invest_business']
        self.competing_product = ['product_name',
                                  'product_logo',
                                  'product_area',
                                  'product_round',
                                  'product_industry',
                                  'product_business',
                                  'setup_date',
                                  'product_valuation']
        # 法律诉讼表  item->
        self.law_suit = [
            'lawsuit_date',
            'judgement_id ',
            'case_type']

        # 裁判文书表   item->
        self.judgement = [
            'relative_comp',
            'judgement_title',
            'case_num',
            'judgement_name',
            'judgement_content']

        self.court_announcement = ['announce_time',
                                   'appeal',
                                   'respondent',
                                   'announce_type',
                                   'court',
                                   'announce_content']
        self.the_dishonest = ['execute_number',
                              'case_number',
                              'execute_unite',
                              'legal_obligation',
                              'performance',
                              'execute_court',
                              'province',
                              'filing_time',
                              'pub_time']
        self.the_executed = ['filing_date',
                             'executed_target',
                             'case_code',
                             'executed_court']
        self.adminis_pubnish = ['pub_date',
                                'pub_code',
                                'pub_type',
                                'pub_authority',
                                'pub_content',
                                ]
        self.seriously_illegal = ['set_time',
                                  'set_reason',
                                  'set_department']
        self.equity_pledge = ['regist_date',
                              'regist_num',
                              'pledgor',
                              'pledgee',
                              'regist_cond',
                              'regist_date',
                              'pledged_amount',
                              'pledged_code',
                              'pledgee_code',
                              'pledge_remark']
        self.chattel_mortgage = ['registed_num',
                                 'registed_depart',
                                 'registed_date',
                                 'mortgagee_info',
                                 'registed_cond',
                                 'vouched_type',
                                 'vouched_amount',
                                 'debt_start',
                                 'debt_end',
                                 'vouched_range',
                                 'pawn_remark',
                                 'pawn_info']
        self.owe_tax = ['tax_date',
                        'tax_num',
                        'tax_type',
                        'tax_current',
                        'tax_balance',
                        'tax_depart']
        self.bidding = [
            'bid_time',
            'rfp_id',
            'bid_purchaser']
        self.RFP = [
            'bid_title',
            'bid_time',
            'bid_related',
            'bid_content'
        ]

        self.bond_information = ['bond_name',
                                 'bond_publisher',
                                 'bond_start',
                                 'bond_start',
                                 'bond_duration',
                                 'interest_mode',
                                 'credit_agency',
                                 'face_value',
                                 'coupon_rate',
                                 'planned_circulation',
                                 'spread',
                                 'bond_date',
                                 'exercise_date',
                                 'circulation_scope',
                                 'bond_code',
                                 'bond_type',
                                 'bond_end',
                                 'trading_day',
                                 'bond_delisting',
                                 'bond_rating',
                                 'reference_rate',
                                 'actual_circulation',
                                 'issue_price',
                                 'frequency',
                                 'exercise_type',
                                 'trustee',
                                 ]
        self.purchase_island = ['admini_region',
                                'pruchase_trustee',
                                'signed_date',
                                'parcel_location',
                                'purchase_assignee',
                                'land_use',
                                'min_volume',
                                'trasaction_price',
                                'start_time',
                                'supervision_num',
                                'total_area',
                                'superior_company',
                                'supply_mode',
                                'max_volume',
                                'end_time',
                                ]
        self.the_employ = ['start_date',
                           'employ_position',
                           'wage',
                           'experience',
                           'employ_num',
                           'employ_city',
                           'employ_area',
                           'source',
                           'start_date',
                           'end_date',
                           'education',
                           'position_desc']
        self.rating_tax = ['rating_year',
                           'rating_level',
                           'rating_type',
                           'rating_num',
                           'rating_office']
        self.random_check = ['check_date',
                             'check_type',
                             'check_result',
                             'check_office']
        self.product_info = ['product_icon',
                             'product_title',
                             'product_short',
                             'product_type',
                             'product_field',
                             'product_desc']
        self.quality_cert = ['device_name',
                             'cert_type',
                             'cert_start',
                             'cert_end',
                             'device_num',
                             'permit_num']
        self.brand_info = ['brand_date',
                           'brand_icon',
                           'brand_name',
                           'brand_num',
                           'brand_type',
                           'brand_cond']
        self.abnormal_operation = ['include_date',
                                   'include_reason ',
                                   'include_authority',
                                   'remove_date',
                                   'remove_reason',
                                   'remove_authority']
        self.patent_info = ['publish_date',
                            'patent_pic',
                            'patent_id',
                            'app_num',
                            'category_num',
                            'patent_name',
                            'patent_address',
                            'inventor',
                            'applicant',
                            'apply_date',
                            'agency',
                            'agent',
                            'abstracts']
        self.copyright_info = ['reg_time',
                               'full_name',
                               'simple_name',
                               'cat_num',
                               'reg_num',
                               'version',
                               'reg_time'
                               'author_nationality',
                               'first_publish',
                               ]
        self.website_filing = ['record_date',
                               'web_name',
                               'web_url',
                               'record_num',
                               'web_status',
                               'unit_nature']

    def process_item(self, item, spider):
        memory = []
        """ company"""
        memory = []
        for i in xrange(len(self.company)):
            memory.append(item[self.company[i]])
        try:
            self.cursor.execute(
                "INSERT INTO company VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
                tuple(memory))
        except Exception,e:
            print traceback.print_exc()
            try:
                self.cursor.execute(
                "UPDATE company SET tyqycid='%s',comp_name='%s',legalperson='%s',regist_No='%s',organization_code='%s',credit_code='%s',"
                "comp_type='%s',industry='%s',regist_captial='%s',regist_time='%s',regist_addr='%s',scope='%s',business_start='%s',business_end='%s',"
                " status='%s',approval_date='%s',reigst_authority='%s',comp_tel='%s',comp_net='%s',comp_email='%s',comp_addr='%s',logo='%s',score='%s',"
                "comp_usedname='%s' where tyqycid="+item["company_id"],
                tuple(memory)
            )
            except Exception,e:
                print traceback.print_exc()
            # self.date_insert(item,"company",self.company)
        self.conn.commit()
        self.cursor.execute("SELECT companyid FROM company WHERE tyqycid='%s'" % item["company_id"])
        item["company_id"] = str(int(self.cursor.fetchone()[0]))

        """ person"""
        memory = []
        person_fk = []
        for i in xrange(len(self.person)):
            memory.append(item[self.person[i]])
        if len(memory[0])>0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute(
                    "INSERT INTO person "
                    "VALUES(NULL,%s,%s)",
                    tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
            finally:
                self.conn.commit()
                self.cursor.execute("SELECT personid From person where tychmid='%s'" % memory[0][i])
                person_fk.append(str(int(self.cursor.fetchone()[0])))

        # self.date_insert(item,"comp_person_rel",self.main_person)


        """ comp_person_rel"""
        memory = []
        item['person_id'] = person_fk
        for i in xrange(len(self.main_person)):
            memory.append(item[self.main_person[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute(
                    "INSERT INTO comp_person_rel "
                    "VALUES(NULL," + item["company_id"] + ","
                                                          "%s,%s)",
                    tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        self.conn.commit()
        # self.date_insert(item,"comp_person_rel",self.main_person)

        # """ shareInfo"""
        # memory = []
        # for i in xrange(len(self.shareholder_info)):
        #     memory.append(item[self.shareholder_info[i]])
        # for (x,y,i) in zip(item["shareholder_name"],item["shareholder_id"],xrange(len(memory[0]))):
        #     if len(x)>4 and y.find(u'公司'):
        #             selec_result=self.cursor.execute("SELECT companyid FROM company WHERE tyqycid='%s'" % y)
        #             if selec_result==0:
        #                 self.cursor.execute("INSERT INTO company(tyqycid,comp_name) VALUES (%s,%s)", (y,x))
        #                 self.conn.commit()
        #                 self.cursor.execute("SELECT companyid FROM company WHERE tyqycid='%s'" % y)
        #             share_company_fk=int(self.cursor.fetchone()[0])
        #             self.cursor.execute("INSERT INTO shareinfo VALUES (NULL,NULL,"+share_company_fk+','
        #                                 "%s,%s,%s,%s)",tuple(str(x[i]) for x in memory))
        #     else:
        #         selec_result = self.cursor.execute("SELECT personid FROM person WHERE tychmid='%s'" % y)
        #         if selec_result == 0:
        #             self.cursor.execute("INSERT INTO person(tychmid,person_name) VALUES (%s,%s)", (y, x))
        #             self.conn.commit()
        #             self.cursor.execute("SELECT personid FROM person WHERE tychmid='%s'" % y)
        #         share_person_fk = int(self.cursor.fetchone()[0])
        #         self.cursor.execute("INSERT INTO shareinfo VALUES (NULL," + share_person_fk + ",NULL,"
        #                             "%s,%s,%s,%s)",
        #                             tuple(str(x[i]) for x in memory))
        #     self.conn.commit()
        """ shareInfo"""
        memory = []
        for i in xrange(len(self.shareholder_info)):
            memory.append(item[self.shareholder_info[i]])
        share_list=[]
        if len(memory[0]) > 0:
          for (x, y, i) in zip(item["shareholder_name"], item["shareholder_id"], xrange(len(memory[0]))):
           try:
            if len(x) > 4 and y.find(u'公司'):
                selec_result = self.cursor.execute("SELECT companyid FROM company WHERE tyqycid='%s'" % y)

                if selec_result == 0:
                    self.cursor.execute("INSERT INTO company(tyqycid,comp_name) VALUES (%s,%s)", (y, x))
                    share_company_fk = int(self.cursor.lastrowid)
                else:
                    share_company_fk = int(self.cursor.fetchone()[0])
                self.cursor.execute("INSERT INTO share_info VALUES (NULL,NULL," + str(share_company_fk) + ','
                                                                                                    "%s,%s,%s,%s)",
                                    tuple(str(x[i]) for x in memory))
            else:
                selec_result = self.cursor.execute("SELECT personid FROM person WHERE tychmid='%s'" % y)
                if selec_result == 0:
                    self.cursor.execute("INSERT INTO person(tychmid,person_name) VALUES (%s,%s)", (y, x))
                    share_person_fk = int(self.cursor.lastrowid)
                else:
                    share_person_fk = int(self.cursor.fetchone()[0])
                self.cursor.execute("INSERT INTO share_info VALUES (NULL," + str(share_person_fk) + ",NULL,"
                                                                                              "%s,%s,%s,%s)",
                                   tuple(str(x[i]) for x in memory))
           except Exception,e:
              print tuple(str(x[i]) for x in memory)
              print traceback.print_exc()
        self.conn.commit()
        # for i in xrange(len(self.shareholder_info)):
        #     memory.append(item[self.shareholder_info[i]])
        # for i in xrange(0, len(memory[0])):
        #     self.cursor.execute( "INSERT INTO  "
        #                          "VALUES(NULL,%s,%s,%s,%s,%s,%s)",
        #                 tuple(str(x[i]) for x in memory))


        """ report"""
        memory = []
        for i in xrange(len(self.annual_reports)):
            memory.append(item[self.annual_reports[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
             self.cursor.execute("INSERT INTO report "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "report", self.annual_reports)

        """ Financing"""
        memory = []
        for i in xrange(len(self.finance_history)):
            memory.append(item[self.finance_history[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
             self.cursor.execute("INSERT INTO financing "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "financing", self.finance_history)

        """investmentinfo"""
        invested_fk = []
        for i in xrange(len(self.investment)):
            memory.append(item[self.investment[i]])
        if len(memory[0]) > 0:
         for (x, y) in zip(item["invested_company_name"], item["invested_company_id"]):
            selec_result = self.cursor.execute("SELECT companyid FROM company WHERE tyqycid='%s'" % y)
            try:
             if selec_result == 0:
                self.cursor.execute("INSERT INTO company(tyqycid,comp_name) VALUES (%s,%s)", (y, x))
                invested_fk.append(str(int(self.cursor.lastrowid)))
             else:
                invested_fk.append(str(int(self.cursor.fetchone()[0])))
            except Exception,e:
                print traceback.print_exc()
         self.conn.commit()
         item["invested_company_id"] = invested_fk
         memory = []

         for i in xrange(0, len(memory[0])):
            try:
             self.cursor.execute("INSERT INTO investment_info "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
             print traceback.print_exc()
         # self.date_insert(item, "investment", self.investment)

        """change_record"""
        memory = []
        for i in xrange(len(self.change_record)):
            memory.append(item[self.change_record[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
             self.cursor.execute("INSERT INTO change_record "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "change_record", self.change_record)

        """coreteam"""
        memory = []
        for i in xrange(len(self.core_team)):
            memory.append(item[self.core_team[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO core_team "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "core_team", self.core_team)

        """businessInfo"""
        memory = []
        for i in xrange(len(self.enterprise_business)):
            memory.append(item[self.enterprise_business[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO business_info "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "business_info", self.enterprise_business)

        """invest_event"""
        memory = []
        for i in xrange(len(self.investment_event)):
            memory.append(item[self.investment_event[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO investment_event "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "investment_event", self.investment_event)

        """competing_product"""
        memory = []
        for i in xrange(len(self.competing_product)):
            memory.append(item[self.competing_product[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO competing_product "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "competing_product", self.competing_product)

        """judgement"""
        memory = []
        judge_fk = []
        for i in xrange(len(self.judgement)):
            memory.append(item[self.judgement[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO judgement "
                                "VALUES(NULL,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
                judge_fk.append(str(int(self.cursor.lastrowid)))
            except Exception,e:
                print tuple(str(x[i]) for x in memory)
                print traceback.print_exc()
        # self.date_insert(item, "judgement", self.)
        self.conn.commit()

        """lawsuit"""
        item["judgement_id"] = []
        item["judgement_id"]=judge_fk
        memory = []
        for i in xrange(len(self.law_suit)):
            memory.append(item[self.law_suit[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO law_suit "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "lawsuit", self.)


        """court_announcement"""
        memory = []
        for i in xrange(len(self.court_announcement)):
            memory.append(item[self.court_announcement[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO court_announcement "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "court_announcement", self.court_announcement)

        """executed_people"""
        memory = []
        for i in xrange(len(self.the_executed)):
            memory.append(item[self.the_executed[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO executed_people "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "executed_people", self.the_executed)

        """administrative_penalty"""
        memory = []
        for i in xrange(len(self.adminis_pubnish)):
            memory.append(item[self.adminis_pubnish[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO administrative_penalty "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "administrative_penalty", self.adminis_pubnish)

        """equity_pledged"""
        memory = []
        item["pledge_remark"]=[]
        for i in xrange(len(item["regist_num"])):
            item["pledge_remark"].append('所报材料真实合法，一切责任由当事人自负')
        for i in xrange(len(self.equity_pledge)):
            memory.append(item[self.equity_pledge[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO equity_pledged "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "equity_pledged", self.equity_pledge)

        """RFP"""
        memory = []
        rfp_fk = []
        for i in xrange(len(self.RFP)):
            memory.append(item[self.RFP[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO RFP "
                                "VALUES(NULL,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
                rfp_fk.append(str(int(self.cursor.lastrowid)))
            except Exception,e:
                print traceback.print_exc()
        self.conn.commit()
        # self.date_insert(item, "RFP", self.)

        """tendering"""
        memory = []
        item["rfp_id"] = rfp_fk
        for i in xrange(len(self.bidding)):
            memory.append(item[self.bidding[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO tendering "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "tendering", self.)

        """recruitment"""
        memory = []
        for i in xrange(len(self.the_employ)):
            memory.append(item[self.the_employ[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO recruitment "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "recruitment", self.the_employ)

        """tax_level"""
        memory = []
        for i in xrange(len(self.rating_tax)):
            memory.append(item[self.rating_tastr(x[i])])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO tax_level "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "tax_level", self.rating_tax)

        """random_check"""
        memory = []
        for i in xrange(len(self.random_check)):
            memory.append(item[self.random_check[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO random_check "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "random_check", self.random_check)

        """product_info"""
        memory = []
        for i in xrange(len(self.product_info)):
            memory.append(item[self.product_info[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO product_info "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "product_info", self.product_info)

        """tradmark_infomation"""
        memory = []
        for i in xrange(len(self.brand_info)):
            memory.append(item[self.brand_info[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO tradmark_infomation "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "tradmark_infomation", self.brand_info)

        """patent"""
        memory = []
        for i in xrange(len(self.patent_info)):
            memory.append(item[self.patent_info[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO patent "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "patent", self.patent_info)

        """copyright"""
        memory = []
        for i in xrange(len(self.copyright_info)):
            memory.append(item[self.copyright_info[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO copyright "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "copyright", self.copyright_info)

        """website_record"""
        memory = []
        for i in xrange(len(self.website_filing)):
            memory.append(item[self.website_filing[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO website_record "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "website_record", self.website_filing)

        """qualification"""
        memory = []
        for i in xrange(len(self.quality_cert)):
            memory.append(item[self.quality_cert[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO qualification "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "qualification", self.quality_cert)

        """bond_info"""
        memory = []
        for i in xrange(len(self.bond_information)):
            memory.append(item[self.bond_information[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO bond_info "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "bond_info", self.bond_information)

        """land_purchase"""
        memory = []
        for i in xrange(len(self.purchase_island)):
            memory.append(item[self.purchase_island[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO land_purchase "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
            # self.date_insert(item, "land_purchase", self.purchase_island)

        """tax_announcement"""
        memory = []
        for i in xrange(len(self.owe_tax)):
            memory.append(item[self.owe_tastr(x[i])])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO tax_announcement "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
            # self.date_insert(item, "tax_announcement", self.owe_tax)

        """chattel_mortgage"""
        memory = []
        item["pawn_remark"] = []
        for i in xrange(len(item["registed_num"])):
            item["pawn_remark"].append('--备注都是一样的有什么好备注的个备注个备注啊')
        for i in xrange(len(self.chattel_mortgage)):
            memory.append(item[self.chattel_mortgage[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO detailed_report "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
         # self.date_insert(item, "detailed_report", self.)

        """serious_offense"""
        memory = []
        for i in xrange(len(self.seriously_illegal)):
            memory.append(item[self.seriously_illegal[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO serious_offense "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "serious_offense", self.seriously_illegal)

        """经营异常"""
        memory = []
        for i in xrange(len(self.abnormal_operation)):
            memory.append(item[self.abnormal_operation[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO abnormal_operation"
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "", self.)

        """dishonest_people"""
        memory = []
        for i in xrange(len(self.the_dishonest)):
            memory.append(item[self.the_dishonest[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO dishonest_people "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "dishonest_people", self.the_dishonest)

        """branch"""
        memory = []
        for i in xrange(len(self.branches)):
            memory.append(item[self.branches[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO branch "
                                "VALUES(NULL," + item["company_id"] + ","
                                                                      "%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "branch", self.branches)

        """detailed_report"""
        memory = []
        for i in xrange(len(self.detailed_report)):
            memory.append(item[self.detailed_report[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO detailed_report "
                                "VALUES(NULL," + item["company_id"] + ','
                                                                      "%s,%s,%s,%s,%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
        # self.date_insert(item, "detailed_report", self.detailed_report)

        """amendment"""
        memory = []
        for i in xrange(len(self.amendment)):
            memory.append(item[self.amendment[i]])
        if len(memory[0]) > 0:
         for i in xrange(0, len(memory[0])):
            try:
                self.cursor.execute("INSERT INTO amendment "
                                "VALUES(NULL," + item["company_id"] + ','
                                                                      "%s,%s,%s,%s)",
                                tuple(str(x[i]) for x in memory))
            except Exception,e:
                print traceback.print_exc()
            # self.date_insert(item, "amendment", self.)

        self.conn.commit()
        return item

    def spider_closed(self, spider):
        # with open('..\\data.xml', 'a') as f:
        #     self.dom.writexml(f, addindent='  ', newl='\n', encoding='utf-8')
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
