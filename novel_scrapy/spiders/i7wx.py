# coding=utf-8
import re
import time
from datetime import datetime

from scrapy import Spider, Request

from ..items import PirateSiteItem


class i7wx(Spider):
    name = "i7wx"
    start_urls = ['https://m.i7wx.com']
    allow_domains = ['https://m.i7wx.com']

    def parse(self, response):
        for page_index in range(1, 500):
            yield Request(url='https://m.i7wx.com/list/1_2_' + str(page_index) + '.html', callback=self.parse_page)
        for page_index in range(1, 500):
            yield Request(url='https://m.i7wx.com/list/2_2_' + str(page_index) + '.html', callback=self.parse_page)
        for page_index in range(1, 500):
            yield Request(url='https://m.i7wx.com/list/3_2_' + str(page_index) + '.html', callback=self.parse_page)
        for page_index in range(1, 500):
            yield Request(url='https://m.i7wx.com/list/4_2_' + str(page_index) + '.html', callback=self.parse_page)
        for page_index in range(1, 451):
            yield Request(url='https://m.i7wx.com/list/5_2_' + str(page_index) + '.html', callback=self.parse_page)
        for page_index in range(1, 500):
            yield Request(url='https://m.i7wx.com/list/6_2_' + str(page_index) + '.html', callback=self.parse_page)
        for page_index in range(1, 500):
            yield Request(url='https://m.i7wx.com/list/7_2_' + str(page_index) + '.html', callback=self.parse_page)

    def parse_page(self, response):
        article_url_list = response.xpath('/html/body/div[4]/ul/li/a/@href').extract()
        for article_url_suffix in article_url_list:
            article_id = re.findall(r'\d+', article_url_suffix)[0]
            article_url = 'https://m.i7wx.com' + article_url_suffix
            yield Request(url=article_url, callback=self.parse_article, meta={
                'article_id': article_id,
                'article_url': article_url
            })

    def parse_article(self, response):
        article_name = response.xpath('/html/body/div[3]/strong/a/text()').extract()[0]
        author = response.xpath('//*[@id="bookinfo"]/div[2]/div[1]/text()').extract()[0]
        only_id = article_name + "-:-" + author

        lasted_time_str = response.xpath('//*[@id="bookinfo"]/div[2]/div[5]/text()').extract()[0]
        lasted_datetime = datetime.strptime(lasted_time_str, "%Y-%m-%dT%H:%M:%S")
        lasted_time = int(time.mktime(lasted_datetime.timetuple()))
        lasted_name = response.xpath('//*[@id="bookinfo"]/div[4]/a/text()').extract()[0]
        # 手机站采集不到是否完本

        is_full = 2
        is_vip = 0
        votes_str = response.xpath('//*[@id="bookinfo"]/div[2]/div[4]/text()').extract()[0]
        votes = re.findall(r'\d+', votes_str)[0]

        chapter_url = 'https://m.i7wx.com/' + str(int(int(response.meta['article_id']) / 1000)) + '/' + \
                      response.meta['article_id'] + '/'
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
        chapter_size_str = response.xpath('/html/body/div[5]/text()').extract()[0]
        chapter_size = re.findall(r'\d+', chapter_size_str)[0]

        item = PirateSiteItem()

        item['site_id'] = 4
        item['site_name'] = "i7wx"

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
