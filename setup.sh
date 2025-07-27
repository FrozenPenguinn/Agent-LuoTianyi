#!/bin/bash

echo "正在启动 Agent-LuoTianyi 项目..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查是否存在虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装项目依赖..."
pip install -r requirements.txt

# 检查配置文件
if [ ! -f "config/config.yaml" ]; then
    echo "复制配置模板..."
    cp config/config.yaml.template config/config.yaml
    echo "请编辑 config/config.yaml 文件配置您的API密钥"
fi

if [ ! -f ".env" ]; then
    echo "复制环境变量模板..."
    cp .env.template .env
    echo "请编辑 .env 文件配置您的API密钥"
fi

# 创建必要目录
mkdir -p logs
mkdir -p data/knowledge
mkdir -p data/models

echo ""
echo "项目启动完成！"
echo ""
echo "使用说明："
echo "1. 编辑 config/config.yaml 配置文件"
echo "2. 编辑 .env 环境变量文件"
echo "3. 运行 python examples/chat_demo.py 开始对话"
echo "4. 运行 python examples/web_demo.py 启动Web界面"
echo ""
