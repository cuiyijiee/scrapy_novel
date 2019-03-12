# coding=utf-8
from scrapy import Spider, Request, Selector
from datetime import datetime
import time
import re
from zhuishubang.items import ZhuishubangItem


class spider(Spider):
    name = "zhuishubang"
    start_urls = ['https://www.zhuishubang.com/']
    allow_domains = ['https://www.zhuishubang.com/']

    def parse(self, response):
        for page_index in range(1, 2000):
            last_update_page_url = 'https://www.zhuishubang.com/all/0_lastupdate_0_0_0_0_0_0_' + str(
                page_index) + '.html'
            yield Request(url=last_update_page_url, callback=self.parseLastUpdatePage)

    def parseLastUpdatePage(self, response):
        article_list = response.xpath('//div[@class="listRightBottom"]/ul/li').extract()

        for article in article_list:
            article_selector = Selector(text=article)
            lasted_name = article_selector.xpath('//p[@class="newChapter"]/a/text()').extract()[0]
            is_full_status = article_selector.xpath('//span[@class="state"]/text()').extract()[0]
            is_full = 1 if is_full_status.encode('utf-8') == '连载中' else 2
            # 网页上解析到的上次更新时间
            lasted_time_str = '20' + article_selector.xpath('//span[@class="state"]/text()').extract()[1].split(':', 1)[
                1]
            # 将字符串转换为datetime格式
            lasted_datetime = datetime.strptime(lasted_time_str, '%Y-%m-%d %H:%M')
            # 转换为timestamp，单位是秒
            lasted_time = int(time.mktime(lasted_datetime.timetuple()))
            article_info_url = article_selector.xpath('//h2/a/@href').extract()[0]
            yield Request(url=article_info_url, callback=self.parseArticleInfo, meta={
                'lasted_name': lasted_name,
                'lasted_time': lasted_time,
                'article_url': article_info_url,
                'is_full': is_full
            })

    def parseArticleInfo(self, response):

        article_name = response.xpath('//meta[@property="og:novel:book_name"]/@content').extract()[0]
        author = response.xpath('//meta[@property="og:novel:author"]/@content').extract()[0]
        only_id = article_name + "-:-" + author
        lasted_name = response.meta['lasted_name']
        lasted_time = response.meta['lasted_time']
        is_full = response.meta['is_full']
        article_url = response.meta['article_url']
        article_id = re.findall(r'\d+\.?\d*', article_url)[0]
        is_vip = 0
        votes = 0
        # 先找到所有的节点
        chapter_nodes = response.xpath('//div[@class="chapterCon"]/ul/li').extract()
        # 通过len方法得到所有节点的个数
        chapter_size = len(chapter_nodes)

        item = ZhuishubangItem()
        item['site_id'] = 1
        item['site_name'] = "zhuishubang"

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
