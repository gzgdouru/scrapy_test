# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from urllib import parse
import re

import scrapy
from scrapy.loader.processors import TakeFirst, Identity, MapCompose

from repository.models import NovelCategory, Author, Novel


def parse_novel_category(value):
    match_obj = re.match(r'.*<a.*?>(\w+)</a>.*', value, re.DOTALL)
    if match_obj:
        return match_obj.group(1)
    else:
        return ""


def parse_novel_author(value):
    match_obj = re.match(r'^作\s*者：(.*)', value)
    if match_obj:
        return match_obj.group(1)
    else:
        return ""


class NovelCollectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NovelInfoItem(scrapy.Item):
    novel_name = scrapy.Field(output_processor=TakeFirst())
    site_name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    image = scrapy.Field()
    intro = scrapy.Field(output_processor=TakeFirst())
    parser = scrapy.Field(output_processor=TakeFirst())
    author = scrapy.Field(input_processor=MapCompose(parse_novel_author), output_processor=TakeFirst())
    category = scrapy.Field(input_processor=MapCompose(parse_novel_category), output_processor=TakeFirst())

    def save_for_mysql(self):
        if not Novel.objects.filter(novel_name=self["novel_name"]).exists():
            novel = Novel()
            novel.novel_name = self["novel_name"]
            novel.site_name = self["site_name"]
            novel.url = self["url"]

            category = NovelCategory.objects.filter(name=self["category"]).first()
            if not category:
                category = NovelCategory()
                category.name = self["category"]
                category.save()
            novel.category = category

            novel.image = self["image"][0]

            author = Author.objects.filter(name=self["author"])
            if not author:
                author = Author()
                author.name = self["author"]
                author.intro = self["author"]
                author.save()
            novel.author = author

            novel.intro = self["intro"]
            novel.parser = self["parser"]
            novel.save()
