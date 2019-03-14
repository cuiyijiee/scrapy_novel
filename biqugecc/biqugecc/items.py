# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BiqugeccItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    site_id = scrapy.Field()
    site_name = scrapy.Field()

    article_id = scrapy.Field()
    article_name = scrapy.Field()
    author = scrapy.Field()

    only_id = scrapy.Field()  # 书名-:-作者

    lasted_time = scrapy.Field()
    lasted_name = scrapy.Field()
    is_full = scrapy.Field()
    is_vip = scrapy.Field()
    votes = scrapy.Field()
    article_url = scrapy.Field()
    chapter_size = scrapy.Field()
    pass
