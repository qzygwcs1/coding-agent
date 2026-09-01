"""Environment-backed configuration for the model client."""

from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv() -> None:
        env_path = __import__("pathlib").Path(".env")
        if not env_path.is_file():
            return
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                name, value = line.split("=", 1)
                os.environ.setdefault(name.strip(), value.strip())


@dataclass(frozen=True)
class ModelConfig:
    api_key: str
    base_url: str
    model_name: str


def load_model_config() -> ModelConfig:
    load_dotenv()
    values = {name: os.getenv(name, "").strip() for name in ("MODEL_API_KEY", "MODEL_BASE_URL", "MODEL_NAME")}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise ValueError("缺少模型配置：" + ", ".join(missing) + "。请检查 .env 文件。")
    return ModelConfig(values["MODEL_API_KEY"], values["MODEL_BASE_URL"].rstrip("/"), values["MODEL_NAME"])
