"""Small OpenAI-compatible client wrapper used by the coding agent."""

from __future__ import annotations

from typing import Any

from openai import OpenAI

from config import ModelConfig


class ModelClient:
    def __init__(self, config: ModelConfig, timeout: float = 60.0):
        self.config = config
        self._client = OpenAI(api_key=config.api_key, base_url=config.base_url, timeout=timeout)

    def complete(self, messages: list[dict[str, Any]]) -> str:
        try:
            response = self._client.chat.completions.create(model=self.config.model_name, messages=messages)
            content = response.choices[0].message.content
            if not content:
                raise RuntimeError("模型返回了空回答")
            return content
        except Exception as error:
            raise RuntimeError(f"模型调用失败：{error}") from error
