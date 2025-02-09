import json
import os
import subprocess
import threading
import time

from spider_traffic.action import kill_chrome_processes, traffic
from spider_traffic.myutils import project_path
from spider_traffic.myutils.config import SPIDER_MODE, config
from spider_traffic.myutils.logger import logger
from spider_traffic.spider.task import task_instance
from spider_traffic.torDo import close_tor, start_tor


def run_action_script(start_urls, traffic_path):
    command = [
        "../.venv/bin/python3",
        "-m",
        "spider_traffic.action",
        " ".join(start_urls),
        traffic_path,
    ]
    # 使用 subprocess 运行 action.py
    subprocess.run(command)


def browser_action():
    VPS_NAME = config["information"]["name"]
    PROTOCAL_NAME = config["information"]["protocal"]
    SITE_NAME = config["information"]["site"]

    # 检查SPIDER_MODE是否为有效值
    valid_modes = ["xray", "tor", "direct"]
    if SPIDER_MODE not in valid_modes:
        raise ValueError(
            f"Invalid SPIDER_MODE: {SPIDER_MODE}. Must be one of {valid_modes}."
        )

    if SPIDER_MODE == "xray":
        xray_path = os.path.join(project_path, "bin", "Xray-linux-64", "xray")
        config_path = os.path.join(project_path, "config", "xray.json")

    while True:
        start_urls = task_instance.current_start_url

        def begin():
            # 开流量收集
            kill_chrome_processes()
            traffic_process, traffic_path = traffic(
                VPS_NAME, PROTOCAL_NAME, SITE_NAME, start_urls
            )
            # 开xray
            # 后台运行并脱离主程序
            if SPIDER_MODE == "xray":
                proxy_process = subprocess.Popen(
                    [xray_path, "run", "--config", config_path],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                logger.info(f"开启Xray程序，加载配置文件{config_path}")
                return traffic_process, proxy_process, True, traffic_path

            elif SPIDER_MODE == "tor":
                proxy_process, result = start_tor()

                return traffic_process, proxy_process, result, traffic_path

            else:
                return traffic_process, None, True, traffic_path

        def stop(traffic_process, proxy_process, traffic_path, result=True):
            if SPIDER_MODE == "xray":
                # 关xray
                proxy_process.terminate()  # 尝试优雅地关闭进程

                # 如果进程没有退出，使用kill强制终止
                try:
                    proxy_process.wait(timeout=5)  # 等待进程退出，最多等5秒
                except subprocess.TimeoutExpired:
                    proxy_process.kill()  # 如果进程没有在超时前退出，强制杀死进程
            elif SPIDER_MODE == "tor":
                close_tor(proxy_process)

            # 关流量收集
            traffic_process.terminate()  # 尝试优雅地关闭进程

            # 如果进程没有退出，使用kill强制终止
            try:
                traffic_process.wait(timeout=5)  # 等待进程退出，最多等5秒
                logger.info("优雅的关闭流量收集进程")
            except subprocess.TimeoutExpired:
                traffic_process.kill()  # 如果进程没有在超时前退出，强制杀死进程
                logger.info("强制杀死流量收集进程")
            if SPIDER_MODE == "tor" and result is not True:
                if os.path.exists(traffic_path):
                    os.remove(traffic_path)

        traffic_process, proxy_process, result, traffic_path = begin()
        if result is False:
            stop(traffic_process, proxy_process, traffic_path, False)
            continue

        if SPIDER_MODE == "tor":
            logger.info("等待tor网络稳定")
            time.sleep(60)

        action_thread = threading.Thread(
            target=run_action_script,
            args=(
                start_urls,
                traffic_path,
            ),
        )
        # 启动线程
        action_thread.start()
        # 等待线程完成
        action_thread.join()

        time.sleep(3)
        logger.info("关闭浏览器进程")
        kill_chrome_processes()
        time.sleep(30)
        logger.info("等待流量结束")

        stop(traffic_process, proxy_process, traffic_path, True)


if __name__ == "__main__":
    browser_action()
