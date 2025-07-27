"""
图结构检索模块

基于知识图谱的多跳推理检索系统
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from abc import ABC, abstractmethod
from dataclasses import dataclass
import json

from ..utils.logger import get_logger


@dataclass
class Entity:
    """实体类"""
    id: str
    name: str
    entity_type: str
    properties: Dict[str, Any]
    
    def __hash__(self):
        return hash(self.id)


@dataclass
class Relation:
    """关系类"""
    id: str
    source_id: str
    target_id: str
    relation_type: str
    properties: Dict[str, Any]
    weight: float = 1.0


@dataclass
class GraphNode:
    """图节点"""
    entity: Entity
    neighbors: List["GraphNode"]
    
    def __hash__(self):
        return hash(self.entity.id)


class KnowledgeGraph:
    """知识图谱类"""
    
    def __init__(self):
        """初始化知识图谱"""
        self.entities: Dict[str, Entity] = {}
        self.relations: List[Relation] = []
        self.adjacency: Dict[str, List[str]] = {}  # 邻接表
    
    def add_entity(self, entity: Entity) -> None:
        """添加实体
        
        Args:
            entity: 实体对象
        """
        self.entities[entity.id] = entity
        if entity.id not in self.adjacency:
            self.adjacency[entity.id] = []
    
    def add_relation(self, relation: Relation) -> None:
        """添加关系
        
        Args:
            relation: 关系对象
        """
        self.relations.append(relation)
        
        # 更新邻接表
        if relation.source_id not in self.adjacency:
            self.adjacency[relation.source_id] = []
        if relation.target_id not in self.adjacency:
            self.adjacency[relation.target_id] = []
        
        self.adjacency[relation.source_id].append(relation.target_id)
    
    def get_neighbors(self, entity_id: str) -> List[Entity]:
        """获取实体的邻居
        
        Args:
            entity_id: 实体ID
            
        Returns:
            邻居实体列表
        """
        neighbor_ids = self.adjacency.get(entity_id, [])
        return [self.entities[nid] for nid in neighbor_ids if nid in self.entities]
    
    def find_path(self, start_id: str, end_id: str, max_depth: int = 3) -> List[List[str]]:
        """查找两个实体间的路径
        
        Args:
            start_id: 起始实体ID
            end_id: 目标实体ID
            max_depth: 最大搜索深度
            
        Returns:
            路径列表
        """
        # TODO: 实现路径搜索算法（BFS/DFS）
        paths = []
        visited = set()
        
        def dfs(current_id: str, target_id: str, path: List[str], depth: int):
            if depth > max_depth:
                return
            
            if current_id == target_id:
                paths.append(path.copy())
                return
            
            if current_id in visited:
                return
            
            visited.add(current_id)
            
            for neighbor_id in self.adjacency.get(current_id, []):
                path.append(neighbor_id)
                dfs(neighbor_id, target_id, path, depth + 1)
                path.pop()
            
            visited.remove(current_id)
        
        dfs(start_id, end_id, [start_id], 0)
        return paths


class GraphRetriever(ABC):
    """图检索器基类"""
    
    @abstractmethod
    def retrieve(self, query: str, entities: List[str], **kwargs) -> List[Dict[str, Any]]:
        """检索相关知识"""
        pass
    
    @abstractmethod
    def multi_hop_retrieve(self, start_entities: List[str], max_hops: int = 2) -> List[Dict[str, Any]]:
        """多跳检索"""
        pass


class Neo4jGraphRetriever(GraphRetriever):
    """Neo4j图数据库检索器"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化Neo4j检索器
        
        Args:
            config: 配置字典
        """
        self.logger = get_logger(__name__)
        self.config = config
        
        # 连接配置
        self.uri = config.get("uri", "bolt://localhost:7687")
        self.username = config.get("username", "neo4j")
        self.password = config.get("password", "password")
        
        # 初始化驱动
        self.driver = None
        self._init_driver()
        
        self.logger.info("Neo4j图检索器初始化完成")
    
    def _init_driver(self) -> None:
        """初始化Neo4j驱动"""
        # TODO: 实现Neo4j连接
        try:
            from neo4j import GraphDatabase
            
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )
            
            # 测试连接
            with self.driver.session() as session:
                session.run("RETURN 1")
            
        except ImportError:
            self.logger.error("Neo4j驱动未安装，请安装: pip install neo4j")
            raise
        except Exception as e:
            self.logger.error(f"Neo4j连接失败: {e}")
            raise
    
    def retrieve(self, query: str, entities: List[str], **kwargs) -> List[Dict[str, Any]]:
        """检索相关知识
        
        Args:
            query: 查询文本
            entities: 相关实体列表
            **kwargs: 额外参数
            
        Returns:
            检索结果列表
        """
        # TODO: 实现基于实体的知识检索
        try:
            with self.driver.session() as session:
                # 构建查询语句
                cypher_query = self._build_retrieval_query(entities, **kwargs)
                
                # 执行查询
                result = session.run(cypher_query, entities=entities)
                
                # 处理结果
                results = []
                for record in result:
                    results.append(dict(record))
                
                self.logger.info(f"图检索到 {len(results)} 条记录")
                return results
                
        except Exception as e:
            self.logger.error(f"图检索失败: {e}")
            return []
    
    def multi_hop_retrieve(
        self,
        start_entities: List[str],
        max_hops: int = 2,
        relation_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """多跳检索
        
        Args:
            start_entities: 起始实体列表
            max_hops: 最大跳数
            relation_types: 关系类型过滤
            
        Returns:
            多跳检索结果
        """
        # TODO: 实现多跳推理检索
        try:
            with self.driver.session() as session:
                # 构建多跳查询
                cypher_query = self._build_multi_hop_query(max_hops, relation_types)
                
                # 执行查询
                result = session.run(
                    cypher_query,
                    start_entities=start_entities,
                    max_hops=max_hops
                )
                
                # 处理结果
                results = []
                for record in result:
                    results.append(dict(record))
                
                self.logger.info(f"多跳检索到 {len(results)} 条路径")
                return results
                
        except Exception as e:
            self.logger.error(f"多跳检索失败: {e}")
            return []
    
    def _build_retrieval_query(self, entities: List[str], **kwargs) -> str:
        """构建检索查询语句
        
        Args:
            entities: 实体列表
            **kwargs: 额外参数
            
        Returns:
            Cypher查询语句
        """
        # TODO: 构建动态Cypher查询
        limit = kwargs.get("limit", 10)
        
        query = f"""
        MATCH (e:Entity)-[r]->(related:Entity)
        WHERE e.name IN $entities
        RETURN e, r, related
        LIMIT {limit}
        """
        
        return query
    
    def _build_multi_hop_query(
        self,
        max_hops: int,
        relation_types: Optional[List[str]] = None
    ) -> str:
        """构建多跳查询语句
        
        Args:
            max_hops: 最大跳数
            relation_types: 关系类型
            
        Returns:
            Cypher查询语句
        """
        # TODO: 构建多跳Cypher查询
        relation_filter = ""
        if relation_types:
            relation_filter = f":{':'.join(relation_types)}"
        
        query = f"""
        MATCH path = (start:Entity)-[{relation_filter}*1..{max_hops}]->(end:Entity)
        WHERE start.name IN $start_entities
        RETURN path, start, end, length(path) as hop_count
        ORDER BY hop_count
        """
        
        return query
    
    def close(self) -> None:
        """关闭连接"""
        if self.driver:
            self.driver.close()


class InMemoryGraphRetriever(GraphRetriever):
    """内存图检索器
    
    用于小规模知识图谱的内存检索
    """
    
    def __init__(self, config: Dict[str, Any]):
        """初始化内存图检索器
        
        Args:
            config: 配置字典
        """
        self.logger = get_logger(__name__)
        self.config = config
        self.knowledge_graph = KnowledgeGraph()
        
        # 加载知识图谱数据
        if "graph_data_path" in config:
            self._load_graph_data(config["graph_data_path"])
        
        self.logger.info("内存图检索器初始化完成")
    
    def _load_graph_data(self, data_path: str) -> None:
        """加载图数据
        
        Args:
            data_path: 数据文件路径
        """
        # TODO: 从文件加载图数据
        try:
            import json
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 加载实体
            for entity_data in data.get("entities", []):
                entity = Entity(
                    id=entity_data["id"],
                    name=entity_data["name"],
                    entity_type=entity_data["type"],
                    properties=entity_data.get("properties", {})
                )
                self.knowledge_graph.add_entity(entity)
            
            # 加载关系
            for relation_data in data.get("relations", []):
                relation = Relation(
                    id=relation_data["id"],
                    source_id=relation_data["source"],
                    target_id=relation_data["target"],
                    relation_type=relation_data["type"],
                    properties=relation_data.get("properties", {}),
                    weight=relation_data.get("weight", 1.0)
                )
                self.knowledge_graph.add_relation(relation)
            
            self.logger.info(f"加载了 {len(self.knowledge_graph.entities)} 个实体和 {len(self.knowledge_graph.relations)} 个关系")
            
        except Exception as e:
            self.logger.error(f"加载图数据失败: {e}")
    
    def retrieve(self, query: str, entities: List[str], **kwargs) -> List[Dict[str, Any]]:
        """检索相关知识
        
        Args:
            query: 查询文本
            entities: 相关实体列表
            **kwargs: 额外参数
            
        Returns:
            检索结果列表
        """
        # TODO: 实现内存图检索
        results = []
        
        for entity_name in entities:
            # 查找实体
            entity = self._find_entity_by_name(entity_name)
            if not entity:
                continue
            
            # 获取邻居实体和关系
            neighbors = self.knowledge_graph.get_neighbors(entity.id)
            
            for neighbor in neighbors:
                result = {
                    "source_entity": entity.name,
                    "target_entity": neighbor.name,
                    "relation": self._get_relation_between(entity.id, neighbor.id),
                    "properties": neighbor.properties
                }
                results.append(result)
        
        return results
    
    def multi_hop_retrieve(self, start_entities: List[str], max_hops: int = 2) -> List[Dict[str, Any]]:
        """多跳检索
        
        Args:
            start_entities: 起始实体列表
            max_hops: 最大跳数
            
        Returns:
            多跳检索结果
        """
        # TODO: 实现多跳检索
        results = []
        
        for entity_name in start_entities:
            entity = self._find_entity_by_name(entity_name)
            if not entity:
                continue
            
            # 查找多跳路径
            paths = self._find_multi_hop_paths(entity.id, max_hops)
            
            for path in paths:
                result = {
                    "start_entity": entity.name,
                    "path": path,
                    "hop_count": len(path) - 1
                }
                results.append(result)
        
        return results
    
    def _find_entity_by_name(self, name: str) -> Optional[Entity]:
        """根据名称查找实体
        
        Args:
            name: 实体名称
            
        Returns:
            实体对象或None
        """
        for entity in self.knowledge_graph.entities.values():
            if entity.name == name:
                return entity
        return None
    
    def _get_relation_between(self, source_id: str, target_id: str) -> Optional[str]:
        """获取两个实体间的关系
        
        Args:
            source_id: 源实体ID
            target_id: 目标实体ID
            
        Returns:
            关系类型或None
        """
        for relation in self.knowledge_graph.relations:
            if relation.source_id == source_id and relation.target_id == target_id:
                return relation.relation_type
        return None
    
    def _find_multi_hop_paths(self, start_id: str, max_hops: int) -> List[List[str]]:
        """查找多跳路径
        
        Args:
            start_id: 起始实体ID
            max_hops: 最大跳数
            
        Returns:
            路径列表
        """
        # TODO: 实现路径搜索
        paths = []
        visited = set()
        
        def dfs(current_id: str, path: List[str], depth: int):
            if depth >= max_hops:
                return
            
            if current_id in visited:
                return
            
            visited.add(current_id)
            
            for neighbor_id in self.knowledge_graph.adjacency.get(current_id, []):
                new_path = path + [neighbor_id]
                paths.append(new_path)
                dfs(neighbor_id, new_path, depth + 1)
            
            visited.remove(current_id)
        
        dfs(start_id, [start_id], 0)
        return paths


class GraphRetrieverFactory:
    """图检索器工厂"""
    
    @staticmethod
    def create_retriever(retriever_type: str, config: Dict[str, Any]) -> GraphRetriever:
        """创建图检索器
        
        Args:
            retriever_type: 检索器类型
            config: 配置字典
            
        Returns:
            图检索器实例
        """
        if retriever_type.lower() == "neo4j":
            return Neo4jGraphRetriever(config)
        elif retriever_type.lower() == "memory":
            return InMemoryGraphRetriever(config)
        else:
            raise ValueError(f"不支持的图检索器类型: {retriever_type}")
