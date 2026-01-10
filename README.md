# 上市储量价值评估石油生产数据预处理系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-orange.svg)](https://pandas.pydata.org/)

> 一个专业的石油生产数据预处理系统，用于处理A2数据表、SEC数据表和评估数据表，支持数据对比、井变化识别、SEC表生成和评估表生成等功能。

## ✨ 主要特性

- 🔄 **智能数据对比** - 自动对比A2表与SEC表，识别参评井和非参评井
- 🔍 **井变化追踪** - 识别注销井、新投井和单元归属变化井
- 📊 **SEC表生成** - 自动生成本年度SEC数据表，支持单元调整和新井导入
- 📈 **评估表生成** - 生成常规油和页岩油评估数据表，支持历史数据调整
- 🌲 **树形结构展示** - 可视化展示油田-单元-井号三级关系
- 💾 **批量数据处理** - 支持处理12个月连续数据（120万+条记录）
- 🖥️ **Web界面操作** - 友好的Web界面，支持文件上传和结果下载
- 🔌 **RESTful API** - 完整的API接口，支持程序化调用

## 系统概述
本系统用于处理石油生产数据，包括A2数据表、SEC数据表和评估数据表的预处理、对比、合并等操作。

## 项目结构
```
oilSystem/
├── backend/               # 后端代码
│   ├── models/           # 数据模型
│   ├── services/         # 业务逻辑
│   ├── utils/            # 工具函数
│   └── app.py            # Flask应用入口
├── frontend/             # 前端代码
│   ├── static/           # 静态资源
│   ├── templates/        # HTML模板
│   └── js/               # JavaScript文件
├── data/                 # 数据存储目录
│   ├── input/            # 输入数据
│   └── output/           # 输出数据
└── requirements.txt      # Python依赖
```

## 🚀 快速开始

### 方式1：使用安装脚本（推荐）

```bash
# 1. 进入项目目录
cd /Users/zzaki/workspace_oil/oilSystem

# 2. 运行安装脚本
./install.sh

# 3. 启动服务
./start.sh

# 4. 访问系统
# 在浏览器中打开: http://localhost:5000
```

### 方式2：手动安装

```bash
# 1. 安装依赖
```bash
pip install -r requirements.txt
```

# 2. 运行示例代码（生成测试数据）
python3 example_usage.py

# 3. 启动后端服务
```bash
cd backend
python app.py
```

# 4. 访问系统
在浏览器中打开: http://localhost:5000
```

## 📚 文档导航

- **[QUICK_START.md](QUICK_START.md)** - 5分钟快速入门指南
- **[USER_GUIDE.md](USER_GUIDE.md)** - 详细的使用说明和API文档
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - 项目架构和技术实现
- **[example_usage.py](example_usage.py)** - Python API使用示例

## 🌟 功能模块

### 第一业务界面
- 对比上年度A2表与SEC表
- 生成油井单元属性表
- 识别参评井和非参评井

### 第二业务界面
- 对比本年度与上年度A2表
- 识别注销井、新投井、归属变化井
- 生成SEC单元变化表

### 第三业务界面
- 调整SEC单元归属
- 导入老区新井
- 导入扩边/PUD转PDP/PDNP井
- 生成本年度SEC数据表

### 第四业务界面
- 常规油评估数据表处理
- 页岩油评估数据表处理
- 历史数据调整
- 生成最终评估数据表
