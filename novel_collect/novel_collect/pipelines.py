# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from urllib import parse

from scrapy.pipelines.images import ImagesPipeline

class NovelCollectPipeline(object):
    def process_item(self, item, spider):
        return item


class DownloadImagePipeline(ImagesPipeline):
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
        item.save_for_mysql()
        return item
