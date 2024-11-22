import random

import scrapy

from spider_traffic.myutils.logger import logger

# 导入 logger 模块
from spider_traffic.spider.task import task_instance


class Spider(scrapy.Spider):
    name = "trace"
    allowed_domains = [task_instance.current_allowed_domain]
    start_urls = [task_instance.current_start_url]

    def parse(self, response):
        a_links = response.css("a::attr(href)").getall()
        if len(a_links) == 0:
            logger.info(f"{response.url} 没有提取到 URL")
            yield response.follow(
                task_instance.current_start_url, self.parse
            )  # 重新开始遍历
        random.shuffle(a_links)
        for link in a_links:
            # 拼接相对 URL 为绝对 URL
            full_url = response.urljoin(link)

            # 检查 URL 是否以 http 或 https 开头
            if full_url.startswith("http"):
                if "analytics" in full_url and "x.com" in full_url:
                    continue
                # 剔除类似登录注册页面
                if any(
                    keyword in full_url for keyword in task_instance.exclude_keywords
                ):
                    continue
                # 跟随提取的链接
                yield response.follow(full_url, self.parse)