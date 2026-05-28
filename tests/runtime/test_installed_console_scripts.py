from __future__ import annotations

import importlib.metadata as importlib_metadata
import json
import subprocess
import sys
from pathlib import Path

import pytest


EXPECTED_ENTRYPOINTS = {
    "genesis-v2-champion-smoke": "genesis_core_v2_cli.console_scripts:champion_smoke_main",
    "genesis-v2-evaluate-champion-smoke": "genesis_core_v2_cli.console_scripts:evaluate_champion_smoke_main",
    "genesis-v2-fixture-smoke": "genesis_core_v2_cli.console_scripts:fixture_smoke_main",
    "genesis-v2-backtest-smoke": "genesis_core_v2_cli.console_scripts:backtest_smoke_main",
    "genesis-v2-model-smoke": "genesis_core_v2_cli.console_scripts:model_smoke_main",
    "genesis-v2-smoke-suite": "genesis_core_v2_cli.console_scripts:smoke_suite_main",
}


def _require_installed_distribution() -> None:
    try:
        importlib_metadata.distribution("genesis-core-v2")
    except importlib_metadata.PackageNotFoundError:
        pytest.skip("Editable install required for console script verification")


def test_installed_distribution_registers_expected_console_scripts() -> None:
    _require_installed_distribution()

    entry_points = {
        entry_point.name: f"{entry_point.module}:{entry_point.attr}"
        for entry_point in importlib_metadata.entry_points(group="console_scripts")
        if entry_point.name in EXPECTED_ENTRYPOINTS
    }

    assert entry_points == EXPECTED_ENTRYPOINTS


def _resolve_console_script(command: str) -> list[str]:
    scripts_dir = Path(sys.executable).resolve().parent
    candidates = [
        scripts_dir / command,
        scripts_dir / f"{command}.exe",
        scripts_dir / f"{command}-script.py",
    ]
    for candidate in candidates:
        if candidate.exists():
            if candidate.suffix.lower() == ".py":
                return [sys.executable, str(candidate)]
            return [str(candidate)]

    raise AssertionError(f"Console script wrapper not found for {command!r} in {scripts_dir}")


@pytest.mark.parametrize(
    ("command", "expected_pairs"),
    [
        (
            "genesis-v2-champion-smoke",
            {"version": "seed_champion_fixture_v1"},
        ),
        (
            "genesis-v2-evaluate-champion-smoke",
            {"action": "NONE", "champion_source": "registry/fixtures/champions/tBTCUSD_1h.json"},
        ),
        ("genesis-v2-fixture-smoke", {"action": "NONE"}),
        (
            "genesis-v2-backtest-smoke",
            {"trade_count": 1, "deterministic": True},
        ),
        (
            "genesis-v2-model-smoke",
            {"schema": ["ema_50"]},
        ),
        (
            "genesis-v2-smoke-suite",
            {"suite": "runtime_smoke_suite_v1"},
        ),
    ],
)
def test_installed_console_scripts_execute(command: str, expected_pairs: dict[str, object]) -> None:
    _require_installed_distribution()

    completed = subprocess.run(
        _resolve_console_script(command),
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(completed.stdout)

    for key, expected_value in expected_pairs.items():
        assert payload.get(key) == expected_value
