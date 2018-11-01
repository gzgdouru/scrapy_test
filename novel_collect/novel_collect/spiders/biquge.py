# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from scrapy.loader import ItemLoader

from novel_collect.items import NovelInfoItem


class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    allowed_domains = ['https://www.cangqionglongqi.com/quanzhifashi/']
    start_urls = ['https://www.cangqionglongqi.com/quanzhifashi/']

    def parse(self, response):
        item_loader = ItemLoader(item=NovelInfoItem(), response=response)
        item_loader.add_css("novel_name", "#info h1::text")
        item_loader.add_css("site_name", ".header_logo a::text")
        item_loader.add_value("url", response.url)
        item_loader.add_css("image", "#fmimg img::attr(src)")
        item_loader.add_css("intro", "#intro")
        item_loader.add_value("parser", "biquge")
        item_loader.add_xpath("author", "//div[@id='info']/p[1]/text()")
        item_loader.add_css("category", ".con_top script::text")
        novelinfo_item = item_loader.load_item()
        yield novelinfo_item

        # urls = response.css("#list dd a::attr(href)").extract()
        # urls = [parse.urljoin(response.url, url) for url in urls]
        # for url in urls:
        #     yield scrapy.Request(url=url, dont_filter=True, callback=self.parse_chapter)

    def parse_chapter(self, response):
        site_name = response.xpath("//div[@id='box_con']/div[@class='con_top']/a[1]/text()").extract()
        novel_name = response.xpath("//*[@id='box_con']/div[1]/a[2]/text()").extract()
        title = response.css(".bookname h1::text").extract()
        content = response.css("#content")
        print(site_name, novel_name, title)

