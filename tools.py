from __future__ import annotations

import subprocess
from pathlib import Path

DEFAULT_COMMAND_TIMEOUT = 30
MAX_OUTPUT_CHARS = 12000


class WorkspaceTools:
    def __init__(self, workspace: Path, command_timeout: int = DEFAULT_COMMAND_TIMEOUT):
        self.workspace = workspace.expanduser().resolve()
        if not self.workspace.is_dir():
            raise ValueError(f"Workspace does not exist: {self.workspace}")
        self.command_timeout = command_timeout

    def _safe_path(self, path: str) -> Path:
        candidate = (self.workspace / path).resolve()
        try:
            candidate.relative_to(self.workspace)
        except ValueError as error:
            raise ValueError("path must stay inside the workspace") from error
        return candidate

    @staticmethod
    def _clip(text: str) -> str:
        if len(text) <= MAX_OUTPUT_CHARS:
            return text
        half = MAX_OUTPUT_CHARS // 2
        return text[:half] + f"\n... output truncated ({len(text)} chars total) ...\n" + text[-half:]

    def list_files(self, path: str = ".") -> str:
        try:
            directory = self._safe_path(path)
            if not directory.is_dir():
                return f"status: error\npath is not a directory: {path}"
            entries = []
            for item in sorted(directory.rglob("*")):
                if ".git" in item.parts or ".venv" in item.parts or "__pycache__" in item.parts:
                    continue
                relative = str(item.relative_to(self.workspace)).replace("\\", "/")
                entries.append(relative + ("/" if item.is_dir() else ""))
            return "status: success\n" + ("\n".join(entries) or "(empty)")
        except (OSError, ValueError) as error:
            return f"status: error\n{error}"

    def read_file(self, path: str) -> str:
        try:
            file_path = self._safe_path(path)
            if not file_path.is_file():
                return f"status: error\nfile does not exist: {path}"
            content = file_path.read_text(encoding="utf-8")
            return f"status: success\npath: {path}\ncontent:\n{self._clip(content)}"
        except (OSError, UnicodeError, ValueError) as error:
            return f"status: error\n{error}"

    def write_file(self, path: str, content: str) -> str:
        try:
            file_path = self._safe_path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            return f"status: success\nwritten: {path}\nchars: {len(content)}"
        except (OSError, UnicodeError, ValueError) as error:
            return f"status: error\n{error}"

    def run_command(self, command: str) -> str:
        try:
            completed = subprocess.run(command, shell=True, cwd=self.workspace, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=self.command_timeout)
            return (f"status: {'success' if completed.returncode == 0 else 'error'}\n"
                    f"exit_code: {completed.returncode}\nstdout:\n{self._clip(completed.stdout)}\n"
                    f"stderr:\n{self._clip(completed.stderr)}")
        except subprocess.TimeoutExpired:
            return f"status: error\ncommand timed out after {self.command_timeout} seconds"
        except OSError as error:
            return f"status: error\n{error}"


def build_tool_handlers(workspace: Path) -> dict[str, object]:
    tools = WorkspaceTools(workspace)
    return {"list_files": tools.list_files, "read_file": tools.read_file, "write_file": tools.write_file, "run_command": tools.run_command}
