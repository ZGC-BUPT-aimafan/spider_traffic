import json
import os

from spider_traffic.myutils import project_path


class Task:
    # 只能有一个实例
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Task, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.file_path = os.path.join(
                project_path, "config", "current_docker_url_list.txt"
            )
            self.urls = self.read_file()  # url的列表
            self.url_num = len(self.urls)
            self.requesturlNum = 0
            # 如果文件不存在，创建并写入默认内容
            if not os.path.exists(os.path.join(project_path, "config", "running.json")):
                with open(
                    os.path.join(project_path, "config", "running.json"), "w"
                ) as f:
                    json.dump({"currentIndex": 0}, f, indent=4)
            with open(os.path.join(project_path, "config", "running.json"), "r") as f:
                params = json.load(f)
                self.current_index = params["currentIndex"]
            with open(
                os.path.join(project_path, "config", "exclude_keywords"), "r"
            ) as f:
                self.exclude_keywords = [s.replace("\n", " ") for s in f.readlines()]
            self._initialized = True

    def read_file(self):
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        urls = [
            line.strip()
            for line in lines
            if line.strip() and not line.strip().startswith("#")
        ]
        return urls

    @property  # 可以实现向属性一样访问方法
    def current_start_url(self):
        url_str = self.urls[self.current_index]
        return r"https://" + url_str

    @property
    def current_allowed_domain(self):
        url_str = self.urls[self.current_index]
        return url_str


task_instance = Task()
