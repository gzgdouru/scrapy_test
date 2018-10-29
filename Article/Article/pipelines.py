# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter

from Article.utils.mysqlV1 import MysqlManager
from repository.models import JobboleArticle

class ArticlePipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline:
    '''自定义json文件导出'''
    def __init__(self):
        self.file = codecs.open("article.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False, indent=2) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline:
    '''调用scrapy提供的json export导出json文件'''
    def __init__(self):
        self.file = open("articleexport.json", "wb")
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for status, value in results:
                item["front_image_path"] = value["path"]
            return item


class CustomMysqlPipeline:
    def __init__(self, dbManager):
        self.dbManager = dbManager

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            port = settings["MYSQL_PORT"],
            charset = settings["MYSQL_CHARSET"],
        )

        dbManager = MysqlManager(**dbparams, max_overflow=20)
        return cls(dbManager)

    def process_item(self, item, spider):
        images = ",".join(item["front_image_url"])
        self.dbManager.insert("tb_jobbole", title=item["title"], create_date=item["create_date"], url=item["url"],
                              url_object_id=item["url_object_id"], front_image_url=images,
                              praise_nums=item["praise_nums"],
                              comment_nums=item["comment_nums"], fav_nums=item["fav_nums"],
                              tags=item["tags"])
        return item


class DjangoMysqlPipeline:
    def process_item(self, item, spider):
        images = ",".join(item["front_image_url"])
        jobble_article = JobboleArticle()
        jobble_article.title = item["title"]
        jobble_article.create_date = item["create_date"]
        jobble_article.url = item["url"]
        jobble_article.url_object_id = item["url_object_id"]
        jobble_article.front_image_url= images
        jobble_article.praise_nums = item["praise_nums"]
        jobble_article.comment_nums=item["comment_nums"]
        jobble_article.fav_nums=item["fav_nums"]
        jobble_article.tags=item["tags"]
        jobble_article.save()


class SaveMysqlPipeline:
    def process_item(self, item, spider):
        item.save_for_mysql()