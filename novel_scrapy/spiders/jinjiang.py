# coding=utf-8
import json
import re
import time
from datetime import datetime

import scrapy
from scrapy import Spider, Request
from scrapy.http.cookies import CookieJar

from ..items import AuthorizedSiteItem

# 实例化一个cookiejar对象
cookie_jar = CookieJar()


class qidian(Spider):
    name = "jinjiang"
    start_urls = ['http://www.jjwxc.net/onebook.php?novelid=4195296']
    allow_domains = ['http://www.jjwxc.net', 'http://app-cdn.jjwxc.net','http://app.robook.com']

    def parse(self, response):

        for page_index in range(1, 20001):
            list_page_url = 'http://www.jjwxc.net/bookbase_slave.php?booktype=&opt=&orderstr=3&endstr=&page=' + str(page_index)
            yield Request(url=list_page_url, callback=self.parseLastUpdatePage)

    def parseLastUpdatePage(self, response):
        article_list = response.xpath('//table[@class="cytable"]/tbody/tr/td[2]/a/@href').extract()
        for article_url_suffix in article_list:
            article_id = re.findall(r'\d+', article_url_suffix)[0]
            article_url = 'http://app-cdn.jjwxc.net/androidapi/novelbasicinfo?novelId=' + article_id
            yield Request(url=article_url, callback=self.parseArticleInfo)

    def parseArticleInfo(self,response):
        response_json = json.loads(response.body)



        article_id = response_json['novelId']
        article_url = 'http://www.jjwxc.net/onebook.php?novelid=' + article_id
        article_name = response_json['novelName']
        author = response_json['authorName']
        only_id = article_name + "-:-" + author

        is_vip = 1 if response_json['isVip'] == '0' else 2
        is_full = response_json['isVip']

        lasted_time_str = response_json['renewDate']
        lasted_datetime = datetime.strptime(lasted_time_str, "%Y-%m-%d %H:%M:%S")
        lasted_time = int(time.mktime(lasted_datetime.timetuple()))
        lasted_name = response_json['renewChapterName']
        chapter_size = response_json['maxChapterId']

        votes = response_json['nutrition_novel']
        months_vote = response_json['nutrition_novel']
        money_man = response_json['novelbefavoritedcount']

        yield scrapy.FormRequest(url='http://app.robook.com/androidapi/getnovelOtherInfo',method='POST', formdata={
            'novelId': article_id,
            'versionCode': '108'
        },callback=self.parse_talks,meta={
            'article_id': article_id,
            'article_name': article_name,
            'author': author,
            'article_url': article_url,
            'only_id': only_id,
            'lasted_time': lasted_time,
            'lasted_name': lasted_name,
            'is_full': is_full,
            'is_vip': is_vip,
            'votes': votes,
            'months_vote': months_vote,
            'money_man': money_man,
            'chapter_size': chapter_size
        })


    def parse_talks(self,response):
        response_json = json.loads(response.body)
        talks = response_json['comment_count']

        item = AuthorizedSiteItem()

        item['site_id'] = 7
        item['site_name'] = "jinjiang"

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
        item['chapter_size'] = response.meta['chapter_size']

        item['months_vote'] = response.meta['months_vote']
        item['money_man'] = response.meta['money_man']
        item['talks'] = talks

        yield item


