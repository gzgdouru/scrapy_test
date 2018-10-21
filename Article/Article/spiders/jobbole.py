# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re
from datetime import datetime

from scrapy.loader import ItemLoader

from Article.items import JobboleArticleItem, JobboleItemLoader
from Article.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['http://blog.jobbole.com/']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        #提取当前页的所有文章链接
        postNodes = response.css("#archive .post-thumb a")
        for postNode in postNodes:
            frontImage = postNode.css("img::attr(src)").extract_first("")
            frontImage = parse.urljoin(response.url, frontImage)
            postUrl = postNode.css("::attr(href)").extract_first("")
            #返回给scrapy下载
            yield Request(url=parse.urljoin(response.url, postUrl), meta={"front_image_url":frontImage}, callback=self.parse_detail, dont_filter=True)

        #提取下一页的url
        nextUrl = response.css(".next.page-numbers::attr(href)").extract_first()
        if nextUrl:
            #返回给scrapy下载
            yield Request(url=parse.urljoin(response.url, nextUrl), callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        '''提取文章的具体内容'''
        # front_image_url = response.meta.get("front_image_url", "")
        # title = response.css(".entry-header h1::text").extract_first()
        # create_date = response.css(".entry-meta-hide-on-mobile::text").extract_first().replace("·", "").strip()
        # praise_nums = response.css(".post-adds .vote-post-up h10::text").extract_first()
        #
        # fav_nums = response.css(".post-adds .bookmark-btn::text").extract_first()
        # match_re = re.match(r".*?(\d+).*", fav_nums)
        # fav_nums = match_re.group(1) if match_re else 0
        #
        # comment_nums = response.css(".post-adds a[href='#article-comment'] span::text").extract_first()
        # match_re = re.match(r".*?(\d+).*", comment_nums)
        # comment_nums = match_re.group(1) if match_re else 0
        #
        # content = response.css(".entry").extract_first()
        #
        # tags = response.css(".entry-meta .entry-meta-hide-on-mobile a::text").extract()
        # tags = ",".join(tags)
        #
        #
        # jobbleItem = JobboleArticleItem()
        # jobbleItem["title"] = title
        # try:
        #     create_date = datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.now().date()
        # jobbleItem["create_date"] = create_date
        # jobbleItem["url"] = response.url
        # jobbleItem["url_object_id"] = get_md5(response.url)
        # jobbleItem["front_image_url"] = [front_image_url]
        # jobbleItem["praise_nums"] = praise_nums
        # jobbleItem["fav_nums"] = fav_nums
        # jobbleItem["comment_nums"] = comment_nums
        # jobbleItem["content"] = content
        # jobbleItem["tags"] = tags

        #通过item_loader加载item
        front_image_url = response.meta.get("front_image_url", "")
        item_loader = JobboleItemLoader(item=JobboleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_css("create_date", ".entry-meta-hide-on-mobile::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".post-adds .vote-post-up h10::text")
        item_loader.add_css("fav_nums", ".post-adds .bookmark-btn::text")
        item_loader.add_css("comment_nums", ".post-adds a[href='#article-comment'] span::text")
        item_loader.add_css("content", ".entry")
        item_loader.add_css("tags", ".entry-meta .entry-meta-hide-on-mobile a::text")
        articleItem = item_loader.load_item()

        yield articleItem