from pathlib import Path

from tools import WorkspaceTools


def test_file_tools_stay_in_workspace(tmp_path: Path) -> None:
    tools = WorkspaceTools(tmp_path)
    assert "status: success" in tools.write_file("nested/example.txt", "hello")
    assert "hello" in tools.read_file("nested/example.txt")
    assert "nested/example.txt" in tools.list_files()
    assert "status: error" in tools.read_file("../outside.txt")


def test_run_command_reports_exit_code(tmp_path: Path) -> None:
    tools = WorkspaceTools(tmp_path)
    result = tools.run_command("python -c \"print('ok')\"")
    assert "status: success" in result
    assert "exit_code: 0" in result
    assert "ok" in result


def test_run_command_reports_failure(tmp_path: Path) -> None:
    tools = WorkspaceTools(tmp_path)
    result = tools.run_command("python -c \"raise SystemExit(3)\"")
    assert "status: error" in result
    assert "exit_code: 3" in result
