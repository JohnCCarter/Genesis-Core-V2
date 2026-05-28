from __future__ import annotations

import tomllib
from pathlib import Path


def test_pyproject_declares_runtime_smoke_console_scripts() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    payload = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))

    assert payload["project"]["scripts"] == {
        "genesis-v2-fixture-smoke": "genesis_core_v2_cli.console_scripts:fixture_smoke_main",
        "genesis-v2-backtest-smoke": "genesis_core_v2_cli.console_scripts:backtest_smoke_main",
        "genesis-v2-smoke-suite": "genesis_core_v2_cli.console_scripts:smoke_suite_main",
    }


def test_pyproject_declares_narrow_local_tooling_defaults() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    payload = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))

    assert payload["tool"]["pytest"]["ini_options"]["norecursedirs"] == [
        "cache",
        "data",
        "logs",
        "results",
        ".venv",
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
