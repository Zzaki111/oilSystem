#!/bin/bash

# 快速安装和测试脚本

echo "======================================"
echo "石油数据预处理系统 - 快速安装"
echo "======================================"
echo ""

# 安装依赖
echo "正在安装Python依赖..."
pip3 install pandas openpyxl numpy flask flask-cors python-dateutil xlrd

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ 依赖安装成功！"
    echo ""
    
    # 运行示例
    echo "======================================"
    echo "运行示例代码..."
    echo "======================================"
    echo ""
    
    python3 example_usage.py
    
    echo ""
    echo "======================================"
    echo "安装和测试完成！"
    echo "======================================"
    echo ""
    echo "接下来你可以："
    echo "1. 运行 ./start.sh 启动Web服务"
    echo "2. 在浏览器访问 http://localhost:5000"
    echo "3. 参考 USER_GUIDE.md 了解详细使用方法"
    echo ""
else
    echo ""
    echo "✗ 依赖安装失败，请检查错误信息"
    exit 1
fi
