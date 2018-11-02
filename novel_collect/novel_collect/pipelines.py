# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from urllib import parse

from scrapy.pipelines.images import ImagesPipeline

from novel_collect.items import NovelInfoItem

class NovelCollectPipeline(object):
    def process_item(self, item, spider):
        return item


class DownloadImagePipeline(ImagesPipeline):
    def process_item(self, item, spider):
        if isinstance(item, NovelInfoItem):
            return super(DownloadImagePipeline, self).process_item(item, spider)
        return item

    def get_media_requests(self, item, info):
        item["image"] = [parse.urljoin(item["url"], image) for image in item["image"]]
        return super(DownloadImagePipeline, self).get_media_requests(item, info)

    def file_path(self, request, response=None, info=None):
        path = super(DownloadImagePipeline, self).file_path(request, response, info)
        image_path = path.replace("full/", "")
        return image_path

    def item_completed(self, results, item, info):
        return item


class SaveMysqlPipeline:
    def process_item(self, item, spider):
        if hasattr(item, "save_for_mysql"):
            item.save_for_mysql()
        return item


class WriteFilePipeline:
    def process_item(self, item, spider):
        if hasattr(item, "write_file"):
            item.write_file()
        return item
