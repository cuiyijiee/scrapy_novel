# coding=utf-8
from scrapy import Spider, Request, Selector
from datetime import datetime
import time
import re
from ..items import QidianItem
from scrapy.http.cookies import CookieJar

# 实例化一个cookiejar对象
cookie_jar = CookieJar()


class qidian(Spider):
    name = "qidian"
    start_urls = ['https://www.qidian.com/all?orderId=&page=1&update=4&style=1&pageSize=20&siteid=1&pubflag=0'
                  '&hiddenField=0']
    allow_domains = ['https://www.qidian.com/']

    def parse(self, response):
        total_update_page = response.xpath('//*[@id="page-container"]/div/ul/li[8]/a/text()').extract()[0]
        for page_index in range(1, int(total_update_page) + 1):
            list_page_url = "https://www.qidian.com/all?orderId=&update=4&style=1&pageSize=20&siteid=1&pubflag=0" \
                            "&hiddenField=0&page=" + str(page_index)
            yield Request(url=list_page_url, callback=self.parseLastUpdatePage)

    def parseLastUpdatePage(self, response):

        article_list = response.xpath('/html/body/div[1]/div[5]/div[2]/div[2]/div/ul/li').extract()
        for article in article_list:
            article_selector = Selector(text=article)

            article_id = article_selector.xpath('//div[@class="book-img-box"]/a/@data-bid').extract()[0]
            article_name = article_selector.xpath('//div[@class="book-mid-info"]/h4/a/text()').extract()[0]
            author = article_selector.xpath('//div[@class="book-mid-info"]/p[1]/a[1]/text()').extract()[0]

            is_full_status = article_selector.xpath('//div[@class="book-mid-info"]/p[1]/span/text()').extract()[0]
            # is_full = 1 if is_full_status.encode('utf-8') == '连载中' else 2
            is_full = 1 if is_full_status == '连载中' else 2
            article_info_url = 'https:' + article_selector.xpath('//div[@class="book-img-box"]/a/@href').extract()[0]

            yield Request(url='https://m.qidian.com/book/' + article_id, callback=self.parseArticleInfo, meta={
                'article_id': article_id,
                'article_name': article_name,
                'author': author,
                'article_url': article_info_url,
                'is_full': is_full
            })

    def parseArticleInfo(self, response):
        lasted_time_str = response.xpath('//*[@id="ariaMuLu"]/text()').extract()[0]
        now_time = int(time.time())
        if lasted_time_str.find('前') >= 0 | lasted_time_str.find('刚刚'):
            lasted_time = now_time - now_time % 86400 + time.timezone
        elif lasted_time_str.find('昨日') >= 0:
            lasted_time = now_time - now_time % 172800 + time.timezone
        else:
            lasted_datetime = datetime.strptime(lasted_time_str, '%Y-%m-%d')
            lasted_time = int(time.mktime(lasted_datetime.timetuple()))

        is_vip_group = response.xpath('//*[@id="bookDetailWrapper"]/div/div[2]/ul/li').extract()
        is_vip = 1 if len(is_vip_group) == 3 else 2

        votes = response.xpath('//*[@id="payTicketsX"]/li[1]/a/p/span[1]/text()').extract()[0]
        months_vote = response.xpath('//*[@id="payTicketsX"]/li[2]/a/p/span[1]/text()').extract()[0]
        money_man = response.xpath('//*[@id="payTicketsX"]/li[3]/a/p/span/text()').extract()[0]
        # TODO 评论数需要解析出 _csrfToken cookie，待做
        talks = response.xpath('//*[@id="ariaFriNum"]/output/text()').extract()[0]




