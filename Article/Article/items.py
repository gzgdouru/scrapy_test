# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from datetime import datetime, timedelta
import re
from w3lib.html import remove_tags

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Join
from scrapy.loader import ItemLoader

from repository.models import ZhihuQuestion, ZhihuAnswer, LagouJob


class JobboleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class CustomTakeFirst(TakeFirst):
    def __call__(self, *args, **kwargs):
        value = super(CustomTakeFirst, self).__call__(*args, **kwargs)
        return value if value else ""


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


def get_min_salary(value):
    match_obj = re.match(r'^(\d+)k.*', value)
    if match_obj:
        return int(match_obj.group(1)) * 1000
    return 0


def get_max_salary(value):
    match_obj = re.match(r'.*?-(\d+)k.*', value)
    if match_obj:
        return int(match_obj.group(1)) * 1000
    return 0


def format_str(value):
    value = str(value).replace("/", "")
    return value.strip()


def get_min_work_years(value):
    if -1 != str(value).find("-"):
        match_obj = re.match(r"经验(\d+)-.*", value)
        if match_obj:
            return int(match_obj.group(1))
    else:
        match_obj = re.match(r'.*?(\d+).*', value)
        if match_obj:
            return int(match_obj.group(1))
    return 0


def get_max_work_years(value):
    if -1 != str(value).find("-"):
        match_obj = re.match(r".*?-(\d+).*", value)
        if match_obj:
            return int(match_obj.group(1))
    return 0


def format_job_addr(value):
    value_list = value.split("\n")
    return "".join([value.strip() for value in value_list if value.strip() != "查看地图"])


def get_publish_time(value):
    if -1 != value.find("-"):
        #yyyy-mm-dd HH:MM:SS
        match_obj = re.match(r'(\d+)-(\d+)-(\d+)\s+(\d+):(\d+):(\d+).*', value)
        if match_obj:
            publish_time = datetime(year=int(match_obj.group(1)), month=int(match_obj.group(2)), day=int(match_obj.group(3)),
                                    hour=int(match_obj.group(4)), minute=int(match_obj.group(5)), second=int(match_obj.group(6)))
            return publish_time
    else:
        if -1 != value.find(":"):
            #xx:xx
            match_obj = re.match(r'(\d+):(\d+).*', value)
            if match_obj:
                now = datetime.now()
                publish_time = datetime(year=now.year, month=now.month, day=now.day,
                                        hour=int(match_obj.group(1)), minute=int(match_obj.group(2)), second=now.second)
                return publish_time
        else:
            #xx天前
            match_obj = re.match(r'(\d+)天前.*', value)
            if match_obj:
                return datetime.now() - timedelta(days=int(match_obj.group(1)))
    return datetime.now()


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
                content=self["content"],
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


class LagouItem(scrapy.Item):
    obj_id = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    salary_min = scrapy.Field(input_processor=MapCompose(get_min_salary), output_processor=TakeFirst())
    salary_max = scrapy.Field(input_processor=MapCompose(get_max_salary), output_processor=TakeFirst())
    job_city = scrapy.Field(input_processor=MapCompose(format_str), output_processor=TakeFirst())
    work_years_min = scrapy.Field(input_processor=MapCompose(get_min_work_years), output_processor=TakeFirst())
    work_years_max = scrapy.Field(input_processor=MapCompose(get_max_work_years), output_processor=TakeFirst())
    degree_need = scrapy.Field(input_processor=MapCompose(format_str), output_processor=TakeFirst())
    job_type = scrapy.Field(output_processor=TakeFirst())
    publish_time = scrapy.Field(input_processor=MapCompose(get_publish_time), output_processor=TakeFirst())
    tags = scrapy.Field(output_processor=Join(","))
    job_advantage = scrapy.Field(output_processor=TakeFirst())
    job_desc = scrapy.Field(output_processor=TakeFirst())
    job_addr = scrapy.Field(input_processor=MapCompose(remove_tags, format_job_addr), output_processor=TakeFirst())
    company_url = scrapy.Field(output_processor=TakeFirst())
    company_name = scrapy.Field(output_processor=TakeFirst())

    def save_for_mysql(self):
        if LagouJob.objects.filter(obj_id=self["obj_id"]).exists():
            LagouJob.objects.filter(obj_id=self["obj_id"]).update(
                salary_min=self["salary_min"],
                salary_max=self["salary_max"],
                work_years_min=self["work_years_min"],
                work_years_max=self["work_years_max"],
                degree_need=self["degree_need"],
                publish_time=self["publish_time"],
                job_desc=self["job_desc"],
                job_addr=self["job_addr"],
                company_url=self["company_url"]
            )
        else:
            lagou_obj = LagouJob()
            lagou_obj.obj_id = self["obj_id"]
            lagou_obj.url = self["url"]
            lagou_obj.title = self["title"]
            lagou_obj.salary_min = self["salary_min"]
            lagou_obj.salary_max = self["salary_max"]
            lagou_obj.job_city = self["job_city"]
            lagou_obj.work_years_min = self["work_years_min"]
            lagou_obj.work_years_max = self["work_years_max"]
            lagou_obj.degree_need = self["degree_need"]
            lagou_obj.job_type = self["job_type"]
            lagou_obj.publish_time = self["publish_time"]
            lagou_obj.tags = self.get("tags")
            lagou_obj.job_advantage = self["job_advantage"]
            lagou_obj.job_desc = self["job_desc"]
            lagou_obj.job_addr = self["job_addr"]
            lagou_obj.company_url = self["company_url"]
            lagou_obj.company_name = self["company_name"]
            lagou_obj.save()


