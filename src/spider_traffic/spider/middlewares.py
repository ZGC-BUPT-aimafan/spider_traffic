# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# useful for handling different item types with a single interface
import json
import os
from datetime import datetime

from scrapy import signals
from scrapy.http import HtmlResponse

from spider_traffic.myutils import project_path
from spider_traffic.myutils.config import config
from spider_traffic.myutils.logger import logger, logger_url
from spider_traffic.spider.chrome import create_chrome_driver, scroll_to_bottom
from spider_traffic.spider.task import task_instance


def append_dict_to_jsonl(data_dict):
    """
    将字典追加到 JSONL 文件中，如果文件不存在则创建。

    :param data_dict: 要追加的字典
    """
    # 确保输入的数据是字典
    if not isinstance(data_dict, dict):
        raise ValueError("输入数据必须是字典类型")
    file_path = os.path.join(project_path, "data", "urls_log.jsonl")
    # 打开文件并以追加模式写入
    with open(file_path, "a") as file:
        # 将字典序列化为 JSON 格式并写入文件
        file.write(json.dumps(data_dict, ensure_ascii=False) + "\n")


class SpiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SpiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __init__(self):
        logger.info(f"创建浏览器驱动")
        self.max_webnum = (
            int(config["spider"]["webnum"])
            if int(config["spider"]["webnum"]) != -1
            else 999999
        )
        self.browser = create_chrome_driver()

    def __del__(self):
        logger.info(f"关闭浏览器驱动")

        self.browser.close()

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if spider.pcap_path not in task_instance.urls_log:
            task_instance.urls_log[spider.pcap_path] = []
        task_instance.requesturlNum += 1

        if task_instance.requesturlNum == 1:
            self.browser.get(request.url)
        else:
            self.browser.execute_script("window.open('');")  # 打开新标签页
            self.browser.switch_to.window(
                self.browser.window_handles[-1]
            )  # 切换到新标签页
            self.browser.get(request.url)  # 访问新 URL
        # 获取当前时间
        now = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        task_instance.urls_log[spider.pcap_path].append([now, request.url])

        # 格式化时间输出，格式为YYYYMMDDHHMMSSsss（精确到毫秒）

        logger_url.info(f"{spider.pcap_path} : {request.url}")
        if task_instance.requesturlNum == len(spider.start_urls):
            append_dict_to_jsonl(task_instance.urls_log)
        if config["spider"]["scroll"].lower() == "true":
            scroll_to_bottom(self.browser)
        return HtmlResponse(
            url=request.url,
            body=self.browser.page_source,
            encoding="utf-8",
            request=request,
        )

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
