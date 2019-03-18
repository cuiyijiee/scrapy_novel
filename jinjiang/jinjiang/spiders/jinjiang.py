# coding=utf-8
from scrapy import Spider, Request, Selector
from datetime import datetime
import time
import re


class jinjiang(Spider):
    name = "jinjiang"
    start_urls = ['http://app-cdn.jjwxc.net']
    allow_domains = ['http://app-cdn.jjwxc.net/']

    def parse(self, response):
        for aricle_id in range(1, 5000000,5):
            article_url = 'http://app-cdn.jjwxc.net/androidapi/novelbasicinfo?novelId=' + str(aricle_id)
            yield Request(url=article_url,callback= self.parseArticle,meta={
                'article_id': aricle_id
            })


    def parseArticle(self,response):
        print(response.body)
