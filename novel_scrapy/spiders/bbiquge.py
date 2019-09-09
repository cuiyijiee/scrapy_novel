# coding=utf-8
import time
from datetime import datetime

from scrapy import Spider, Request

from ..items import PirateSiteItem


class biqugecc(Spider):
    name = "bbiquge"
    start_urls = ['https://www.bbiquge.com']
    allow_domains = ['https://www.bbiquge.com']

    def parse(self, response):
        for article_index in range(1, 126748):
            article_url = "https://www.bbiquge.com/book_" + str(article_index) + "/"
            yield Request(url=article_url, callback=self.parseArticle, meta={
                'article_id': article_index,
                'article_url': article_url
            })

    def parseArticle(self, response):
        article_name = response.xpath('//meta[@property="og:novel:book_name"]/@content').extract()[0]
        author = response.xpath('//meta[@property="og:novel:author"]/@content').extract()[0]
        only_id = article_name + "-:-" + author
        lasted_name = response.xpath('//meta[@property="og:novel:latest_chapter_name"]/@content').extract()[0]
        lasted_time_str = response.xpath('//meta[@property="og:novel:update_time"]/@content').extract()[0]
        lasted_datetime = datetime.strptime(lasted_time_str, "%Y-%m-%d %H:%M:%S")
        lasted_time = int(time.mktime(lasted_datetime.timetuple()))

        is_full_status = response.xpath('//meta[@property="og:novel:status"]/@content').extract()[0]
        is_full = 0 if is_full_status == '连载' else 1
        is_vip = 0
        votes = 0

        chapter_nodes = response.xpath('//*[@id="list"]/dl/dd').extract()
        chapter_size = len(chapter_nodes)

        article_url = response.meta['article_url']
        article_id = response.meta['article_id']

        item = PirateSiteItem()
        item['site_id'] = 8
        item['site_name'] = "bbiquge"

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
