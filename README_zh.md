# 智能培训助手

[![simpleui](https://img.shields.io/badge/developing%20with-Simpleui-2077ff.svg)](https://github.com/newpanjing/simpleui)

[English Readme](./README.md)
[视频](https://aws.highspot.com/items/666812973cc797aaa133c66a?lfrm=shp.4)

- [智能培训助手](#智能培训助手)
  - [简介](#简介)
  - [智能培训助手是什么？](#智能培训助手是什么)
  - [为什么要开发智能培训助手](#为什么要开发智能培训助手)
  - [为什么要使用智能培训助手](#为什么要使用智能培训助手)
  - [在线演示 (仅供GenAIIC内部使用，该IP已不支持，请自行部署，用户名密码不变)](#在线演示-仅供genaiic内部使用该ip已不支持请自行部署用户名密码不变)
  - [功能详情](#功能详情)
    - [基本设置](#基本设置)
    - [角色对话设置](#角色对话设置)
    - [对话检查器设置](#对话检查器设置)
  - [预设助手](#预设助手)
  - [安装](#安装)
  - [使用方法](#使用方法)
  - [贡献者](#贡献者)
  - [常见问题](#常见问题)



## 简介

**本项目是AWS GenAIIC的一个实验性项目。这个代码仅用于研究和测试目的,不适合用于生产环境。请不要将此代码部署到生产环境中。如果您有任何问题或需要在生产环境中使用此项目,请联系 Hao Huang (tonyhh@amazon.com)。**

## 智能培训助手是什么？

智能培训助手包括对话质检和客服培训助手，可以协助客服部门完成自定义维度的对话质检和自定义流程的客服培训。

## 为什么要开发智能培训助手

1）客服业务中，生成式AI有很大应用场景；
2）质检与培训是客服部门核心需求；
3）智能培训助手提供了一个客服质检和培训生成式AI应用模板，可以快速基于此模板进行二次开发，满足客户个性化需求。

## 为什么要使用智能培训助手

- 快速开发，快速给客户演示
- 关注业务，忽略底层技术实现
- 良好的可拓展性，可以方便地进行二次开发
- 完善的后台和权限管理

![web_login_page](./frontend/readme/imgs/架构图.png)

**智能培训助手**基于GenAIIC POC项目(客户: Huolala, Mobvista),包含两个关键组件:
- **角色助手**: 角色助手能根据预定义角色背景、对话背景、语言风格和其他相关设定进行模拟对话。
- **质检助手**: 质检助手能够根据自定义的领域或主题评估对话质量，判断是否合规。

在架构方面,**智能培训助手**包括:
- 基于Django的后端:
    - 支持 **RESTful API**;
    - 支持 **基于Token的权限控制**;
    - Amazon RDS中的MySQL数据库;

- 基于Streamlit的前端:
    - 一个使用简单的streamlit前端（**请勿用于生产环境**）。

## 在线演示 (仅供GenAIIC内部使用，该IP已不支持，请自行部署，用户名密码不变)
- 演示网站: http://54.159.114.20:8501/admin/
    - 由于演示环境并非生产环境,因此您可能会遇到无法访问的情况。如果无法访问在线演示,请通过 Slack 联系我(Hao Huang,tonyhh@amazon)。
    - 以下账户并非超级用户,如果您需要访问用户管理,请通过 Slack 联系我(Hao Huang,tonyhh@amazon)。
- Username: GenAIIC-test01
- Password: 20240410genaiic
- API Doc: http://54.159.114.20:8501/redoc/
- API Swagger: http://54.159.114.20:8501/swagger/

![web_login_page](./frontend/readme/imgs/web_login_page.png)

## 功能详情

### 基本设置
<details> <summary>详细介绍</summary>

基本设置包括基本模型设置和核心提示设置:
- 模型设置: 您可以在这里添加/修改/删除/搜索基本模型。目前,我们只支持Claude 3模型。
</details>


### 角色对话设置

<details> <summary>详细介绍</summary>

**角色助手设置**由四个部分组成:角色聊天机器人、技能、响应检查器和系统提示。

- 角色聊天机器人:
    - 角色定义了模拟训练助手的基本人格和语言风格。
    - 角色包括角色名称、角色背景、语言技能和其他相关特征。
- 技能:
    - 技能包括角色助手可以使用的对话状态,如被动响应、主动提出某个领域的问题等,用于控制对话流程。
    - 一项技能包括技能名称、技能描述、技能示例、响应检查器(可选)和LLM相关配置。
- 响应检查器:
    - 响应质量检查器可以检查助手在某个回合中的响应是否满足技能要求。如果不满足,它将请求新的生成,直到达到最大次数。
    - 响应质量检查器包括检查器名称、检查器描述、检查器提示、最大质量检查次数和LLM相关配置。检查器提示将直接输入到LLM,其中包含占位符{msg}。
- 系统提示词:
    - 系统提示词是**角色助手设置**的系统提示词。我们已经准备了两个系统提示(一个中文,一个英文)。如果您有特定要求,可以添加自己的核心提示。请记住,请在核心提示中保留**占位符**。请参考默认的系统提示(id1,中文)或系统提示(id2,英文)。


</details>



### 对话检查器设置 

<details> <summary>详细介绍</summary>

**对话检查器设置**由质量检查聊天机器人和对话检查器组成。

- 质量检查聊天机器人:
    - 质量检查聊天机器人定义了质量检查场景,包括名称、背景和一系列对话检查器。
- 对话检查器:
    - 对话检查器是专门用于检查对话质量的组件,输出格式默认为JSON格式。
    - 对话检查器包括检查器名称、描述、提示和LLM相关配置。检查器提示将直接输入到LLM,其中包含占位符{msg}。
    - 请注意,当您开发自己的提示词时,响应格式需要为JSON格式(便于在前端Streamlit中显示)。

</details>

## 预设助手

为了更直观的演示智能培训助手的所有功能，系统预设了一些助手供您选择。

- **角色助手**: 
    - 货拉拉司机助手（中文）：模拟一位货拉拉外部司机与邀约员对话。
    - 杰夫贝佐斯（英文）：模拟杰夫贝佐斯与对亚马逊感兴趣的人进行对话。
- **质检助手**: 
    - 货拉拉质检助手（中文）：
        - 能力提升分析：对邀约员给出能力提升建议
        - 服务态度检测：检测邀约员的服务态度
    - 通用质检助手（英文）：
        - 脏话检测：检测对话是否含有脏话
        - 态度检测：检测对话态度是否粗鲁
        - 信息校验（基于知识库）：检测对话内容是否与知识库数据相符合

## 安装

![architecture](./frontend/readme/imgs/architecture.png)


- AWS 预先条件
    - AWS Services
        - AWS EC2 (t3.medium is enough, 40GB disk is enough, OS: Ubuntu or Amazon Linux)
        - (optional) AWS RDS
    - AWS Permissions
        - AmazonBedrockFullAccess  (你需要先申请Claude 3的权限)
    - Security Groups
        - Type:Custom Port:8501 Source:0.0.0.0/0
        - Type:Custom Port:8502 Source:0.0.0.0/0

- 安装anaconda
```
# miniconda安装示例
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh
```

- 下载Repo
```bash
git clone git@ssh.gitlab.aws.dev:genaiic-reusable-assets/demo-artifacts/smart_training_assistant.git
```

- 一键安装python环境
```bash
sh ./install.sh
```


## 使用方法

- 激活Conda环境

```bash
conda activate smart_training_assistant
```

- **设置Iframe页面**
你需要修改Django中Iframe的页面地址来访问前端：
    - 修改位置：`/smart_training_assistant/backend/backend/settings.py` 162行，请修改为你机器的公网IP地址。

- 一键运行

```bash
sh ./run.sh
```

- **配置Bedrock区域**
  - 默认区域为us-east-1，如果您需要修改bedrock调用区域，请进入配置页面Base Setting -> Base models，选择对应模型进行修改。

- 一键停止

```bash
sh ./stop.sh
```

## 贡献者
- Nancy Wu (Nancynwu@amazon.com)
- Hao Huang (tonyhh@amazon.com)
- Xuefei Zhang (xuefegzh@amazon.com)
- Guang Yang (yaguan@amazon.com)

## 常见问题

- 我无法访问我的网站
  - 请断开VPN使用；
  - 网站的访问地址是：http://你的公网IP:8501/admin/
  - 请注意你的8501，8502两个端口的安全组已经开放
  - 如果还不能访问，请检查前后端log文件，查看是否存在错误。

- 我可以访问网站，但是聊天机器人提示没有权限访问模型：
  - 请检查你的Bedrock权限
  - 请检查你是否可以访问这个模型
  - 请检查你的区域是否与后端配置中 Base Setting -> Base models中对应模型区域一致
