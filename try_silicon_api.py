from openai import OpenAI
import os
key = os.environ.get("SILICONFLOW_API_KEY")

client = OpenAI(
    base_url="https://api.siliconflow.cn/v1",
    api_key=os.environ.get("SILICONFLOW_API_KEY"),
)

# 发送带有流式输出的请求
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V2.5",
    messages=[
        {
            "role": "user",
            "content": "请回复且仅回复两个字：收到",
        }
    ],
    stream=True,  # 启用流式输出
)

# 逐步接收并处理响应
for chunk in response:
    if not chunk.choices:
        continue
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
    if chunk.choices[0].delta.reasoning_content:
        print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
