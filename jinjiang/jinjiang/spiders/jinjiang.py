# coding=utf-8
from scrapy import Spider, Request, Selector
from datetime import datetime
import time
import re


class jinjiang(Spider):

    name = "jinjiang"
    start_urls = ['http://www.jjwxc.net']
    allow_domains = ['http://www.jjwxc.net/']

    def parse(self, response):

