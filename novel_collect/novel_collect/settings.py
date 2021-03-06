# -*- coding: utf-8 -*-

import os, sys
import django

# Scrapy settings for novel_collect project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'novel_collect'

SPIDER_MODULES = ['novel_collect.spiders']
NEWSPIDER_MODULE = 'novel_collect.spiders'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATAREPO_DIR = os.path.join(BASE_DIR, "datarepo")
sys.path.append(DATAREPO_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'datarepo.settings'
django.setup()
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'novel_collect (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'novel_collect.middlewares.NovelCollectSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'novel_collect.middlewares.NovelCollectDownloaderMiddleware': 543,
    # 'novel_collect.middlewares.ProxyIpMiddleware': 1,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'novel_collect.pipelines.NovelCollectPipeline': 300,
    # 'novel_collect.pipelines.DownloadImagePipeline': 1,
    # 'novel_collect.pipelines.SaveMysqlPipeline': 2,
    # 'novel_collect.pipelines.WriteFilePipeline': 3,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

IMAGES_URLS_FIELD = "image"
IMAGES_STORE = os.path.join(BASE_DIR, "images")
if not os.path.exists(IMAGES_STORE):
    os.makedirs(IMAGES_STORE)

NOVELS_DIR = os.path.join(BASE_DIR, "novels")
