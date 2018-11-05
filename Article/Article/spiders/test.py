# -*- coding: utf-8 -*-
import logging

import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['http://httpbin.org/get']
    start_urls = ['http://httpbin.org/get']
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES" : {
            'Article.middlewares.RandomUserAgentMiddleware': 1,
            'Article.middlewares.ProxyIpMiddleware': 2,
        },
    }

    def parse(self, response):
        logging.info(response.text)
