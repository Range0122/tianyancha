# -*- coding:utf-8 -*-

import urllib2
import codecs
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

while True:
    print "CATCH"
    url = 'http://tvp.daxiangdaili.com/ip/?tid=556706495113104&num=100&category=2&delay=5&foreign=none'
    response = urllib2.urlopen(url)
    with codecs.open('F:\PycharmProjects\\tianyancha\ip_list.txt', 'w') as f:
        f.write(response.read())
    time.sleep(180)
