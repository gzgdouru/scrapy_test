# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Join
from scrapy.loader import ItemLoader
from datetime import datetime


class JobboleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def date_convert(value):
    try:
        create_date = datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.now().date()
    return create_date

def get_nums(value):
    match_re = re.match(r".*?(\d+).*", value)
    nums = match_re.group(1) if match_re else 0
    return nums


def remove_comment(value):
    if "评论" in value:
        return ""
    else:
        return value


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(input_processor=MapCompose(date_convert))
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(output_processor=Identity())
    front_image_path = scrapy.Field()

    praise_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    fav_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    comment_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    content = scrapy.Field()
    tags = scrapy.Field(input_processor=MapCompose(remove_comment), output_processor=Join(","))


class ZhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    # create_time = scrapy.Field()
    # update_time = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()


class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()
