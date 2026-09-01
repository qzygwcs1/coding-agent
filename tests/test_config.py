import pytest

from config import load_model_config


def test_load_model_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MODEL_API_KEY", "test-key")
    monkeypatch.setenv("MODEL_BASE_URL", "https://example.test/v1/")
    monkeypatch.setenv("MODEL_NAME", "test-model")
    config = load_model_config()
    assert config.api_key == "test-key"
    assert config.base_url == "https://example.test/v1"
    assert config.model_name == "test-model"


def test_missing_model_config(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("MODEL_API_KEY", "MODEL_BASE_URL", "MODEL_NAME"):
        monkeypatch.setenv(name, "")
    with pytest.raises(ValueError, match="缺少模型配置"):
        load_model_config()
