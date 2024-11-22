import os
import subprocess
import threading
from datetime import datetime
from queue import Queue

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spider_traffic.myutils import project_path
from spider_traffic.myutils.config import config
from spider_traffic.myutils.logger import logger
from spider_traffic.spider.spiders.trace import Spider
from spider_traffic.traffic.capture import capture

# 定义停止信号的队列
stop_signal_queue = Queue()
process = CrawlerProcess(get_project_settings())


def stop_crawlers_after_delay(process):
    logger.info("定时器到期，停止爬虫。")
    for crawler in process.crawlers:
        crawler.stop()
    stop_signal_queue.put("STOP")


# 启动爬虫
def start_spider():
    time_limit = int(config["spider"]["time_per_website"])
    # 添加你要运行的爬虫
    process.crawl(Spider)

    # 开启定时器
    timer_thread = threading.Timer(
        time_limit, stop_crawlers_after_delay, args=(process,)
    )
    # timer_thread.daemon = True  # 设置为守护线程
    timer_thread.start()

    logger.info(f"开始爬取数据，爬取时间设为{str(time_limit/60)}分钟")

    # 启动爬虫
    process.start()

    stop_signal_queue.get()
    logger.info("收到停止信号，准备停止爬虫。")


def kill_chrome_processes():
    try:
        # Run the command to kill all processes containing 'chrome'
        subprocess.run(
            ["sudo", "pkill", "-f", "chrome"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr.decode('utf-8')}")


def traffic(VPS_NAME, PROTOCAL_NAME, SITE_NAME, url):
    # 获取当前时间
    current_time = datetime.now()
    # 格式化输出
    formatted_time = current_time.strftime("%Y%m%d%H%M%S")

    # 输出的格式：协议_时间_设备_位置_网站.pcap
    output_name = f"{PROTOCAL_NAME}_{formatted_time}_{VPS_NAME}_{SITE_NAME}_{url.split("//")[-1]}.pcap"
    output_path = os.path.join(
        project_path, "data", "pcap", url.split("//")[-1], output_name
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    traffic_process = capture(output_path)

    return traffic_process


if __name__ == "__main__":
    start_spider()
