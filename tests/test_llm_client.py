from types import SimpleNamespace

from config import ModelConfig
from llm_client import ModelClient


def test_complete_extracts_text_without_printing_key() -> None:
    client = ModelClient.__new__(ModelClient)
    client.config = ModelConfig("secret-key", "https://example.test/v1", "test-model")
    client._client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **kwargs: SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="模型连接成功"))]))))
    assert client.complete([{"role": "user", "content": "回复连接成功"}]) == "模型连接成功"
