# 开发指南

## 项目开发环境设置

### 1. 环境准备

#### Python环境
确保Python版本在3.8及以上：
```bash
python --version
```
目前开发版本为3.10，因此模块的可用性仅在3.10及以上版本得到保证。

#### 虚拟环境（推荐）
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```
也可以使用conda环境：
```bash

# 创建conda环境
conda create -n venv python=3.8

# 激活conda环境
conda activate venv
```


### 2. 依赖安装

```bash
# 安装基础依赖
pip install -r requirements.txt

# 开发工具（可选）
pip install -r requirements-dev.txt
```

### 3. 环境变量配置

创建 `.env` 文件：
```bash
# 复制环境变量模板
cp .env.template .env
```

在 `.env` 文件中配置：
```env
SILICONFLOW_API_KEY=your_siliconflow_api_key_here
NEO4J_PASSWORD=your_neo4j_password_here
```

对于Windows用户，建议使用PowerShell或Git Bash来运行命令行操作，以避免路径问题。使用如下方案配置环境变量：
1. 搜索编辑系统环境变量；
2. 在跳出的窗口中点击“环境变量”；
3. 如果仅需要为当前用户配置，则在“用户变量”中点击“新建”，输入变量名和变量值。反之，如果需要为所有用户配置，则在“系统变量”中点击“新建”，输入变量名和变量值；
   - 变量名：`SILICONFLOW_API_KEY`，变量值为自己的API KEY；
   - 变量名：`NEO4J_PASSWORD`，变量值为自己的Neo4j密码；
4. 点击“确定”保存。
5. 重启命令行窗口（可能需要重启vscode）以使环境变量生效。
6. 在命令行中使用 `echo $SILICONFLOW_API_KEY` 和 `echo $NEO4J_PASSWORD` 来验证环境变量是否设置成功。

## 核心架构说明

### 模块划分

1. **agents/**: Agent核心逻辑
   - `luotianyi_agent.py`: 主Agent类
   - `conversation_manager.py`: 对话管理

2. **knowledge/**: 知识管理系统
   - `graph_retriever.py`: 图结构检索
   - `vector_store.py`: 向量数据库操作
   - `knowledge_builder.py`: 知识库构建

3. **llm/**: 大模型接口
   - `siliconflow_client.py`: 硅基流动API客户端
   - `prompt_manager.py`: Prompt模板管理

### 关键设计模式

#### 1. 策略模式 - LLM提供商
```python
class LLMProvider(ABC):
    @abstractmethod
    def chat(self, messages: List[Dict]) -> str:
        pass

class SiliconFlowProvider(LLMProvider):
    def chat(self, messages: List[Dict]) -> str:
        # 具体实现
        pass
```

#### 2. 装饰器模式 - 功能增强
```python
def with_persona(func):
    def wrapper(*args, **kwargs):
        # 注入人设信息
        result = func(*args, **kwargs)
        return apply_persona(result)
    return wrapper
```

#### 3. 观察者模式 - 事件处理
```python
class ConversationEvent:
    def notify_observers(self, event_type: str, data: Dict):
        # 通知所有观察者
        pass
```

## 开发工作流

### 1. 代码规范

#### 格式化
```bash
# 使用Black格式化代码
black src/ tests/

# 检查代码风格
flake8 src/ tests/
```

#### 类型检查
```bash
# 使用mypy进行类型检查
mypy src/
```

### 2. 测试

#### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_agent.py

# 生成覆盖率报告
pytest --cov=src tests/
```

#### 测试编写规范
```python
def test_agent_basic_response():
    """测试Agent基础回复功能"""
    agent = LuoTianyiAgent()
    response = agent.chat("你好")
    
    assert response is not None
    assert len(response) > 0
    assert "洛天依" in response or "天依" in response
```

### 3. 提交规范

#### Commit Message格式
```
<type>(<scope>): <description>

<body>

<footer>
```

类型说明：
- `feat`: 新功能
- `fix`: 问题修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(agent): 添加多轮对话记忆功能

- 实现基于滑动窗口的对话历史管理
- 支持自定义记忆长度配置
- 优化上下文相关性检索

Closes #123
```

## 扩展开发

### 1. 添加新的知识源

#### 步骤
1. 在 `data/knowledge_base/` 创建新的数据文件
2. 实现对应的知识加载器
3. 更新知识图谱构建脚本
4. 重新构建向量索引

#### 示例
```python
class CustomKnowledgeLoader:
    def load_data(self, file_path: str) -> List[Document]:
        # 加载自定义格式的知识数据
        pass
    
    def extract_entities(self, text: str) -> List[Entity]:
        # 提取实体信息
        pass
```

### 2. 集成新的LLM提供商

#### 步骤
1. 继承 `LLMProvider` 基类
2. 实现 `chat()` 方法
3. 在配置文件中添加相应配置
4. 更新 `LLMFactory` 类

#### 示例
```python
class NewLLMProvider(LLMProvider):
    def __init__(self, config: Dict):
        self.config = config
    
    def chat(self, messages: List[Dict]) -> str:
        # 实现与新LLM的交互逻辑
        pass
```

### 3. 多模态功能扩展

#### TTS集成
```python
class TTSEngine:
    def synthesize(self, text: str, voice_config: Dict) -> bytes:
        # 语音合成逻辑
        pass
```

#### Live2D集成
```python
class Live2DController:
    def trigger_action(self, emotion: str, intensity: float):
        # 触发相应的Live2D动作
        pass
```

## 调试技巧

### 1. 日志配置
```python
from loguru import logger

# 添加详细的调试日志
logger.add("debug.log", level="DEBUG", rotation="10 MB")

# 在关键位置添加日志
logger.info(f"用户输入: {user_input}")
logger.debug(f"检索到的知识: {retrieved_docs}")
```

### 2. 性能分析
```python
import cProfile
import pstats

# 分析Agent性能
profiler = cProfile.Profile()
profiler.enable()

# 运行Agent
agent.chat("测试消息")

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative').print_stats(10)
```

### 3. 内存监控
```python
import psutil
import os

def monitor_memory():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"内存使用: {memory_info.rss / 1024 / 1024:.2f} MB")
```

## 部署指南

### 1. 容器化部署

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "src/main.py"]
```

#### Docker Compose
```yaml
version: '3.8'
services:
  agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SILICONFLOW_API_KEY=${SILICONFLOW_API_KEY}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
```

### 2. 生产环境配置

#### 性能优化
- 使用多进程/多线程
- 配置连接池
- 启用缓存机制
- 实现负载均衡

#### 监控告警
- 集成Prometheus监控
- 配置健康检查
- 设置错误告警
- 记录关键指标

## 常见问题

### Q: 如何处理API限流？
A: 实现指数退避重试机制，并配置合适的请求频率限制。

### Q: 向量数据库性能优化？
A: 选择合适的嵌入维度，定期清理无用向量，使用近似搜索算法。

### Q: 如何保证角色一致性？
A: 强化Prompt工程，建立评估指标，使用强化学习微调。

## 贡献代码

1. Fork项目仓库
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 创建Pull Request

感谢您的贡献！🎵
