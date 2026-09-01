from pathlib import Path


def test_project_entrypoint_exists() -> None:
    assert Path(__file__).parents[1].joinpath("agent.py").is_file()
