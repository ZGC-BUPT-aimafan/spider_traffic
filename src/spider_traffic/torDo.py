import os
import subprocess
import time
from multiprocessing import Process

from spider_traffic.myutils import project_path
from spider_traffic.myutils.logger import logger


def long_running_task(log_file):
    while True:
        time.sleep(1)
        f = os.popen(f"cat {log_file}|grep 'Bootstrapped 100%'|wc -l")
        process_num = int(f.read())
        if process_num != 0:
            break


def wait_for_100(log_file, timeout=180):
    # 创建子进程
    process = Process(target=long_running_task, args=(log_file,))
    process.start()
    process.join(timeout=timeout)  # 等待最多 x秒
    if process.is_alive():
        process.terminate()  # 强制终止子进程
        return False
    else:
        return True


def start_tor():
    """
    根据flag启动Tor程序:
        'none':裸Tor
        'meek':使用Meek的Tor
        'obfs4_0'使用Obfs4且客户端iat-mode=0的Tor
        'obfs4_1'使用Obfs4且客户端iat-mode=1的Tor
        'obfs4_2'使用Obfs4且客户端iat-mode=2的Tor
        'snowflake'使用snowflake的Tor
        'webtunnel'使用webtunnel的Tor
    Return:
        进程,启动成功标志(True为启动成功, False为启动不成功)
    """
    # 根据配置制作/挑选torrc文件
    torrc_file = os.path.join(project_path, "config", "torrc")
    log_file = os.path.join(project_path, "logs", "notice.log")
    tor_path = os.path.join(project_path, "bin", "tor_s", "tor")

    # 清空log日志用于后续判断Tor是否启动成功
    subprocess.call("echo > %s" % log_file, shell=True)
    # 使用torrc文件启动Tor
    tor_process = subprocess.Popen(
        [tor_path, "-f", torrc_file],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # 判断Tor是否启动成功
    tor_is_started = wait_for_100(log_file, 300)
    logger.info(f"Tor启动成功? {tor_is_started}!!")
    return tor_process, tor_is_started


def close_tor(tor_process):
    tor_process.terminate()  # 尝试优雅地关闭进程
    # 如果进程没有退出，使用kill强制终止
    try:
        tor_process.wait(timeout=5)  # 等待进程退出，最多等5秒
        logger.info("优雅的关闭Tor进程")
    except subprocess.TimeoutExpired:
        tor_process.kill()  # 如果进程没有在超时前退出，强制杀死进程
        logger.info("强制杀死Tor进程")


if __name__ == "__main__":
    # 测试启动Tor与关闭Tor
    tor_process, success = start_tor("webtunnel")
    print(f"{time.time}Tor启动成功?:{success}")
    time.sleep(20)
    close_tor(tor_process)
