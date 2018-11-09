# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
import logging

from scrapy import signals
from fake_useragent import UserAgent
from scrapy.http import HtmlResponse

from Article.utils.mysqlV1 import MysqlManager


class ArticleSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CustomSpiderMiddleware(object):
    def __init__(self):
        super(CustomSpiderMiddleware, self).__init__()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_spider_input(self, response, spider):
        raise RuntimeError("测试异常")

    def process_spider_exception(self, response, exception, spider):
        logger = logging.getLogger(__name__)
        logger.info("{0} error: {1}".format(spider.name, exception))


class RandomUserAgentMiddleware(object):
    def __init__(self, ua_type):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = ua_type

    @classmethod
    def from_crawler(cls, crawler):
        ua_type = crawler.settings.get("USER_AGNET_TYPE", "random")
        return cls(ua_type)

    def process_request(self, request, spider):
        if hasattr(self.ua, self.ua_type):
            user_agent = getattr(self.ua, self.ua_type)
        else:
            user_agent = self.ua.random
        request.headers.setdefault("User-Agent", user_agent)


class ProxyIpMiddleware(object):
    def __init__(self):
        super(ProxyIpMiddleware, self).__init__()
        self.mysqldb = MysqlManager(host="193.112.150.18", user="ouru", passwd="5201314Ouru...", db="novel")

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        proxy = self.get_proxy()
        request.meta["proxy"] = proxy

    def get_proxy(self):
        record = list(self.mysqldb.execute("select * from proxys order by rand() limit 1"))[0]
        proxy = "http://{0}:{1}".format(record.ip, record.port)
        return proxy


class DynamicPageMiddleware(object):
    def __init__(self):
        super(DynamicPageMiddleware, self).__init__()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        spider.browser.get(request.url)
        time.sleep(2)
        text = spider.browser.page_source
        return HtmlResponse(url=request.url, body=text, request=request, encoding="utf-8")


class ArticleDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
