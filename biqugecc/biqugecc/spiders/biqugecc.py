# coding=utf-8
from scrapy import Spider, Request, Selector
from datetime import datetime
import time
import re

from ..items import BiqugeccItem


class biqugecc(Spider):
    name = "biqugecc"
    start_urls = ['https://www.biquge.cc']
    allow_domains = ['https://www.biquge.cc']

    def parse(self, response):
        for article_index in range(1, 526501):
            article_url = "https://www.biquge.cc/html/1/" + str(article_index) + "/"
            yield Request(url=article_url, callback=self.parseArticle, meta={
                'article_id': article_index,
                'article_url': article_url
            })

    def parseArticle(self, response):

        article_name = response.xpath("//div[@id='info']/h1/text()").extract()[0].encode('utf-8')
        author = response.xpath('//*[@id="info"]/p[1]/text()').extract()[0].encode('utf-8').split('：', 1)[1]
        only_id = article_name + "-:-" + author
        lasted_name = response.xpath('//*[@id="info"]/p[4]/a/text()').extract()[0]
        lasted_time_str = response.xpath('//*[@id="info"]/p[3]/text()').extract()[0].encode('utf-8').split('：', 1)[1]
        try:
            lasted_datetime = datetime.strptime(lasted_time_str, "%m/%d/%Y %I:%M:%S %p")
        except ValueError:
            lasted_datetime = datetime.strptime(lasted_time_str, "%Y/%m/%d %H:%M:%S")
        lasted_time = int(time.mktime(lasted_datetime.timetuple()))

        is_full_status = response.xpath('//meta[@property="og:novel:status"]/@content').extract()[0]
        is_full = 1 if is_full_status.encode('utf-8') == '连载' else 2
        is_vip = 0
        votes = 0
        chapter_nodes = response.xpath('//*[@id="list"]/dl/dd').extract()
        chapter_size = len(chapter_nodes)
        if chapter_size > 12:
            chapter_size = chapter_size - 12
        article_url = response.meta['article_url']
        article_id = response.meta['article_id']

        item = BiqugeccItem()
        item['site_id'] = 2
        item['site_name'] = "biqugecc"

        item['article_id'] = article_id
        item['article_name'] = article_name
        item['author'] = author
        item['only_id'] = only_id
        item['lasted_time'] = lasted_time
        item['lasted_name'] = lasted_name
        item['is_full'] = is_full
        item['is_vip'] = is_vip
        item['votes'] = votes
        item['article_url'] = article_url
        item['chapter_size'] = chapter_size

        yield item

