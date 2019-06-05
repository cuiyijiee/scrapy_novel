# coding=utf-8
from scrapy import Spider, Request, Selector
from datetime import datetime
import time
import re
from ..items import QidianItem
from scrapy.http.cookies import CookieJar
import json

# 实例化一个cookiejar对象
cookie_jar = CookieJar()

class qidian(Spider):
    name = "qidian"
    start_urls = ['https://m.qidian.com/majax/free/getFreeLeftTime?gender=male']
    allow_domains = ['https://m.qidian.com/']

    def parse(self, response):

        cookie = response.headers.getlist('Set-Cookie')[0]
        token = bytes.decode(cookie).split(";")[0].split("=")[1]

        for male_page_index in range(1, 31):
            list_page_url = 'https://m.qidian.com/majax/rank/updatelist?gender=male&catId=-1&pageNum=' + str(male_page_index) + '&_csrfToken=' + token
            yield Request(url=list_page_url, callback=self.parseLastUpdatePage, meta={
                "token":token
            })

        for female_page_index in range(1, 21):
            list_page_url = 'https://m.qidian.com/majax/rank/updatelist?gender=female&catId=-1&pageNum=' + str(female_page_index) + '&_csrfToken=' + token
            yield Request(url=list_page_url, callback=self.parseLastUpdatePage, meta={
                "token":token
            })

    def parseLastUpdatePage(self, response):
        response_json = json.loads(response.body)
        for article in response_json['data']['records']:
            article_id = article['bid']
            article_name = article['bName']
            author = article['bAuth']

            only_id = article_name + "-:-" + author

            is_full_status = article['state']
            is_full = 1 if is_full_status == '连载中' else 2
            article_info_url = 'https://m.qidian.com/book/' + str(article_id)

            yield Request(url= article_info_url, callback=self.parseArticleInfo, meta={
                'article_id': article_id,
                'article_name': article_name,
                'author': author,
                'only_id': only_id,
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

        lasted_name = response.xpath('//*[@id="ariaMuLu"]/text()').extract()[1].replace('连载至','')

        is_vip_group = response.xpath('//*[@id="bookDetailWrapper"]/div/div[2]/ul/li').extract()
        is_vip = 1 if len(is_vip_group) == 3 else 2

        votes = response.xpath('//*[@id="payTicketsX"]/li[1]/a/p/span[1]/text()').extract()[0]
        months_vote = int(response.xpath('//*[@id="payTicketsX"]/li[2]/a/p/span[1]/text()').extract()[0])
        money_man = int(response.xpath('//*[@id="payTicketsX"]/li[3]/a/p/span/text()').extract()[0])

        # TODO 评论数需要登录
        #talks = response.xpath('//*[@id="ariaFriNum"]/output/text()').extract()[0]
        talks = 0

        yield Request(url='https://m.qidian.com/book/' + str(response.meta['article_id']) + '/catalog', callback=self.parseChapterSize, meta={
            'article_id': response.meta['article_id'],
            'article_name': response.meta['article_name'],
            'author': response.meta['author'],
            'article_url': response.meta['article_url'],
            'only_id': response.meta['only_id'],
            'lasted_time': lasted_time,
            'lasted_name': lasted_name,
            'is_full':response.meta['is_full'],
            'is_vip': is_vip,
            'votes': votes,
            'months_vote': months_vote,
            'money_man': money_man,
            'talks':talks
        })

    def parseChapterSize(self,response):
        #chapter_list = response.xpath('//*[@id="volumes"]/li').extract()
        #chapter_size = len(chapter_list)
        chapter_size = response.xpath('//*[@id="catelogX"]/div/div[1]/h4/output/text()').extract()[0]

        item = QidianItem()

        item['site_id'] = 3
        item['site_name'] = "qidian"

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

        item['months_vote'] = response.meta['months_vote']
        item['money_man'] = response.meta['money_man']
        item['talks'] = response.meta['talks']

        yield item





