# -*- coding: utf-8 -*-
import time
from urllib import parse
import re
from datetime import datetime
import json

import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader

from Article.items import ZhihuQuestionItem, ZhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    answer_start_url = r'https://www.zhihu.com/api/v4/questions/{0}/answers' \
                       r'?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&' \
                       r'limit={1}&offset={2}&sort_by=default'

    def parse(self, response):
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = [url for url in all_urls if "https" in url]
        for url in all_urls:
            match_obj = re.match(r'(.*zhihu.com/question/(\d+)[/$])', url)
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                yield Request(url=request_url, dont_filter=True, headers=self.headers,
                              meta={"question_id": question_id},
                              callback=self.parse_question)

    def parse_question(self, response):
        question_id = response.meta.get("question_id")
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_value("zhihu_id", question_id)
        item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")
        item_loader.add_value("url", response.url)
        item_loader.add_css("title", ".QuestionHeader .QuestionHeader-title::text")
        item_loader.add_css("content", ".QuestionHeader-detail")
        item_loader.add_css("answer_num", ".List-headerText span::text")
        item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
        item_loader.add_css("watch_user_num", ".NumberBoard-itemValue::text")
        item_loader.add_css("click_num", ".NumberBoard-itemValue::text")
        item_loader.add_value("crawl_time", datetime.now())
        item_loader.add_value("crawl_update_time", datetime.now())
        question_item = item_loader.load_item()

        yield Request(url=self.answer_start_url.format(question_id, 5, 0), dont_filter=True, headers=self.headers,
                      callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        answer_json = json.loads(response.text)
        is_end = answer_json["paging"]["is_end"]
        totals = answer_json["paging"]["totals"]
        next_url = answer_json["paging"]["next"]

        for answer in answer_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if answer["content"] else answer["excerpt"]
            answer_item["praise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.now()
            answer_item["crawl_update_time"] = datetime.now()
            yield answer_item

        if not is_end:
            yield Request(url=next_url, dont_filter=True, headers=self.headers, callback=self.parse_answer)

    def start_requests(self):
        from selenium import webdriver
        url = r'https://www.zhihu.com'
        browser = webdriver.Chrome(executable_path=r"E:/chromedriver.exe")
        browser.get(url)
        browser.find_element_by_css_selector(".SignContainer-switch span").click()
        time.sleep(0.5)

        browser.find_element_by_css_selector(".SignFlow-account input[name='username']").send_keys("18719091650")
        browser.find_element_by_css_selector(".SignFlow-password input[name='password']").send_keys("5201314ouru")
        time.sleep(0.5)

        browser.find_element_by_css_selector(".SignFlow-submitButton").click()
        time.sleep(5)

        cookies = browser.get_cookies()
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie["name"]] = cookie["value"]

        browser.close()
        for url in self.start_urls:
            yield Request(url=url, dont_filter=True, cookies=cookie_dict, headers=self.headers, callback=self.parse)
