import random

import scrapy

from spider_traffic.myutils.config import config
from spider_traffic.myutils.logger import logger

# 导入 logger 模块


class Spider(scrapy.Spider):
    name = "trace"

    def __init__(self, start_urls=None, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        if start_urls:
            self.start_urls = start_urls

    def parse(self, response):
        pass
