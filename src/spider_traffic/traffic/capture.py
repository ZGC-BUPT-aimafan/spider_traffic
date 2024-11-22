import os
import shutil
import subprocess
import time
from datetime import datetime

from spider_traffic.myutils import project_path
from spider_traffic.myutils.config import config
from spider_traffic.myutils.logger import logger

should_stop_capture = False


def capture(output_path):
    ip_addr = config["information"]["ip_addr"]
    # 设置tcpdump命令的参数
    tcpdump_command = [
        "tcpdump",
        "-i",
        "any",
        "-n",
        "host",
        ip_addr,
        "and",
        "not",
        "port",
        "22",
        "and",
        "not",
        "port",
        "80",
        "-w",
        output_path,  # 输出文件的路径
    ]

    process = subprocess.Popen(
        tcpdump_command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    time.sleep(1)

    logger.info(f"流量采集开始，pcap输出路径 {output_path}")
    return process


def stop_capture(formatted_time, TASK_NAME):
    global process
    process.terminate()
    log_path = os.path.join(config["spider"]["i2pd_path"], "aimafan.log")
    dst_dir = os.path.join(project_path, "data", TASK_NAME, "log_file")
    dst_name = os.path.join(dst_dir, f"{formatted_time}.log")
    try:
        move_log(log_path, dst_name)
    except Exception as e:
        logger.error(f"无法将log文件{log_path}移动到指定位置：{e}")
    return dst_name


def move_log(log_path, dst_path):
    if not os.path.exists(os.path.dirname(dst_path)):
        os.makedirs(os.path.dirname(dst_path))
    shutil.move(log_path, dst_path)


if __name__ == "__main__":
    capture("www.baidu.com", "TEST", "1111111", "tcp")
    time.sleep(9)
    stop_capture("11111", "test")
