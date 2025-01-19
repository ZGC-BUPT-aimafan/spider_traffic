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


def run_action_script():
    command = ["../.venv/bin/python3", "-m", "spider_traffic.action"]
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

    while True:
        if SPIDER_MODE == "xray":
            xray_path = os.path.join(project_path, "bin", "Xray-linux-64", "xray")
            config_path = os.path.join(project_path, "config", "xray.json")

        while True:
            # 开流量收集
            kill_chrome_processes()
            traffic_process = traffic(
                VPS_NAME, PROTOCAL_NAME, SITE_NAME, task_instance.current_start_url
            )
            # 开xray
            # 后台运行并脱离主程序
            if SPIDER_MODE == "xray":
                xray_process = subprocess.Popen(
                    [xray_path, "run", "--config", config_path],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                logger.info(f"开启Xray程序，加载配置文件{config_path}")
                time.sleep(5)
            action_thread = threading.Thread(target=run_action_script)
            # 启动线程
            action_thread.start()
            # 等待线程完成
            action_thread.join()

            time.sleep(3)
            logger.info("关闭浏览器进程")
            kill_chrome_processes()
            time.sleep(30)
            logger.info("等待流量结束")

            if SPIDER_MODE == "xray":
                # 关xray
                xray_process.terminate()  # 尝试优雅地关闭进程

                # 如果进程没有退出，使用kill强制终止
                try:
                    xray_process.wait(timeout=5)  # 等待进程退出，最多等5秒
                except subprocess.TimeoutExpired:
                    xray_process.kill()  # 如果进程没有在超时前退出，强制杀死进程
            # 关流量收集
            traffic_process.terminate()  # 尝试优雅地关闭进程

            # 如果进程没有退出，使用kill强制终止
            try:
                traffic_process.wait(timeout=5)  # 等待进程退出，最多等5秒
                logger.info("优雅的关闭流量收集进程")
            except subprocess.TimeoutExpired:
                traffic_process.kill()  # 如果进程没有在超时前退出，强制杀死进程
                logger.info("强制杀死流量收集进程")
            logger.info(
                f"第{str(task_instance.current_index)}个url爬取完成，爬取下一个url"
            )
            task_instance.current_index = (
                task_instance.current_index + 1
            ) % task_instance.url_num
            running_path = os.path.join(project_path, "config", "running.json")
            with open(running_path, "w") as f:
                json.dump({"currentIndex": task_instance.current_index}, f)


if __name__ == "__main__":
    browser_action()
