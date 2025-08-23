from src.agents.luotianyi_agent import LuoTianyiAgent
import re
agent = LuoTianyiAgent("config/config.json")
ret = agent.chat("天依晚上好！")

# 按照中文标点符号和emoji将回复文本分割成多个部分
segments = re.split(r'(?<=[。！？])|(?=[\U0001F600-\U0001F64F])', ret)

# 逐个输出
import time
for segment in segments:
    length = len(segment)
    time.sleep(0.1 * length)  # 根据文本长度调整延迟时间
    print(segment)