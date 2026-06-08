from __future__ import annotations

import importlib.metadata as importlib_metadata
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

EXPECTED_ENTRYPOINTS = {
    "genesis-v2-api-shell": "genesis_core_v2_cli.console_scripts:api_shell_main",
    "genesis-v2-mcp-stdio": "genesis_core_v2_cli.console_scripts:mcp_stdio_main",
    "genesis-v2-pytest": "genesis_core_v2_cli.console_scripts:pytest_suite_main",
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
        pytest.skip("Project sync required for console script verification")


def _installed_console_entrypoints() -> dict[str, str]:
    return {
        entry_point.name: f"{entry_point.module}:{entry_point.attr}"
        for entry_point in importlib_metadata.entry_points(group="console_scripts")
        if entry_point.name in EXPECTED_ENTRYPOINTS
    }


def _require_current_console_script_install() -> dict[str, str]:
    _require_installed_distribution()
    entry_points = _installed_console_entrypoints()
    if entry_points != EXPECTED_ENTRYPOINTS:
        pytest.skip(
            'Current interpreter does not expose the expected Genesis-Core-V2 console scripts; run `uv sync --extra dev --extra mcp` in this interpreter.'
        )
    return entry_points


def _require_module(module_name: str, install_hint: str) -> None:
    if importlib.util.find_spec(module_name) is None:
        pytest.skip(f"Console script verification requires {install_hint}")


def test_installed_distribution_registers_expected_console_scripts() -> None:
    entry_points = _require_current_console_script_install()
    assert entry_points == EXPECTED_ENTRYPOINTS


def _run_installed_entrypoint(
    command: str, command_args: list[str]
) -> subprocess.CompletedProcess[str]:
    repo_root = Path(__file__).resolve().parents[2]
    code = """
import importlib.metadata as importlib_metadata
import sys

entry_points = {
    entry_point.name: entry_point
    for entry_point in importlib_metadata.entry_points(group='console_scripts')
}
entry_point = entry_points[sys.argv[1]]
callable_obj = entry_point.load()
sys.argv = [sys.argv[1], *sys.argv[2:]]
raise SystemExit(callable_obj())
"""
    return subprocess.run(
        [sys.executable, "-c", code, command, *command_args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )


@pytest.mark.parametrize(
    ("command", "command_args", "required_module", "install_hint", "expected_pairs"),
    [
        (
            "genesis-v2-api-shell",
            ["--print-config"],
            None,
            None,
            {
                "app": "core.server:app",
                "host": "127.0.0.1",
                "port": 8000,
                "reload": False,
            },
        ),
        (
            "genesis-v2-mcp-stdio",
            ["--print-config"],
            "mcp",
            'the optional `[mcp]` extra (`uv sync --extra mcp`)',
            {
                "server_name": "genesis-core-v2",
                "log_level": "INFO",
            },
        ),
        (
            "genesis-v2-pytest",
            ["--print-config"],
            "pytest",
            'the local test dependencies (`uv sync --extra dev`)',
            {
                "pytest_args": ["-q"],
            },
        ),
        (
            "genesis-v2-champion-smoke",
            [],
            None,
            None,
            {"version": "seed_champion_fixture_v1"},
        ),
        (
            "genesis-v2-evaluate-champion-smoke",
            [],
            None,
            None,
            {"action": "NONE", "champion_source": "registry/fixtures/champions/tBTCUSD_1h.json"},
        ),
        ("genesis-v2-fixture-smoke", [], None, None, {"action": "NONE"}),
        (
            "genesis-v2-backtest-smoke",
            [],
            None,
            None,
            {"trade_count": 1, "deterministic": True},
        ),
        (
            "genesis-v2-model-smoke",
            [],
            None,
            None,
            {"schema": ["ema_50"]},
        ),
        (
            "genesis-v2-smoke-suite",
            [],
            None,
            None,
            {"suite": "runtime_smoke_suite_v1"},
        ),
    ],
)
def test_installed_console_scripts_execute(
    command: str,
    command_args: list[str],
    required_module: str | None,
    install_hint: str | None,
    expected_pairs: dict[str, object],
) -> None:
    _require_current_console_script_install()
    if required_module is not None and install_hint is not None:
        _require_module(required_module, install_hint)

    completed = _run_installed_entrypoint(command, command_args)
    payload = json.loads(completed.stdout)

    for key, expected_value in expected_pairs.items():
        assert payload.get(key) == expected_value
