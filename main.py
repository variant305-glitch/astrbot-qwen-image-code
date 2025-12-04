import imghdr
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult  # pyright: ignore[reportMissingImports]
from astrbot.api.star import Context, Star, register  # pyright: ignore[reportMissingImports]
from astrbot.api import logger  # pyright: ignore[reportMissingImports]
import os
import dashscope
from openai import OpenAI
async def get_image_jieshi(image_url):
    
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
                    "image_url": {"url": image_url},
                },
                {"type": "text", "text": "请分析图片内容。"},
            ],
            },
        ],
        )
        return completion.choices[0].message.content
 

url = None
async def extract_image_url(chain):
    if chain is not None:
            for comp in chain:
                if hasattr(comp, 'type'):
                    if comp.type == 'Image' and hasattr(comp, 'url') and comp.url:
                        return comp.url
                    elif comp.type == 'Reply' and hasattr(comp, 'chain'):
                    # 递归检查 Reply 内部的消息链
                        url = extract_image_url(comp.chain)
                        if url:
                            return url
                        return url
    return None
@register("helloworld", "Xiaji", "一个简单的 Hello World 插件", "1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("帮我看看")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个识别用户发送图片作出反应指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        s = None
        s = await extract_image_url(message_chain)
        get_huida = await get_image_jieshi(s)

        yield event.plain_result(str(get_huida)) # 发送一条纯文本消息
        yield event.plain_result(f"发送消息，{message_chain} ")
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
