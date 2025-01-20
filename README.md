# 流量捕获系统

该系统用于在Docker内部执行程序，包含爬虫和流量收集功能。该系统可以根据需求进行灵活配置，支持不同的爬取深度、爬取方式以及流量捕获方式。


## 构建 Docker 镜像

在开始使用之前，首先需要构建Docker镜像。在有`dockerfile`的目录下执行以下命令来构建镜像（对应不同的操作系统、以及相同操作系统的不同版本有不同的`dockerfile`，默认为`ubuntu24`，其中`dockerfiles`目录中有`ubuntu20、debian12`版本的操作系统，如有需要可以将其替换为`spider_traffic`目录下的`dockerfile`）：
> 注意！！
> 如果安装的是`ubuntu20`，那么还需要在创建镜像之前将`requirements.txt`文件进行修改，可替换为`requirements`文件夹中的`requirements_ubuntu20.txt`，`txt`文件名保持和`spider_traffic`中一致的文件名；

```bash
docker build -t aimafan/spider_traffic:v1 .
```

## 部署说明
该项目的部署可以参考服务部署项目：[traffic_spider_bushu](https://github.com/ZGC-BUPT-aimafan/traffic_spider_bushu.git) 。


### 提前准备

在生成镜像之前，需要在bin目录中准备以下文件，名称和结构要匹配

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

### Dockerfile 说明

本次的Dockerfile文件采用Ubuntu:latest基底，仅支持direct模式和xray模式，tor模式的环境依赖需要另外写Dockerfile文件

在使用Dockerfile文件打包镜像之前，需要修改第一行采用的基底镜像