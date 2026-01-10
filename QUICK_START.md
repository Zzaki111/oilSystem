# 快速开始指南

欢迎使用**上市储量价值评估石油生产数据预处理系统**！

---

## 🚀 5分钟快速开始

### 步骤1：安装依赖

在项目根目录下运行：

```bash
./install.sh
```

或者手动安装：

```bash
pip3 install pandas openpyxl numpy flask flask-cors python-dateutil xlrd
```

### 步骤2：生成示例数据

运行示例脚本，生成测试数据：

```bash
python3 example_usage.py
```

这将在 `data/input/` 目录下生成示例文件。

### 步骤3：启动服务

```bash
./start.sh
```

或者手动启动：

```bash
cd backend
python3 app.py
```

### 步骤4：访问系统

在浏览器中打开：

```
http://localhost:5000
```

---

## 📋 使用流程

### 方式1：通过Web界面

1. **第一业务界面**
   - 上传A2数据表（`a2-202409_sample.xlsx`）
   - 上传SEC数据表（`SEC数据表-202409_sample.xlsx`）
   - 输入年月：202409
   - 点击"开始对比"
   - 查看结果和树形结构

2. **第二业务界面**
   - 上传上年度A2表
   - 上传本年度A2表
   - 输入年份：2025
   - 点击"开始对比"
   - 查看注销井、新投井、变化井统计

3. **第三业务界面**
   - 上传上年度SEC表
   - 上传单元变化表（可选）
   - 上传老区新井表（可选）
   - 上传扩边/PUD表（可选）
   - 输入本年度年份和年月
   - 点击"生成SEC数据表"

4. **第四业务界面**
   - 选择评估类型（常规油/页岩油）
   - 上传相关数据表
   - 点击"生成评估数据表"

### 方式2：通过Python API

```python
from backend.utils.data_io import DataImportExport
from backend.services.business_service_1 import BusinessService1

# 读取数据
a2_df = DataImportExport.read_a2_table("data/input/a2-202409.xlsx")
sec_df = DataImportExport.read_sec_table("data/input/SEC数据表-202409.xlsx")

# 执行对比
result = BusinessService1.compare_a2_sec_tables(a2_df, sec_df, 202409)

# 保存结果
DataImportExport.write_excel(result, "data/output/结果.xlsx")
```

---

## 📁 目录结构

```
oilSystem/
├── backend/               # 后端代码
│   ├── models/           # 数据模型
│   ├── services/         # 业务逻辑（4个业务界面）
│   ├── utils/            # 工具函数
│   └── app.py            # Flask应用
├── frontend/             # 前端代码
│   ├── templates/        # HTML模板
│   └── static/js/        # JavaScript
├── data/
│   ├── input/            # 输入数据（放置Excel文件）
│   └── output/           # 输出结果（自动生成）
├── example_usage.py      # 使用示例
├── install.sh            # 安装脚本
├── start.sh              # 启动脚本
├── README.md             # 项目说明
├── USER_GUIDE.md         # 详细使用指南
└── PROJECT_SUMMARY.md    # 项目总结
```

---

## 📊 数据表说明

### A2数据表

油田单井的单月生产数据表。

**必需字段**：
- 井号（唯一标识）
- 大油田
- 单元
- 年月（6位数字，如202309）
- 月产油量(t)
- 月产水量(m3)
- 月产气量(10^4m3)

**命名规范**：`a2-YYYYMM.xlsx`

### SEC数据表

包含SEC归属关系的评估数据表。

**必需字段**：
- 井号
- SEC油田
- SEC单元
- 是否参评（"是"/"否"）
- 页岩油/常规

**命名规范**：`SEC数据表-YYYYMM.xlsx`

### 评估数据表

用于绘制评估曲线的连续数据表。

**必需字段**：
- 油气田
- 评估单元
- 生产时间年
- 生产时间月
- 油、气、水产量
- 油井开井数

---

## 🔧 常用命令

### 安装依赖
```bash
pip3 install -r requirements.txt
```

### 运行示例
```bash
python3 example_usage.py
```

### 启动服务
```bash
python3 backend/app.py
```

### 生成示例数据
在Python中：
```python
from example_usage import create_sample_data
create_sample_data()
```

---

## 💡 快速技巧

### 1. 批量上传文件

可以在 `data/input/` 目录放置多个文件，通过API批量处理：

```python
import os
from backend.utils.data_io import DataImportExport

input_dir = "data/input"
files = [f for f in os.listdir(input_dir) if f.endswith('.xlsx')]

for file in files:
    df = DataImportExport.read_excel(os.path.join(input_dir, file))
    # 处理数据...
```

### 2. 快速查看数据

```python
import pandas as pd

# 读取并预览
df = pd.read_excel("data/input/a2-202409.xlsx")
print(df.head())
print(df.info())
```

### 3. 导出多种格式

```python
# 导出CSV
df.to_csv("output.csv", index=False, encoding='utf-8-sig')

# 导出Excel多个sheet
with pd.ExcelWriter("output.xlsx") as writer:
    df1.to_excel(writer, sheet_name="Sheet1")
    df2.to_excel(writer, sheet_name="Sheet2")
```

---

## ❓ 常见问题

### Q1: 提示"ModuleNotFoundError: No module named 'pandas'"

**解决**：运行 `pip3 install -r requirements.txt` 安装依赖

### Q2: Web界面功能显示"功能开发中"

**解决**：这是前端提示，实际功能已在后端实现。可以直接使用Python API，或参考 `backend/app.py` 中的接口实现前端调用。

### Q3: 文件上传后找不到

**解决**：文件会保存在 `data/input/` 目录，检查该目录权限

### Q4: 处理大文件很慢

**解决**：
- 建议单次处理不超过10万条记录
- 可以分批处理后合并结果
- 使用服务器模式而非调试模式运行Flask

---

## 📖 进一步学习

- 📘 [用户指南](USER_GUIDE.md) - 详细的使用说明
- 📙 [项目总结](PROJECT_SUMMARY.md) - 系统架构和技术实现
- 📗 [README](README.md) - 项目概述

---

## 🎯 下一步

1. ✅ 熟悉4个业务界面的功能
2. ✅ 准备自己的数据文件
3. ✅ 根据实际需求调整代码
4. ✅ 参考示例代码实现自动化流程

---

## 📞 技术支持

如有问题，请：
1. 查看 [USER_GUIDE.md](USER_GUIDE.md) 中的常见问题
2. 检查 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) 了解系统设计
3. 参考 [example_usage.py](example_usage.py) 中的示例代码

---

**祝使用愉快！** 🎉
