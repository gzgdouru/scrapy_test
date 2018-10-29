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

from repository.models import ZhihuQuestion, ZhihuAnswer


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


def replace_permil(value, flag=''):
    return str(value).replace(',', flag)


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
    zhihu_id = scrapy.Field(output_processor=TakeFirst())
    topics = scrapy.Field(output_processor=Join(","))
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    content = scrapy.Field(output_processor=TakeFirst())
    # create_time = scrapy.Field()
    # update_time = scrapy.Field()
    answer_num = scrapy.Field(output_processor=TakeFirst())
    comments_num = scrapy.Field(input_processor=MapCompose(get_nums), output_processor=TakeFirst())
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field(output_processor=TakeFirst())
    crawl_update_time = scrapy.Field(output_processor=TakeFirst())

    def save_for_mysql(self):
        answer_num = int(replace_permil(self["answer_num"]))
        comments_num = int(replace_permil(self["comments_num"]))
        watch_user_num = int(replace_permil(self["watch_user_num"][0]))
        click_num = int(replace_permil(self["click_num"][1]))

        if ZhihuQuestion.objects.filter(zhihu_id=int(self["zhihu_id"])).exists():
            ZhihuQuestion.objects.filter(zhihu_id=int(self["zhihu_id"])).update(
                content=self.content,
                answer_num=answer_num,
                comments_num=comments_num,
                watch_user_num=watch_user_num,
                click_num=click_num,
                crawl_update_time=self.crawl_update_time
            )
        else:
            zhihu_quesion_obj = ZhihuQuestion()
            zhihu_quesion_obj.zhihu_id = int(self["zhihu_id"])
            zhihu_quesion_obj.topics = self["topics"]
            zhihu_quesion_obj.url = self["url"]
            zhihu_quesion_obj.title = self["title"]
            zhihu_quesion_obj.content = self["content"]
            zhihu_quesion_obj.answer_num = answer_num
            zhihu_quesion_obj.comments_num = comments_num
            zhihu_quesion_obj.watch_user_num = watch_user_num
            zhihu_quesion_obj.click_num = click_num
            zhihu_quesion_obj.crawl_time = self["crawl_time"]
            zhihu_quesion_obj.crawl_update_time = self["crawl_update_time"]
            zhihu_quesion_obj.save()


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

    def save_for_mysql(self):
        if ZhihuAnswer.objects.filter(zhihu_id=int(self["zhihu_id"])).exists():
            ZhihuAnswer.objects.filter(zhihu_id=int(self["zhihu_id"])).update(
                content = self["content"],
                praise_num=self["praise_num"],
                comments_num=self["comments_num"],
                update_time=datetime.fromtimestamp(self["update_time"]),
                crawl_update_time=self["crawl_update_time"]
            )
        else:
            zhihu_answer_obj = ZhihuAnswer()
            zhihu_answer_obj.zhihu_id = int(self["zhihu_id"])
            zhihu_answer_obj.url = self["url"]
            zhihu_answer_obj.question = ZhihuQuestion.objects.get(pk=self["question"])
            zhihu_answer_obj.author_id = self["author_id"]
            zhihu_answer_obj.content = self["content"]
            zhihu_answer_obj.praise_num = self["praise_num"]
            zhihu_answer_obj.comments_num = self["comments_num"]
            zhihu_answer_obj.create_time = datetime.fromtimestamp(self["create_time"])
            zhihu_answer_obj.update_time = datetime.fromtimestamp(self["update_time"])
            zhihu_answer_obj.crawl_time = self["crawl_time"]
            zhihu_answer_obj.crawl_update_time = self["crawl_update_time"]
            zhihu_answer_obj.save()