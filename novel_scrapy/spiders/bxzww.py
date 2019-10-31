# coding=utf-8
import time
from datetime import datetime

from scrapy import Spider, Request

from ..items import PirateSiteItem


class bxzww(Spider):
    name = "bxzww"
    start_urls = ['https://www.bxzww.com/']
    allow_domains = ['https://www.bxzww.com/']

    def parse(self, response):
        for article_index in range(1, 70368):
            # for article_index in range(1, 2):
            article_url = "http://www.bxzww.com/bxinfo/" + str(int(article_index / 1000)) + "/" + str(article_index) + ".htm"
            yield Request(url=article_url, callback=self.parseArticle, meta={
                'article_id': article_index,
                'article_url': article_url
            })

    def parseArticle(self, response):
        article_name = response.xpath('//*[@id="page"]/div[7]/div[1]/div[2]/div[2]/h1/text()').extract()[0]
        author = response.xpath('//*[@id="page"]/div[7]/div[1]/div[2]/div[2]/p/span[1]/a/text()').extract()[0]
        only_id = article_name + "-:-" + author
        lasted_name = response.xpath('//*[@id="dirsort01"]/li[1]/span/a/text()').extract()[0]
        lasted_time_str = response.xpath('//*[@id="page"]/div[7]/div[1]/div[2]/div[2]/p/span[3]/text()').extract()[0]
        lasted_datetime = datetime.strptime(lasted_time_str, "%Y-%m-%d")
        lasted_time = int(time.mktime(lasted_datetime.timetuple()))

        is_full_status = response.xpath('//*[@id="page"]/div[7]/div[1]/div[2]/div[2]/p/span[2]/text()').extract()[0]
        is_full = 0 if str.strip(is_full_status) == '连载中' else 1

        article_chapter_url = "http://www.bxzww.com/bx/" + str(int(response.meta['article_id'] / 1000)) + "/" + str(response.meta['article_id']) + "/"

        yield Request(url=article_chapter_url, callback=self.parseChapter, meta={
            'article_id': response.meta['article_id'],
            'article_url': response.meta['article_url'],
            'article_name': article_name,
            'author': author,
            'only_id': only_id,
            'lasted_time': lasted_time,
            'lasted_name': lasted_name,
            'is_full': is_full
        })

    def parseChapter(self, response):
        chapter_nodes = response.xpath('//div[@class="clearfix dirconone"]/ul/li').extract()
        chapter_size = len(chapter_nodes)

        item = PirateSiteItem()
        item['site_id'] = 10
        item['site_name'] = "bxzww"
        item['article_id'] = response.meta['article_id']
        item['article_name'] = response.meta['article_name']
        item['author'] = response.meta['author']
        item['only_id'] = response.meta['only_id']
        item['lasted_time'] = response.meta['lasted_time']
        item['lasted_name'] = response.meta['lasted_name']
        item['is_full'] = response.meta['is_full']
        item['is_vip'] = 0
        item['votes'] = 0
        item['article_url'] = response.meta['article_url']
        item['chapter_size'] = chapter_size

        # print(item)
        yield item
