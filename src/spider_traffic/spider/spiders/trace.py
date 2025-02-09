import random

import scrapy

from spider_traffic.myutils.config import config
from spider_traffic.myutils.logger import logger

# 导入 logger 模块


class Spider(scrapy.Spider):
    name = "trace"

    def __init__(self, start_urls=None, pcap_path=None, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.pcap_path = pcap_path
        if start_urls:
            self.start_urls = start_urls

    def __init__(self, pcap_path=None, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.pcap_path = pcap_path

    def parse(self, response):
        pass
