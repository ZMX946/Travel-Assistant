# 旅游规划机器人

基于 LangGraph 和 LLM 的智能旅游行程规划助手，能够根据用户需求自动规划详细的旅游行程，包括景点推荐、路线规划、餐饮住宿等全方位服务。

Please cite the paper if this is helpful to you:

> Wei Kang, Maoxuan Zhou, Yu Guo, Tianfu Li, Jiandong Li, Yuwei Liu.  
> *Generative adversarial augmented multi-scale CNN for machine fault diagnosis*.  
> Control Engineering Practice, Volume 167, 2026, 106625.  
> https://doi.org/10.1016/j.conengprac.2025.106625  
> https://www.sciencedirect.com/science/article/pii/S0967066125003879


## 🌟 功能特色

- **智能目的地推荐**：根据用户需求推荐合适的旅游目的地
- **景点信息获取**：自动获取目的地景点详细信息（开放时间、游玩时长等）
- **精确位置定位**：获取景点经纬度坐标，确保路线规划准确性
- **智能行程规划**：基于景点位置、开放时间等因素合理安排每日行程
- **交通路线规划**：提供景点间的交通方案和时间预估
- **周边服务搜索**：推荐餐厅、酒店等周边服务设施
- **实时网络搜索**：获取最新的旅游信息和资讯
- **交互式界面**：基于 Gradio 的友好 Web 界面

## 🏗️ 项目架构

```
旅游规划机器人/
├── agents/          # 智能代理模块
│   └── agents.py    # 异步/同步代理实现
├── graph/           # LangGraph 工作流
│   └── graph.py     # 状态图构建和应用初始化
├── models/          # 模型工厂
│   └── factory.py   # LLM 模型工厂类
├── prompts/         # 提示词模板
│   └── main.py      # 主要提示词模板
├── states/          # 状态管理
│   └── state.py     # 公共状态定义
├── tools/           # 工具集合
│   ├── attractions.py    # 景点信息获取
│   ├── locations.py      # 位置坐标获取
│   ├── transportation.py # 交通路线规划
│   ├── nearby.py         # 周边搜索
│   ├── web_search.py     # 网络搜索
│   └── save.py           # 信息保存
├── utils/           # 工具函数
│   └── helper.py    # 辅助函数
└── webrun.py        # Web 应用启动入口
```

## 🛠️ 技术栈

- **核心框架**：LangGraph - 构建多代理工作流
- **语言模型**：OpenAI GPT-4o-mini
- **Web 框架**：Gradio - 构建交互式界面
- **网络爬虫**：Selenium + BeautifulSoup - 获取景点信息
- **地图服务**：高德地图 API - 位置和路线服务
- **搜索引擎**：DuckDuckGo - 网络信息搜索

## 📋 环境要求

- Python 3.11
- Chrome 浏览器（用于 Selenium）
- 高德地图 API Key
- OpenAI API Key

## 🚀 快速开始

### 1. 进入项目

```bash
cd 旅游规划机器人
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件并配置以下环境变量：

```env
OPENAI_API_KEY=your_openai_api_key
AMAP_API_KEY=your_amap_api_key
```

### 4. 启动应用

```bash
python webrun.py
```

应用将在浏览器中自动打开，默认地址：`http://localhost:7860`

## 🎯 使用指南


### 基本使用流程

1. **输入旅游需求**：描述您的旅游偏好、时间、预算等
2. **选择目的地**：从推荐的目的地中选择心仪的地点
3. **确认景点**：查看景点详情并选择想要游览的景点
4. **查看行程**：获得详细的每日行程安排
5. **完善服务**：添加餐饮和住宿推荐



## 🔧 核心工具说明

| 工具名称 | 功能描述 | API 依赖 |
|---------|---------|----------|
| `get_attractions_information` | 获取目的地景点信息 | 马蜂窝网站爬虫 |
| `get_location_coordinate` | 获取地点经纬度坐标 | 高德地图 API |
| `route_planning` | 规划交通路线 | 高德地图 API |
| `search_nearby_poi` | 搜索周边设施 | 高德地图 API |
| `web_search` | 网络信息搜索 | DuckDuckGo |

