# coding=utf-8
import re
import time
from datetime import datetime

from scrapy import Spider, Request

from ..items import PirateSiteItem


class du00(Spider):
    name = "du00"
    start_urls = ['https://m.du00.com']
    allow_domains = ['https://m.du00.com', 'https://www.du00.com']

    def parse(self, response):
        for page_index in range(1, 166641):
            article_id = str(page_index)
            article_url = 'https://m.du00.com/book/' + str(page_index) + '.html'
            yield Request(url=article_url, callback=self.parse_article, meta={
                        'article_id': article_id,
                        'article_url': article_url
                    })
    #        yield Request(url='https://m.du00.com/top-postdate-' + str(page_index) + '/', callback=self.parse_page)

    # def parse_page(self, response):
    #     article_url_list = response.xpath('//p[@class="line"]/a[2]/@href').extract()
    #     for article_url_suffix in article_url_list:
    #         article_id = re.findall(r'\d+', article_url_suffix)[0]
    #         article_url = 'https://m.du00.com' + article_url_suffix
    #         #print(article_id, article_url)
    #         print(article_url)
    #         yield Request(url=article_url, callback=self.parse_article, meta={
    #             'article_id': article_id,
    #             'article_url': article_url
    #         })

    def parse_article(self, response):

        if response.xpath('/html/head/title/text()').extract()[0] != '出现错误！':
            article_name = response.xpath('//div[@class="block_txt2"]/p/a/h2/text()').extract()[0]
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

            chapter_url = 'https://m.du00.com/xs/' + response.meta['article_id'] + '/1/'
            #chapter_url = 'https://www.du00.com/read/' + str(int(int(response.meta['article_id']) / 1000)) +'/' + response.meta['article_id'] + '/index.html'

            yield Request(url=chapter_url, callback=self.parse_chapter_page_size, meta={
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

    def parse_chapter_page_size(self,response):
        chapter_page_size_str = response.xpath('//div[@class="page"][2]/text()[3]').extract()[0]
        chapter_page_size = re.findall(r'\d+', chapter_page_size_str)[1]
        last_chapter_list_url = 'https://m.du00.com/xs/' + response.meta['article_id'] + '/' + str(chapter_page_size) + '/'

        yield Request(url=last_chapter_list_url,callback=self.parse_last_chapter_size,meta={
            'article_id': response.meta['article_id'],
            'article_url': response.meta['article_url'],
            'article_name': response.meta['article_name'],
            'author': response.meta['author'],
            'only_id': response.meta['only_id'],
            'lasted_time': response.meta['lasted_time'],
            'lasted_name': response.meta['lasted_name'],
            'is_full': response.meta['is_full'],
            'is_vip': response.meta['is_vip'],
            'votes': response.meta['votes'],
            'total_chapter_page_size': chapter_page_size
        })


    def parse_last_chapter_size(self,response):
        last_chapter_size = len(response.xpath('//ul[@class="chapter"]/li'))
        chapter_size = (int(response.meta['total_chapter_page_size']) -1 ) * 20 + int(last_chapter_size)

        item = PirateSiteItem()

        item['site_id'] = 6
        item['site_name'] = "du00"

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
