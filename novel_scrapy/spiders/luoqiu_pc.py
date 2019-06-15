# coding=utf-8
import re
import time
from datetime import datetime

from scrapy import Spider, Request

from ..items import PirateSiteItem


class luoqiu_pc(Spider):
    name = "luoqiu_pc"
    start_urls = ['https://www.luoqiu.com']
    allow_domains = ['https://www.luoqiu.com']

    def parse(self, response):
        for page_index in range(1, 500):
            yield Request(url='https://www.luoqiu.com/top/lastupdate_' + str(page_index) + '.html',
                          callback=self.parse_page)

    def parse_page(self, response):
        article_url_list = response.xpath('//div[@class="body"]/table/tbody/tr/td[2]/a/@href').extract()
        for article_url in article_url_list:
            article_id = re.findall(r'\d+', article_url)[0]
            yield Request(url=article_url, callback=self.parse_article, meta={
                'article_id': article_id,
                'article_url': article_url
            })

    def parse_article(self, response):

        article_name = response.xpath('//meta[@property="og:novel:book_name"]/@content').extract()[0]
        author = response.xpath('//meta[@property="og:novel:author"]/@content').extract()[0]
        only_id = article_name + "-:-" + author

        # 如果出现问题使用下面这个，精确度到日
        # lasted_time_str = response.xpath('//meta[@property="og:novel:update_time"]/@content').extract()[0]
        # lasted_datetime = datetime.strptime(lasted_time_str, "%Y-%m-%d")
        lasted_time_str = response.xpath('//td[@width="27%"]/text()').extract()[0]
        lasted_datetime = datetime.strptime(lasted_time_str, "%Y-%m-%d %H:%M:%S")

        lasted_time = int(time.mktime(lasted_datetime.timetuple()))
        lasted_name = response.xpath('//meta[@property="og:novel:latest_chapter_name"]/@content').extract()[0]

        is_full = 1 if response.xpath('//meta[@property="og:novel:status"]/@content').extract()[0].find(
            '连载') >= 0 else 2
        is_vip = 0
        votes = 0

        chapter_url = 'https://www.luoqiu.com/read/' + response.meta['article_id'] + '/'

        yield Request(url=chapter_url, callback=self.parse_chapter, meta={
            'article_id': response.meta['article_id'],
            'article_url': response.meta['article_url'],
            'article_name': article_name,
            'author': author,
            'only_id': only_id,
            'lasted_time': lasted_time,
            'lasted_name': lasted_name,
            'is_full': is_full,
            'is_vip': is_vip,
            'votes': votes
        })

    def parse_chapter(self, response):
        chapter_size = len(response.xpath('//*[@id="defaulthtml4"]/table/tbody/tr')) * 4

        item = PirateSiteItem()

        item['site_id'] = 5
        item['site_name'] = "luoqiu"

        item['article_id'] = response.meta['article_id']
        item['article_name'] = response.meta['article_name']
        item['author'] = response.meta['author']
        item['only_id'] = response.meta['only_id']
        item['lasted_time'] = response.meta['lasted_time']
        item['lasted_name'] = response.meta['lasted_name']
        item['is_full'] = response.meta['is_full']
        item['is_vip'] = response.meta['is_vip']
        item['votes'] = response.meta['votes']
        item['article_url'] = response.meta['article_url']
        item['chapter_size'] = chapter_size

        yield item
