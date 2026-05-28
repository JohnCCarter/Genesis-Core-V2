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
