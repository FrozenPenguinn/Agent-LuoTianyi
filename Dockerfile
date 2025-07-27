# Agent-LuoTianyi Docker配置
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY src/ src/
COPY config/ config/
COPY prompts/ prompts/
COPY data/ data/

# 设置环境变量
ENV PYTHONPATH=/app/src

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "examples/web_demo.py"]
