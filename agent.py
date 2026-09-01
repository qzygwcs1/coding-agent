"""Command-line entry point for the coding agent.

The model client and local tools will be added in later steps.  This first
version only proves that the project can start and accepts a task/workspace.
"""

from __future__ import annotations

import argparse
from pathlib import Path


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
    print("Agent scaffold is ready. Model and local tools will be added next.")


if __name__ == "__main__":
    main()
