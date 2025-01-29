# 流量捕获系统Spider Traffic

Spider Traffic 是一个用于采集和分析网络流量的自动化爬虫框架。该项目结合了网络爬虫技术和流量捕获机制，能够在不同的代理模式（如 Xray、Tor、Direct）下进行流量采集，并生成相应的 PCAP 文件。

## 核心功能
### 网络爬取与流量采集

通过 Scrapy 爬虫框架自动爬取目标网站的数据。
使用 tcpdump 进行网络流量捕获，生成 .pcap 格式的数据文件。

### 多种代理模式支持
Xray 模式：通过 Xray 代理进行流量传输。
Tor 模式：基于 Tor 网络进行匿名访问。
Direct 模式：直接访问目标网站。

### 自动化控制
通过 main.py 作为入口，自动调度流量采集与爬虫执行。
运行过程中动态管理 Chrome 进程，确保流量采集的完整性。
任务完成后自动停止代理服务和流量采集进程。

## 构建 Docker 镜像

在开始使用之前，首先需要构建Docker镜像。在有`dockerfile`的目录下执行以下命令来构建镜像（对应不同的操作系统、以及相同操作系统的不同版本有不同的`dockerfile`，默认为`ubuntu24`，其中`dockerfiles`目录中有`ubuntu20、debian12`版本的操作系统，如有需要可以将其替换为`spider_traffic`目录下的`dockerfile`）：
> 注意！！
> 如果安装的是`ubuntu20`，那么还需要在创建镜像之前将`requirements.txt`文件进行修改，可替换为`requirements`文件夹中的`requirements_ubuntu20.txt`，`txt`文件名保持和`spider_traffic`中一致的文件名；

由于本仓库中 `bin/google-chrome-stable_current_amd64.deb` 由git lfs托管，所以需要通过git lfs正确拉去该安装包

1. 安装git-lfs
```bash
sudo apt install git-lfs    // debian/ubuntu
brew install git-lfs        // mac
```

2. 克隆项目
```bash
git clone --recurse-submodules https://github.com/ZGC-BUPT-aimafan/spider_traffic.git
cd spider_traffic
git lfs pull
```

3. 构建镜像
```bash
docker build -t aimafan/spider_traffic:v1 .
```

## 部署说明
该项目的部署可以参考服务部署项目：[traffic_spider_bushu](https://github.com/ZGC-BUPT-aimafan/traffic_spider_bushu.git) 。



### Dockerfile 说明

在使用Dockerfile文件打包镜像之前，需要修改第一行采用的基底镜像