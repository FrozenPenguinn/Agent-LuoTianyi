"""
基础对话示例

演示如何使用洛天依Agent进行基础对话
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agents.luotianyi_agent import LuoTianyiAgent
from src.utils.logger import setup_logging, get_logger


def main():
    """主函数"""
    # 设置日志
    setup_logging({
        "level": "INFO",
        "console_output": True,
        "file_output": False
    })
    
    logger = get_logger(__name__)
    logger.info("启动洛天依对话示例")
    
    try:
        # 初始化Agent
        logger.info("初始化洛天依Agent...")
        config_path = project_root / "config" / "config.yaml"
        agent = LuoTianyiAgent(str(config_path))
        
        logger.info("洛天依Agent初始化完成！")
        print("\n" + "="*50)
        print("🎵 洛天依对话Agent 已启动 🎵")
        print("输入 'quit' 或 'exit' 退出对话")
        print("输入 'reset' 重置对话历史")
        print("="*50 + "\n")
        
        # 开始对话循环
        while True:
            try:
                # 获取用户输入
                user_input = input("你: ").strip()
                
                if not user_input:
                    continue
                
                # 处理特殊命令
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("洛天依: 再见啦～下次再聊哦！")
                    break
                elif user_input.lower() in ['reset', '重置']:
                    agent.reset()
                    print("洛天依: 对话历史已重置，我们重新开始吧～")
                    continue
                elif user_input.lower() in ['help', '帮助']:
                    print_help()
                    continue
                
                # 生成回复
                response = agent.chat(user_input)
                print(f"洛天依: {response}")
                
            except KeyboardInterrupt:
                print("\n洛天依: 再见啦～")
                break
            except Exception as e:
                logger.error(f"对话处理出错: {e}")
                print("洛天依: 诶？刚才出了点小问题呢～再试一次吧？")
                
    except Exception as e:
        logger.error(f"初始化失败: {e}")
        print(f"❌ 初始化失败: {e}")
        print("\n请检查：")
        print("1. 配置文件是否正确")
        print("2. API密钥是否设置")
        print("3. 依赖包是否安装完整")
        return 1
    
    return 0


def print_help():
    """打印帮助信息"""
    help_text = """
🎵 洛天依对话Agent 帮助信息 🎵

基本命令：
  quit/exit/退出  - 退出程序
  reset/重置      - 重置对话历史
  help/帮助       - 显示此帮助信息

对话技巧：
  • 可以问我关于我的歌曲、演出信息
  • 可以和我聊日常话题
  • 我会记住我们的对话历史哦～

示例对话：
  "你好洛天依！"
  "你有什么代表作品吗？"
  "今天天气真好呢"
  "能为我唱首歌吗？"
"""
    print(help_text)


def demo_conversations():
    """演示对话"""
    print("\n🎵 演示对话开始 🎵\n")
    
    # 这里可以添加一些预设的演示对话
    demo_messages = [
        "你好洛天依！",
        "你能介绍一下自己吗？",
        "你最喜欢的歌曲是什么？",
        "今天心情怎么样？"
    ]
    
    # TODO: 当Agent实现完成后，可以在这里添加演示逻辑
    print("演示功能将在Agent实现完成后提供")


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
