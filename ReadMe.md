#TianYanCha_Spider
一个爬取[天眼查](http://www.tianyancha.com)的企业信息的爬虫，遍历机制是根据企业名称进行搜索，企业名称保存在`name_list.txt`中，来自[黄页88](http://www.huangye88.com/)，其爬虫代码见[Yellow_Page](https://github.com/Range0122/yellow_page)。
# Scrapy + Selenium + Phantomjs
由于目标网页中需要抓取的数据采用了JS渲染，通过普通的request无法抓到，所以使用了`selenium` + `phantomjs`
目前只是做了在搜索了企业名称之后对于展示了企业详细信息的网站的url的获取，后续将更新抓取详细信息的代码。