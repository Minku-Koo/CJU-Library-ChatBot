# -*- coding: utf-8 -*-

import scrapy

import sys

from scrapy.spiders import Spider

from scrapy.selector import HtmlXPathSelector

from companycrawler.items import CompanycrawlerItem

from scrapy.http import Request

from scrapy.selector import Selector
reload(sys)
sys.setdefaultencoding('utf-8')
 

class companycrawler_Spider(scrapy.Spider):
    name = "companycrawler"  #spider 이름
    allowed_domains = ["http://www.jobkorea.co.kr/"]  #최상위 도메인
 
    #1번만 실행
    def start_requests(self):
        for i in range(1,5,1):
            yield scrapy.Request("http://www.jobkorea.co.kr/starter/?schPart=10016&Page={0}".format(i),self.parse)
 
    #아이템 parse
    def parse(self, response):
        for colum in  response.xpath('//div[@class="filterListArea"]/ul/li') :
            item = CompanycrawlerItem() 
            item['company'] = colum.xpath('div/div[@class="coTit"]/a/text()').extract_first() #주택명 추출
            item['context'] =colum.xpath('div/div[@class="tit"]//a/span/text()').extract_first()
            yield item