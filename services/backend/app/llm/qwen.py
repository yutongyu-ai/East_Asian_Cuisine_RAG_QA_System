import os
from openai import OpenAI
from pydantic import PrivateAttr

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

class QwenLLM(BaseChatModel):

    _client: OpenAI = PrivateAttr()

    @property
    def _llm_type(self):
        return "qwen-intl"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        object.__setattr__(
            self,
            "_client",
            OpenAI(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
            )
        )

    def _generate(self, messages, stop=None, **kwargs):

        role_map = {
            "human": "user",
            "ai": "assistant",
            "system": "system"
        }

        formatted = [
            {
                "role": role_map.get(m.type, "user"),
                "content": m.content
            }
            for m in messages
        ]

        resp = self._client.chat.completions.create(
            model="qwen-turbo",
            messages=formatted
        )

        return ChatResult(generations=[
            ChatGeneration(
                message=AIMessage(content=resp.choices[0].message.content)
            )
        ])