# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
import csv
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class HenanSpider(CrawlSpider):
    name = "henan"
    allowed_domains = ["www.hngp.gov.cn"]
    start_urls = ['http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0101']
    for i in range(1,5):
        start_urls.append("http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0101&bz=0&pageSize=10&pageNo="+str(i))
    
    rules = (
        Rule(SgmlLinkExtractor(allow=("/henan/content?"),restrict_xpaths=('//div[@class="List2"]',)), callback='parse_item', follow=True),
    )
    
    def parse_item(self, response):
	hxs = HtmlXPathSelector(response)
        sites = hxs.select('//h1[@class="TxtCenter Padding10 BorderEEEBottom Top5"]')
        times = hxs.select('//span[@class="Blue"]')
        time=[]
	for subTimes in times:
            time.append(subTimes.select('text()').extract())
            #print ("this time length",len(time),"this time type",type(time))
        date=time
        #print ("this date length",len(date),"this date type",type(date[2][0]),date[2][0])
	for site in sites:
            title = site.select('text()').extract()
            print ("this sites is",title[0].decode())
	if os.path.isdir('.\\henan') == False:
            os.makedirs('.\\henan')
	filename = ".\\henan"+"\\"+title[0].decode()+".html"#.encode("gbk") .split("\n")[1]
        #print title[0].split("\n")[1].encode('gbk')
	with open(filename, 'wb') as f:
            f.write(response.body)
	csvfile = codecs.open('henan-result.csv','a',"utf-8-sig")
	writer = csv.writer(csvfile)
	writer.writerow([title[0].decode().replace(","," "), date[2][0].decode(),response.url])#split("\n")[1].
	csvfile.close()
