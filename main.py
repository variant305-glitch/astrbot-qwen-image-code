from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult  # pyright: ignore[reportMissingImports]
from astrbot.api.star import Context, Star, register  # pyright: ignore[reportMissingImports]
from astrbot.api import logger  # pyright: ignore[reportMissingImports]
import os
from openai import OpenAI
def get_image_jieshi(self,image_url,message_user = "请分析图中日志或代码是做什么的或者有什么错误，并给出建议"):
    try:
        client = OpenAI(
            api_key= self.api_key, #获取配置文件的api_key  
            base_url=self.base_url,  #获取配置文件的base_url
            )
        if self.api_key == "":       # 判断api_key是否为空
            return "请填写正确的api_key"
        if self.base_url is None:
            return "请发送图片"
        if self.model == "":
            return "请填写正确的AI模型参数"
        completion = client.chat.completions.create(
        model = self.model , #获取配置文件的AI模型参数
        messages=[
            {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": image_url},
                },
                {"type": "text", "text":message_user + "请用简短的中文纯文本回答。"},
            ],
            },
        ],
        )
        return completion.choices[0].message.content 
    except Exception as e:
        logger.error(e)
        return "识别错误，请检查控制台日志"
 

url = None
def extract_image_url(chain):
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
@register("qwen_codeimage", "Xiaji", "通过代码或日志截图来识别内容或错误并给出建议", "1.0")
class MyPlugin(Star):
    def __init__(self, context: Context,config: dict):
        super().__init__(context)
        self.config = config
        self.api_key = config.get("api_key", "")
        self.model = config.get("model", "qwen-vl-max")
        self.base_url = config.get("base_url", "")
    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 帮我看看。注册成功后，发送 `帮我看看` 就会触发这个指令
    @filter.command("帮我看看")
    async def look(self, event: AstrMessageEvent):
        """这是一个识别用户发送图片作出反应指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        #user_name =  event.get_sender_name()
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        message_user = message_str[4:]
        s = None
        s =  extract_image_url(message_chain)
        logger.info(s)
        get_huida =  get_image_jieshi(self,s,message_user)
        
        yield event.plain_result(str(get_huida)) # 发送一条纯文本消息
    
    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
