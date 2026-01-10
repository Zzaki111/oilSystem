#!/bin/bash

# 石油生产数据预处理系统 - 快速启动脚本

echo "=================================================="
echo "🛢️  石油生产数据预处理系统"
echo "=================================================="
echo ""

# 检查Python环境
echo "📦 检查Python环境..."
if ! command -v python &> /dev/null
then
    echo "❌ 未找到Python，请先安装Python 3.8+"
    exit 1
fi

python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✅ Python版本: $python_version"
echo ""

# 检查依赖
echo "📦 检查依赖包..."
required_packages=("flask" "pandas" "openpyxl" "flask-cors")
missing_packages=()

for package in "${required_packages[@]}"; do
    if ! python -c "import $package" 2>/dev/null; then
        missing_packages+=("$package")
    fi
done

if [ ${#missing_packages[@]} -gt 0 ]; then
    echo "⚠️  缺少以下依赖包: ${missing_packages[*]}"
    echo "📥 正在安装..."
    pip install "${missing_packages[@]}"
    echo ""
fi

echo "✅ 所有依赖已就绪"
echo ""

# 启动服务
echo "🚀 启动Flask服务..."
echo "📍 服务地址: http://localhost:5001"
echo "📌 按Ctrl+C停止服务"
echo ""
echo "=================================================="
echo ""

cd "$(dirname "$0")/backend"
python app.py
