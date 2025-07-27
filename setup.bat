@echo off
echo 正在启动 Agent-LuoTianyi 项目...

:: 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

:: 检查是否存在虚拟环境
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
)

:: 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

:: 安装依赖
echo 安装项目依赖...
pip install -r requirements.txt

:: 检查配置文件
if not exist config\config.yaml (
    echo 复制配置模板...
    copy config\config.yaml.template config\config.yaml
    echo 请编辑 config\config.yaml 文件配置您的API密钥
)

if not exist .env (
    echo 复制环境变量模板...
    copy .env.template .env
    echo 请编辑 .env 文件配置您的API密钥
)

:: 创建必要目录
if not exist logs mkdir logs
if not exist data\knowledge mkdir data\knowledge
if not exist data\models mkdir data\models

echo.
echo 项目启动完成！
echo.
echo 使用说明：
echo 1. 编辑 config\config.yaml 配置文件
echo 2. 编辑 .env 环境变量文件或手动配置环境变量
echo 3. 运行 python examples\chat_demo.py 开始对话
echo 4. 运行 python examples\web_demo.py 启动Web界面
echo.
pause
