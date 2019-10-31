# coding=utf-8
import time
from datetime import datetime

from scrapy import Spider, Request


class xbiquge6(Spider):
    name = "xiangcunxiaoshuo"
    start_urls = ['https://m.xiangcunxiaoshuo.la/']
    allow_domains = ['https://m.xiangcunxiaoshuo.la/']

    def parse(self, response):
        for article_index in range(1, 629893):
            article_url = "https://m.xiangcunxiaoshuo.la/info-" + str(article_index) + "/"
            yield Request(url=article_url, callback=self.parseArticle, meta={
                'article_id': article_index,
                'article_url': article_url
            })

    def parseArticle(self, response):
        article_name = response.xpath("//meta[@property='og:novel:book_name']/@content").extract()[0]
        author = response.xpath("//meta[@property='og:novel:author']/@content").extract()[0]
        only_id = article_name + "-:-" + author

        lasted_name = response.xpath('//ul[@class="chapter"]/li[1]/a/text()').extract()[0]
        lasted_time_str = response.xpath('//meta[@property="og:novel:update_time"]/@content').extract()[0]
        lasted_datetime = datetime.strptime(lasted_time_str, "%Y-%m-%d %H:%M:%S")
        lasted_time = int(time.mktime(lasted_datetime.timetuple()))

        is_full_status = response.xpath('//meta[@property="og:novel:status"]/@content').extract()[0]
        is_full = 0 if is_full_status == '连载中' else 1
        is_vip = 0
        votes = 0

        print(only_id, lasted_name, lasted_time)
