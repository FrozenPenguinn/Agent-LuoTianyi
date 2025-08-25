import os
from typing import List, Tuple, Dict, Any
from abc import ABC, abstractmethod
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document

import requests
from langchain_core.embeddings import Embeddings

class SiliconFlowEmbeddings(Embeddings):
    def __init__(self, model="BAAI/bge-m3", api_key=None, base_url="https://api.siliconflow.cn/v1"):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url

    def embed_documents(self, texts):
        return [self._embed(text) for text in texts]

    def embed_query(self, text):
        return self._embed(text)

    def _embed(self, text):
        url = f"{self.base_url}/embeddings"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"model": self.model, "input": text}
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()["data"][0]["embedding"]



api_key = os.getenv("SILICONFLOW_API_KEY")
# ---------------- 抽象类 ----------------
class VectorStore(ABC):
    """向量存储基类"""
    
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> List[str]:
        """添加文档到向量库"""
        pass
    
    @abstractmethod
    def search(self, query: str, k: int = 5, **kwargs) -> List[Tuple[Document, float]]:
        """搜索相似文档"""
        pass
    
    @abstractmethod
    def delete_documents(self, doc_ids: List[str]) -> bool:
        """删除文档"""
        pass
    
    @abstractmethod
    def update_document(self, doc_id: str, document: Document) -> bool:
        """更新文档"""
        pass


# ---------------- Chroma 实现 ----------------
class MyLogger():
    def __init__(self, name: str):
        self.name = name

    def info(self, msg: str):
        print(f"[INFO] {self.name}: {msg}")

    def error(self, msg: str):
        print(f"[ERROR] {self.name}: {msg}")

class ChromaVectorStore(VectorStore):
    """Chroma向量数据库实现"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化Chroma向量存储
        
        Args:
            config: 配置字典
        """
        self.logger = MyLogger(self.__class__.__name__)
        self.config = config
        
        # 配置参数
        self.persist_directory = config.get("persist_directory", "./data/embeddings")
        self.collection_name = config.get("collection_name", "luotianyi_knowledge")
        self.embedding_model = config.get("embedding_model", "text-embedding-3-small")
        
        # 初始化 Chroma 客户端
        self.client = None
        self.collection = None
        self._init_chroma()
        
        self.logger.info(f"Chroma向量存储初始化完成: {self.collection_name}")
    
    def _init_chroma(self):
        """初始化 Chroma 向量数据库"""
        embeddings = SiliconFlowEmbeddings(
            model = "Qwen/Qwen3-Embedding-8B",
            base_url = "https://api.siliconflow.cn/v1",
            api_key = api_key 
        )
        self.collection = Chroma(
            collection_name=self.collection_name,
            embedding_function=embeddings,
            persist_directory=self.persist_directory,
        )

    def add_documents(self, documents: List[Document]) -> List[str]:
        """添加文档到向量库"""
        ids = [str(hash(doc.page_content)) for doc in documents]
        self.collection.add_documents(documents, ids=ids)
        self.logger.info(f"成功添加 {len(documents)} 条文档")
        return ids

    def search(self, query: str, k: int = 5, **kwargs) -> List[Tuple[Document, float]]:
        """搜索相似文档"""
        results = self.collection.similarity_search_with_score(query, k=k)
        return results  # [(Document, score), ...]

    def delete_documents(self, doc_ids: List[str]) -> bool:
        """删除文档"""
        try:
            self.collection.delete(ids=doc_ids)
            self.logger.info(f"成功删除 {len(doc_ids)} 条文档")
            return True
        except Exception as e:
            self.logger.error(f"删除文档失败: {e}")
            return False

    def update_document(self, doc_id: str, document: Document) -> bool:
        """更新文档（删除+重建）"""
        try:
            self.delete_documents([doc_id])
            self.collection.add_documents([document], ids=[doc_id])
            self.logger.info(f"文档 {doc_id} 更新成功")
            return True
        except Exception as e:
            self.logger.error(f"更新文档失败: {e}")
            return False

if __name__ == "__main__":
    from langchain_core.documents import Document
    
    config = {
        "persist_directory": "./data/chroma_db",
        "collection_name": "luotianyi_knowledge",
        "embedding_model": "text-embedding-3-small"
    }
    
    store = ChromaVectorStore(config)
    
    # 添加文档
    docs = [
        Document(page_content="小笼包是洛天依最喜欢的食物之一"),
        Document(page_content="洛天依是一位虚拟歌手"),
    ]
    ids = store.add_documents(docs)
    
    # 搜索
    results = store.search("洛天依喜欢吃什么？", k=2)
    for doc, score in results:
        print(f"[score={score:.4f}] {doc.page_content}")
    
    # 更新
    store.update_document(ids[0], Document(page_content="洛天依最喜欢吃糖葫芦"))
    
    # 删除
    store.delete_documents(ids)
