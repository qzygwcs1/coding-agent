"""The hand-written model -> tool -> result loop for the coding agent."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from llm_client import ModelClient


TOOL_DEFINITIONS = [
    {"type": "function", "function": {"name": "list_files", "description": "列出工作区内的文件", "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "相对工作区的目录，默认当前目录"}}, "additionalProperties": False}}},
    {"type": "function", "function": {"name": "read_file", "description": "读取工作区内的文本文件", "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "相对工作区的文件路径"}}, "required": ["path"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "write_file", "description": "写入工作区内的文件", "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "相对工作区的文件路径"}, "content": {"type": "string", "description": "要写入的完整文本"}}, "required": ["path", "content"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "run_command", "description": "在工作区内执行命令并返回输出", "parameters": {"type": "object", "properties": {"command": {"type": "string", "description": "要执行的命令"}}, "required": ["command"], "additionalProperties": False}}},
]

SYSTEM_PROMPT = """你是一个本地编程智能体。你只能通过提供的工具操作当前工作区。
先查看相关文件，再修改代码；修改后必须运行相关测试。必须根据工具真实结果判断任务是否完成，不能凭空声称成功。完成后说明修改了哪些文件和测试结果。"""


class AgentLoop:
    def __init__(self, client: ModelClient, handlers: dict[str, Callable[..., str]], max_steps: int = 15, on_event: Callable[[str], None] | None = None):
        self.client = client
        self.handlers = handlers
        self.max_steps = max_steps
        self.on_event = on_event or (lambda message: print(message))

    def _event(self, message: str) -> None:
        self.on_event(message)

    def run(self, task: str) -> str:
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task},
        ]
        for step in range(1, self.max_steps + 1):
            self._event(f"\n[Step {step}] model is thinking")
            assistant = self.client.complete_with_tools(messages, TOOL_DEFINITIONS)
            messages.append(assistant)
            tool_calls = assistant.get("tool_calls") or []
            if not tool_calls:
                answer = assistant.get("content") or "模型没有返回最终回答。"
                self._event(f"[Assistant] {answer}")
                return answer

            for call in tool_calls:
                function = call.get("function", {})
                name = function.get("name", "")
                raw_arguments = function.get("arguments", "{}")
                call_id = call.get("id", "missing-tool-call-id")
                self._event(f"[Tool] {name} {raw_arguments}")
                try:
                    arguments = json.loads(raw_arguments) if isinstance(raw_arguments, str) else raw_arguments
                    if not isinstance(arguments, dict):
                        raise ValueError("tool arguments must be a JSON object")
                    handler = self.handlers.get(name)
                    if handler is None:
                        raise ValueError(f"unknown tool: {name}")
                    result = handler(**arguments)
                except Exception as error:
                    result = f"status: error\n{name}: {error}"
                self._event(f"[Result] {result[:500]}")
                messages.append({"role": "tool", "tool_call_id": call_id, "content": result})
        answer = f"达到最大步骤数（{self.max_steps}），任务停止。请检查工作区后继续。"
        self._event(f"[Stopped] {answer}")
        return answer
