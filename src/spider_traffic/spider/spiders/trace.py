import scrapy

from spider_traffic.myutils.logger import logger

# 导入 logger 模块
from spider_traffic.spider.task import task_instance


class Spider(scrapy.Spider):
    name = "trace"
    start_urls = [task_instance.current_start_url]

    def parse(self, response):
        logger.debug(response.body)
