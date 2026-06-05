from __future__ import annotations

import tomllib
from pathlib import Path


def test_pyproject_declares_local_tooling_console_scripts() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    payload = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))

    assert payload["project"]["scripts"] == {
        "genesis-v2-api-shell": "genesis_core_v2_cli.console_scripts:api_shell_main",
        "genesis-v2-mcp-stdio": "genesis_core_v2_cli.console_scripts:mcp_stdio_main",
        "genesis-v2-pytest": "genesis_core_v2_cli.console_scripts:pytest_suite_main",
        "genesis-v2-qwen-builder": "genesis_core_v2_cli.console_scripts:qwen_builder_main",
        "genesis-v2-champion-smoke": "genesis_core_v2_cli.console_scripts:champion_smoke_main",
        "genesis-v2-evaluate-champion-smoke": "genesis_core_v2_cli.console_scripts:evaluate_champion_smoke_main",
        "genesis-v2-fixture-smoke": "genesis_core_v2_cli.console_scripts:fixture_smoke_main",
        "genesis-v2-backtest-smoke": "genesis_core_v2_cli.console_scripts:backtest_smoke_main",
        "genesis-v2-model-smoke": "genesis_core_v2_cli.console_scripts:model_smoke_main",
        "genesis-v2-smoke-suite": "genesis_core_v2_cli.console_scripts:smoke_suite_main",
    }


def test_pyproject_declares_narrow_local_tooling_defaults() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    payload = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))

    assert payload["tool"]["pytest"]["ini_options"]["pythonpath"] == ["src", "."]
    assert payload["tool"]["pytest"]["ini_options"]["norecursedirs"] == [
        "cache",
        "data",
        "logs",
        "results",
        ".venv",
        ".hypothesis",
    ]
    assert payload["tool"]["ruff"]["extend-exclude"] == [
        ".venv/",
        "cache/",
        "data/",
        "logs/",
        "results/",
    ]
    assert payload["tool"]["ruff"]["lint"]["select"] == ["E", "W", "F", "I", "B", "C4", "UP"]
    assert payload["tool"]["ruff"]["lint"]["ignore"] == ["E501", "B008", "C901"]
    assert payload["tool"]["black"]["extend-exclude"] == "(^cache/|^data/|^logs/|^results/)"
