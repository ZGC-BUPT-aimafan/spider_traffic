import configparser
import os

from spider_traffic.myutils import project_path

# 创建一个配置解析器
config = configparser.ConfigParser()

# 读取配置文件
config_defult_path = os.path.join(project_path, "config", "config.ini")
config.read(config_defult_path)

SPIDER_MODE = config["spider"]["mode"]
multisite_num = int(config["spider"]["multisite_num"])

# 可以在这里添加一些函数来获取特定的配置项
# def get_database_config():
#     return {
#         'host': config['database']['host'],
#         'user': config['database']['user'],
#         'password': config['database']['password'],
#         'database': config['database']['database']
#     }
