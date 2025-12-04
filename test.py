import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-831335d092bb4550ba87db6b7f7eacbf",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen-vl-max",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://gchat.qpic.cn/gchatpic_new/0/0-0-22167BA09D776C2EB1838946A9AB2EED/0"
                    },
                },
                {"type": "text", "text": "请分析图片内容。"},
            ],
        },
    ],
)
print(completion.choices[0].message.content)