# 流量捕获系统

该系统用于在Docker内部执行程序，包含爬虫和流量收集功能。该系统可以根据需求进行灵活配置，支持不同的爬取深度、爬取方式以及流量捕获方式。

该分支支持一次访问多个网站，这里的网站会从urls.txt中随机选择n个，捕获流量（仅访问主页）。


## 提前准备

1. 在生成镜像之前，需要在bin目录中准备以下文件，名称和结构要匹配

```
.
├── chromedriver-linux64
│   ├── chromedriver
│   └── LICENSE.chromedriver
├── google-chrome-stable_current_amd64.deb
└── Xray-linux-64
    ├── geoip.dat
    ├── geosite.dat
    ├── LICENSE
    ├── README.md
    └── xray
```

> Chrome浏览器的安装包和驱动需要相互匹配。

2. 修改Dockerfile中的基底镜像

本次的Dockerfile文件采用Ubuntu:latest基底，仅支持direct模式和xray模式，tor模式的环境依赖需要另外写Dockerfile文件

在使用Dockerfile文件打包镜像之前，需要修改第一行采用的基底镜像

## 构建 Docker 镜像

在开始使用之前，首先需要构建Docker镜像。执行以下命令来构建镜像：

```bash
docker build -t aimafan/spider_traffic:v1 .
```

## 部署说明
该项目的部署可以参考服务部署项目：[traffic_spider_bushu](https://github.com/ZGC-BUPT-aimafan/traffic_spider_bushu.git) 。



