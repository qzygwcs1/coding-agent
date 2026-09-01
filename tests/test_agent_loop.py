from typing import Any

from agent_loop import AgentLoop


class FakeClient:
    def __init__(self, responses: list[dict[str, Any]]):
        self.responses = iter(responses)
        self.calls: list[list[dict[str, Any]]] = []

    def complete_with_tools(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> dict[str, Any]:
        self.calls.append(messages.copy())
        return next(self.responses)


def test_loop_executes_tool_and_returns_final_answer() -> None:
    client = FakeClient([
        {"role": "assistant", "content": None, "tool_calls": [{"id": "call-1", "type": "function", "function": {"name": "read_file", "arguments": '{"path":"a.py"}'}}]},
        {"role": "assistant", "content": "已读取文件并完成任务。"},
    ])
    events: list[str] = []
    loop = AgentLoop(client, {"read_file": lambda path: f"content of {path}"}, on_event=events.append)
    assert loop.run("查看 a.py") == "已读取文件并完成任务。"
    assert len(client.calls) == 2
    assert any("content of a.py" in str(message) for message in client.calls[1])


def test_loop_reports_bad_tool_arguments_and_stops_at_limit() -> None:
    client = FakeClient([
        {"role": "assistant", "content": None, "tool_calls": [{"id": "call-1", "type": "function", "function": {"name": "read_file", "arguments": "not-json"}}]},
    ])
    loop = AgentLoop(client, {"read_file": lambda path: "unused"}, max_steps=1, on_event=lambda _: None)
    assert "达到最大步骤数" in loop.run("test")
