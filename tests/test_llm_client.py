from types import SimpleNamespace

from config import ModelConfig
from llm_client import ModelClient


def test_complete_extracts_text_without_printing_key() -> None:
    client = ModelClient.__new__(ModelClient)
    client.config = ModelConfig("secret-key", "https://example.test/v1", "test-model")
    client._client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **kwargs: SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="模型连接成功"))]))))
    assert client.complete([{"role": "user", "content": "回复连接成功"}]) == "模型连接成功"


def test_complete_with_tools_returns_structured_tool_call() -> None:
    client = ModelClient.__new__(ModelClient)
    client.config = ModelConfig("secret-key", "https://example.test/v1", "test-model")
    client._client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=lambda **kwargs: SimpleNamespace(
                    choices=[SimpleNamespace(
                        message=SimpleNamespace(
                            content=None,
                            tool_calls=[SimpleNamespace(
                                id="call-1",
                                function=SimpleNamespace(name="read_file", arguments='{"path":"a.py"}'),
                            )],
                        )
                    )]
                )
            )
        )
    )
    result = client.complete_with_tools([], [{"type": "function"}])
    assert result["role"] == "assistant"
    assert result["tool_calls"][0]["function"]["name"] == "read_file"