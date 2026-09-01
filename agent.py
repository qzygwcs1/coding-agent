"""Command-line entry point for the coding agent.

The model client and local tools will be added in later steps.  This first
version only proves that the project can start and accepts a task/workspace.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from tools import WorkspaceTools
from config import load_model_config
from llm_client import ModelClient
from agent_loop import AgentLoop


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A small local coding agent")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Directory the agent will be allowed to inspect and modify",
    )
    parser.add_argument(
        "task",
        nargs="?",
        help="Programming task for the agent (omit to enter it interactively)",
    )
    parser.add_argument("--check-model", action="store_true", help="Send one request to verify the configured model")
    parser.add_argument("--max-steps", type=int, default=15, help="Maximum model-tool rounds")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = args.workspace.expanduser().resolve()

    if not workspace.is_dir():
        raise SystemExit(f"Workspace does not exist or is not a directory: {workspace}")

    task = args.task or input("Task: ").strip()
    if not task:
        raise SystemExit("A programming task is required.")

    print(f"Workspace: {workspace}")
    print(f"Task: {task}")
    tools = WorkspaceTools(workspace)
    print("Available local tools: list_files, read_file, write_file, run_command")
    print("Workspace files:")
    print(tools.list_files())
    if args.check_model:
        try:
            config = load_model_config()
            answer = ModelClient(config).complete([
                {"role": "system", "content": "你是一个简洁的编程助手。"},
                {"role": "user", "content": "请只回复：模型连接成功"},
            ])
            print(f"Model: {config.model_name}")
            print(f"Assistant: {answer}")
        except (ValueError, RuntimeError) as error:
            raise SystemExit(str(error)) from error
        return

    config = load_model_config()
    result = AgentLoop(ModelClient(config), {
        "list_files": tools.list_files,
        "read_file": tools.read_file,
        "write_file": tools.write_file,
        "run_command": tools.run_command,
    }, max_steps=args.max_steps).run(task)
    print(f"Final answer: {result}")

if __name__ == "__main__":
    main()
