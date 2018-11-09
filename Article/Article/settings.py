# -*- coding: utf-8 -*-

import os, sys
import django

DATA_REPO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_repo")
sys.path.append(DATA_REPO_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'data_repo.settings'
django.setup()


# Scrapy settings for Article project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Article'

SPIDER_MODULES = ['Article.spiders']
NEWSPIDER_MODULE = 'Article.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Article (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Article.middlewares.ArticleSpiderMiddleware': 543,
# }

#User-Agent的类型
USER_AGNET_TYPE = "random"

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'Article.middlewares.ArticleDownloaderMiddleware': 543,
   # 'Article.middlewares.RandomUserAgentMiddleware': 1,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Article.pipelines.ArticlePipeline': 300,

    # 'scrapy.pipelines.images.ArticleImagePipeline' : 1,
    # 'Article.pipelines.JsonWithEncodingPipeline' : 2,
    # 'Article.pipelines.JsonExporterPipeline' : 3,
    # 'Article.pipelines.CustomMysqlPipeline' : 4,
    # 'Article.pipelines.DjangoMysqlPipeline': 5,
   # 'Article.pipelines.SaveMysqlPipeline' : 6,
}

IMAGES_URLS_FIELD = "front_image"
project_dir = os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE = os.path.join(project_dir, "images")

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = "193.112.150.18"
MYSQL_DBNAME = "scrapy_test"
MYSQL_USER = "ouru"
MYSQL_PASSWORD = "5201314Ouru..."
MYSQL_PORT = 3306
MYSQL_CHARSET = "utf8"
