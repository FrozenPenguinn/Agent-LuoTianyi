"""
硅基流动平台客户端

封装硅基流动API的调用逻辑
"""

from typing import Dict, List, Optional, Any, Iterator
from openai import OpenAI
import os
import time
import random

from ..utils.logger import get_logger


class SiliconFlowClient:
    """硅基流动平台LLM客户端"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化客户端
        
        Args:
            config: 配置字典
        """
        self.logger = get_logger(__name__)
        self.config = config
        
        # 初始化OpenAI客户端
        try:
            self.client = OpenAI(
                base_url=config.get("base_url", "https://api.siliconflow.cn/v1"),
                api_key=config.get("api_key") or os.environ.get("SILICONFLOW_API_KEY")
            )
        except Exception as e:
            self.logger.error(f"初始化硅基流动客户端失败: {e}")
            raise Exception(f"无法初始化硅基流动客户端: {e}")
        
        # 模型配置
        self.model = config.get("model", "deepseek-ai/DeepSeek-V2.5")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 1000)
        self.top_p = config.get("top_p", 0.9)
        
        # 重试配置
        self.max_retries = config.get("max_retries", 3)
        self.retry_delay = config.get("retry_delay", 1.0)
        
        self.logger.info(f"硅基流动客户端初始化完成，模型: {self.model}")
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """发送聊天请求
        
        Args:
            messages: 消息列表
            **kwargs: 额外参数
            
        Returns:
            模型回复文本
        """
        try:
            # 合并参数
            params = self._build_params(messages, **kwargs)
            
            # 发送请求
            response = self._send_request(params)
            
            # 提取回复内容
            content = self._extract_content(response)
            
            self.logger.info(f"LLM回复生成成功，长度: {len(content)}")
            return content
            
        except Exception as e:
            self.logger.error(f"LLM请求失败: {e}")
            raise
    
    def chat_stream(self, messages: List[Dict[str, str]], **kwargs) -> Iterator[str]:
        """流式聊天请求
        
        Args:
            messages: 消息列表
            **kwargs: 额外参数
            
        Yields:
            流式回复文本片段
        """
        try:
            # 构建参数
            params = self._build_params(messages, stream=True, **kwargs)
            
            # 发送流式请求
            response = self._send_request(params)
            
            # 逐步返回内容
            for chunk in self._extract_stream_content(response):
                yield chunk
                
        except Exception as e:
            self.logger.error(f"流式LLM请求失败: {e}")
            raise
    
    def _build_params(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """构建请求参数
        
        Args:
            messages: 消息列表
            **kwargs: 额外参数
            
        Returns:
            请求参数字典
        """
        params = {
            "model": kwargs.get("model", self.model),
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "top_p": kwargs.get("top_p", self.top_p),
            "stream": kwargs.get("stream", False)
        }
        
        return params
    
    def _send_request(self, params: Dict[str, Any]) -> Any:
        """发送API请求（带重试）
        
        Args:
            params: 请求参数
            
        Returns:
            API响应
        """
        # TODO: 实现请求发送逻辑
        # - 实现指数退避重试
        # - 处理API限流
        # - 记录请求日志
        
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(**params)
                return response
                
            except Exception as e:
                last_exception = e
                self.logger.warning(f"请求失败 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                
                if attempt < self.max_retries - 1:
                    # 指数退避
                    delay = self.retry_delay * (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(delay)
        
        # 所有重试都失败
        raise last_exception
    
    def _extract_content(self, response: Any) -> str:
        """提取响应内容
        
        Args:
            response: API响应
            
        Returns:
            回复文本
        """
        # TODO: 实现内容提取逻辑
        # - 处理不同类型的响应
        # - 提取文本内容
        # - 处理错误情况
        
        try:
            if hasattr(response, 'choices') and response.choices:
                choice = response.choices[0]
                if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                    return choice.message.content or ""
            
            self.logger.warning("无法从响应中提取内容")
            return ""
            
        except Exception as e:
            self.logger.error(f"提取响应内容失败: {e}")
            return ""
    
    def _extract_stream_content(self, response: Any) -> Iterator[str]:
        """提取流式响应内容
        
        Args:
            response: 流式API响应
            
        Yields:
            文本片段
        """
        # TODO: 实现流式内容提取
        # - 处理流式响应格式
        # - 逐步返回文本片段
        # - 处理连接错误
        
        try:
            for chunk in response:
                if not chunk.choices:
                    continue
                
                choice = chunk.choices[0]
                if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
                    content = choice.delta.content
                    if content:
                        yield content
                        
        except Exception as e:
            self.logger.error(f"提取流式内容失败: {e}")
            raise
    
    def validate_connection(self) -> bool:
        """验证API连接
        
        Returns:
            连接是否正常
        """
        # TODO: 实现连接验证
        # - 发送简单的测试请求
        # - 验证API密钥有效性
        # - 检查模型可用性
        
        try:
            test_messages = [{"role": "user", "content": "test"}]
            response = self.chat(test_messages)
            return True
        except Exception as e:
            self.logger.error(f"连接验证失败: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息
        
        Returns:
            模型信息字典
        """
        # TODO: 实现模型信息获取
        # - 查询模型详细信息
        # - 返回模型能力和限制
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p
        }
