# Agent-LuoTianyi：虚拟歌手洛天依对话Agent

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/🦜️🔗-LangChain-brightgreen)](https://langchain.readthedocs.io/)

## 🎵 项目介绍

本项目旨在设计并实现一个具备角色扮演能力的虚拟歌手洛天依（Luo Tianyi）智能对话Agent。该Agent基于**图结构增强RAG**架构，使用**LangChain**框架构建，集成**硅基流动平台**的大模型接口，为用户提供沉浸式的洛天依互动体验。

### ✨ 核心特性

- 🤖 **智能对话**：基于图结构增强RAG的自然语言交互
- 🎭 **角色一致性**：符合洛天依官方设定的人格化表达
- 📚 **知识库驱动**：可维护的洛天依专属知识体系
- 🎼 **多模态扩展**：支持语音合成（GPT-SoVITS）和Live2D动作
- 🔧 **模块化设计**：易于扩展和维护的组件化架构
- 🚀 **灵活部署**：支持本地和云端部署方案目文档：虚拟歌手洛天依角色扮演Agent设计
## 一、项目目的
本项目旨在设计并实现一个具备角色扮演能力的虚拟歌手洛天依（Luo Tianyi）智能对话Agent。该Agent将被部署于本地或云端，能够与用户进行自然语言交互，响应内容需体现洛天依的已有知识背景（如代表歌曲、演出信息、官方设定等）与其拟定性格特征（如活泼、可爱、有亲和力等）。项目最终目标是实现一个具备“人格化表达”和“知识一致性”的互动系统，提升用户的沉浸式体验。

## 📋 项目要求

### 功能需求
1. **对话能力**：与用户进行自然语言聊天，回答问题、回应情感表达、参与轻松互动
2. **人物设定一致性**：
   - 语气风格符合洛天依官方形象（亲切、年轻、略带调皮）
   - 回答内容体现洛天依相关的事实性内容（歌曲、演出、合作、形象设定等）
3. **知识可控**：基于可维护的知识库，支持知识更新和个性化微调
4. **模块化设计**：清晰分离各功能模块，便于后续升级和调优
5. **可部署性**：支持本地或服务器端独立部署

### 技术需求
- 基于LangChain框架的图结构增强RAG系统
- 集成硅基流动平台大模型API
- 支持向量数据库进行知识检索
- 预留GPT-SoVITS语音合成接口
- 预留Live2D动作生成接口

## 🏗️ 系统架构

### 整体架构
采用**图结构增强RAG**的三阶段处理流程：

```
用户输入 ──▶ 意图理解 ──▶ 图结构检索 ──▶ 语言模型生成 ──▶ 多模态输出
    │            │            │              │              │
  文本/语音    意图分类     知识图谱        LLM生成      文本/语音/动作
```

### 核心模块

#### 🧠 模块A：对话理解与意图识别
- **功能**：用户输入预处理、意图分类、实体识别
- **技术栈**：LangChain + NLP预处理
- **输入**：用户文本/语音输入
- **输出**：结构化意图和实体信息

#### 📚 模块B：图结构知识检索
- **功能**：基于知识图谱的多跳推理检索
- **技术栈**：向量数据库 + 图数据库 + LangChain检索链
- **知识内容**：
  - 洛天依官方设定和人物背景
  - 代表歌曲、专辑和歌词信息
  - 演出记录和合作信息
  - 粉丝互动和社交媒体内容
- **输出**：相关知识片段和关联信息

#### 🎭 模块C：角色化响应生成
- **功能**：基于检索结果生成洛天依风格回复
- **技术栈**：硅基流动平台LLM + LangChain生成链
- **特性**：
  - 角色设定注入
  - 风格一致性保持
  - 上下文记忆管理
- **输出**：角色化文本回复

#### 🎵 模块D：多模态输出（扩展）
- **语音合成**：GPT-SoVITS生成洛天依音色
- **动作生成**：Live2D模型动作驱动
- **表情控制**：情感识别与表情映射

## 🛠️ 技术栈

### 核心依赖
- **LangChain**: 大模型应用开发框架
- **硅基流动平台**: 大模型API服务
- **Vector Database**: 向量检索（Chroma/Pinecone）
- **Graph Database**: 知识图谱存储（Neo4j/ArangoDB）

### 扩展组件
- **GPT-SoVITS**: 语音克隆与合成
- **Live2D**: 虚拟形象动作生成
- **FastAPI**: Web服务框架
- **Streamlit**: 交互界面（可选）

## 📁 项目结构

```
Agent-LuoTianyi/
├── README.md                 # 项目文档
├── LICENSE                   # MIT许可证
├── requirements.txt          # Python依赖
├── config/                   # 配置文件
│   ├── config.yaml          # 主配置文件
│   ├── persona.yaml         # 洛天依人设配置
│   └── prompts/             # Prompt模板
├── src/                     # 源代码
│   ├── __init__.py
│   ├── agents/              # Agent核心逻辑
│   │   ├── __init__.py
│   │   ├── luotianyi_agent.py
│   │   └── conversation_manager.py
│   ├── knowledge/           # 知识管理
│   │   ├── __init__.py
│   │   ├── graph_retriever.py
│   │   ├── vector_store.py
│   │   └── knowledge_builder.py
│   ├── llm/                 # 大模型接口
│   │   ├── __init__.py
│   │   ├── siliconflow_client.py
│   │   └── prompt_manager.py
│   ├── multimodal/          # 多模态扩展
│   │   ├── __init__.py
│   │   ├── tts_engine.py
│   │   └── live2d_controller.py
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── logger.py
│       └── helpers.py
├── data/                    # 数据文件
│   ├── knowledge_base/      # 知识库文件
│   ├── embeddings/          # 向量嵌入
│   └── personas/            # 人设数据
├── tests/                   # 测试代码
│   ├── __init__.py
│   ├── test_agent.py
│   └── test_knowledge.py
├── scripts/                 # 脚本工具
│   ├── setup_knowledge.py  # 知识库初始化
│   ├── train_embeddings.py # 向量训练
│   └── deploy.py            # 部署脚本
├── docs/                    # 详细文档
│   ├── api.md               # API文档
│   ├── deployment.md        # 部署指南
│   └── development.md       # 开发指南
└── examples/                # 使用示例
    ├── basic_chat.py        # 基础对话示例
    ├── web_interface.py     # Web界面示例
    └── multimodal_demo.py   # 多模态演示
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- 硅基流动平台API密钥
- 内存：至少 4GB RAM
- 存储：至少 2GB 可用空间

### 快速启动

**Windows用户：**
```cmd
# 双击运行快速启动脚本
setup.bat
```

**Linux/Mac用户：**
```bash
# 运行快速启动脚本
chmod +x setup.sh
./setup.sh
```

### 手动安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/Agent-LuoTianyi.git
cd Agent-LuoTianyi
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
# 复制模板文件
cp .env.template .env
cp config/config.yaml.template config/config.yaml

# 编辑配置文件，填入您的API密钥
```

5. **运行示例**
```bash
# 命令行聊天演示
python examples/chat_demo.py

# Web界面演示
python examples/web_demo.py

# 知识库构建演示
python examples/knowledge_demo.py
```

### Docker部署

```bash
# 使用Docker Compose快速部署
docker-compose up -d

# 或单独构建镜像
docker build -t agent-luotianyi .
docker run -p 8000:8000 agent-luotianyi
```

### 基础使用

```python
from src.agents.luotianyi_agent import LuoTianyiAgent

# 初始化Agent
agent = LuoTianyiAgent()

# 开始对话
response = agent.chat("你好，洛天依！")
print(response)
```

## 🔧 配置说明

### 主配置文件 (`config/config.yaml`)
```yaml
# 大模型配置
llm:
  provider: "siliconflow"
  model: "deepseek-chat"
  api_key: "${SILICONFLOW_API_KEY}"
  temperature: 0.7

# 知识库配置
knowledge:
  vector_store: "chroma"
  graph_store: "neo4j"
  embedding_model: "text-embedding-3-small"

# Agent配置
agent:
  persona_file: "config/persona.yaml"
  memory_size: 10
  response_max_tokens: 500
```

### 人设配置 (`config/persona.yaml`)
```yaml
name: "洛天依"
personality:
  traits: ["活泼", "可爱", "有亲和力", "略带调皮"]
  speaking_style: "亲切自然，偶尔使用可爱的语气词"
  
background:
  - "Vocaloid虚拟歌手"
  - "代表色为灰绿色"
  - "喜欢唱歌和与粉丝互动"
  
favorite_songs:
  - "普通DISCO"
  - "权御天下"
  - "九九八十一"
```

## 🧪 开发指南

### 添加新的知识内容
1. 在 `data/knowledge_base/` 中添加结构化数据
2. 运行 `python scripts/setup_knowledge.py` 重建索引
3. 测试新知识的检索效果

### 扩展多模态功能
1. 实现 `src/multimodal/` 中的接口
2. 在配置文件中启用相应模块
3. 参考 `examples/multimodal_demo.py` 进行测试

### 自定义Prompt模板
在 `config/prompts/` 中添加新的模板文件，并在代码中引用。

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### 代码规范
- 使用 Black 进行代码格式化
- 遵循 PEP 8 编码规范
- 添加必要的测试用例
- 更新相关文档

## 📜 许可证

本项目基于 [MIT 许可证](LICENSE) 开源。

## 🙏 致谢

- 感谢洛天依官方提供的角色设定
- 感谢LangChain社区的技术支持
- 感谢硅基流动平台提供的API服务
- 感谢所有贡献者的努力

## 📞 联系方式

- 项目地址：[GitHub Repository](https://github.com/SheepLiu712/Agent-LuoTianyi)
- 问题反馈：[Issues](https://github.com/SheepLiu712/Agent-LuoTianyi/issues)
- 讨论交流：[Discussions](https://github.com/SheepLiu712/Agent-LuoTianyi/discussions)

---

🎵 *"大家好，我是洛天依！让我们一起开始愉快的对话吧～"* 🎵
