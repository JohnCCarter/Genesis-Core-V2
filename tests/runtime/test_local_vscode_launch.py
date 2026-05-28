from __future__ import annotations

import json
from pathlib import Path


EXPECTED_LAUNCH_PROGRAMS = {
    "genesis-v2: api shell": "${workspaceFolder}/scripts/api/api_shell.py",
    "genesis-v2: smoke suite": "${workspaceFolder}/scripts/smoke/smoke_suite.py",
    "genesis-v2: pytest": "${workspaceFolder}/scripts/validate/pytest_suite.py",
}


def test_local_vscode_launch_profiles_encode_repeatable_debug_loop() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    payload = json.loads((repo_root / ".vscode" / "launch.json").read_text(encoding="utf-8"))
    configs = {config["name"]: config for config in payload["configurations"]}

    assert payload["version"] == "0.2.0"
    assert set(EXPECTED_LAUNCH_PROGRAMS).issubset(configs)

    for name, expected_program in EXPECTED_LAUNCH_PROGRAMS.items():
        assert configs[name]["type"] == "debugpy"
        assert configs[name]["request"] == "launch"
        assert configs[name]["program"] == expected_program
        assert configs[name]["cwd"] == "${workspaceFolder}"
        assert configs[name]["env"] == {"PYTHONPATH": "${workspaceFolder}/src"}
        assert configs[name]["console"] == "integratedTerminal"

    assert configs["genesis-v2: api shell"]["args"] == ["--reload"]
    assert configs["genesis-v2: smoke suite"].get("args", []) == []
    assert configs["genesis-v2: pytest"]["args"] == ["-q"]
    assert configs["genesis-v2: pytest"]["purpose"] == ["debug-test"]
