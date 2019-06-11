# coding=utf-8
import re
import time
from datetime import datetime

from scrapy import Spider, Request

from ..items import PirateSiteItem


class luoqiu(Spider):
    name = "luoqiu"
    start_urls = ['http://m.luoqiu.com']
    allow_domains = ['http://m.luoqiu.com']

    def parse(self, response):
        for page_index in range(1, 2000):
            yield Request(url='http://m.luoqiu.com/top-lastupdate-' + str(page_index) + '/', callback=self.parse_page)

    def parse_page(self, response):
        article_url_list = response.xpath('//div[@class="cover"]/p/a[2]/@href').extract()
        for article_url_suffix in article_url_list:
            article_id = re.findall(r'\d+', article_url_suffix)[0]
            article_url = 'http://m.luoqiu.com' + article_url_suffix
            yield Request(url=article_url, callback=self.parse_article, meta={
                'article_id': article_id,
                'article_url': article_url
            })

    def parse_article(self, response):

        article_name = response.xpath('//div[@class="block_txt2"]/p[1]/a/h2/text()').extract()[0]
        author = response.xpath('//div[@class="block_txt2"]/p[2]/text()').extract()[0].split('：')[1]
        only_id = article_name + "-:-" + author

        lasted_time_str = response.xpath('//div[@class="block_txt2"]/p[5]/text()').extract()[0].split('：')[1].strip()
        try:
            lasted_datetime = datetime.strptime(lasted_time_str, "%Y-%m-%d")
        except ValueError:
            lasted_datetime = datetime.strptime(lasted_time_str, "%Y/%m/%d")
        lasted_time = int(time.mktime(lasted_datetime.timetuple()))
        lasted_name = response.xpath('//div[@class="block_txt2"]/p[6]/a/text()').extract()[0]

        is_full = 1 if response.xpath('//div[@class="block_txt2"]/p[4]/text()').extract()[0].find('连载') >= 0 else 2
        is_vip = 0
        votes = 0

        chapter_url = 'http://m.luoqiu.com/wapbook-' + response.meta['article_id'] + '/'

        yield Request(url=chapter_url,callback=self.parse_chapter,meta={
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

    def parse_chapter(self,response):
        chapter_size = len(response.xpath('//ul[@class="chapter"]/li'))

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
