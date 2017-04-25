# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import re
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import codecs
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

user_agent_list = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
]

ua = random.choice(user_agent_list)
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ua
dcap["phantomjs.page.settings.loadImages"] = False

with codecs.open('F:\\PycharmProjects\\tianyancha\\tianyancha\\test_list.txt', 'r', encoding='utf-8') as f:
    final_url_list = []
    for line in f.readlines():
        # try:
        print line
        driver = webdriver.PhantomJS(executable_path='E:\Webdriver\phantomjs-2.1.1-windows\\bin\phantomjs.exe',
                                     desired_capabilities=dcap)
        driver.get("http://www.tianyancha.com/")
        sleep_time = random.randint(8, 12)
        time.sleep(sleep_time)
        search_item = driver.find_element_by_tag_name('input')
        search_item.send_keys(line)
        search_item.send_keys(Keys.RETURN)
        time.sleep(sleep_time)
        url_list = re.findall('(http://www.tianyancha.com/company/[\d]*)', driver.page_source)
        if url_list:
            final_url_list += url_list
            print "Successed"
        else:
            print "EMPTY ", driver.current_url
        driver.quit()
    final_url_list = {}.fromkeys(final_url_list).keys()
    with codecs.open('empty_list.txt', 'a', encoding='utf-8') as f:
        for url in final_url_list:
            f.write(url+'\n')





