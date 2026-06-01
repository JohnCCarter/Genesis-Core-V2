from __future__ import annotations

import json
from pathlib import Path

EXPECTED_TASK_ARGS = {
    "genesis-v2: api shell": ["scripts/api/api_shell.py", "--reload"],
    "genesis-v2: mcp stdio": ["scripts/mcp/mcp_stdio.py"],
    "genesis-v2: smoke suite": ["scripts/smoke/smoke_suite.py"],
    "genesis-v2: pytest": ["scripts/validate/pytest_suite.py", "-q"],
}


def test_local_vscode_tasks_encode_repeatable_skeleton_loop() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    payload = json.loads((repo_root / ".vscode" / "tasks.json").read_text(encoding="utf-8"))
    tasks = {task["label"]: task for task in payload["tasks"]}

    assert payload["version"] == "2.0.0"
    assert payload["options"] == {
        "cwd": "${workspaceFolder}",
        "env": {"PYTHONPATH": "${workspaceFolder}/src"},
    }
    assert set(EXPECTED_TASK_ARGS).issubset(tasks)

    for label, expected_args in EXPECTED_TASK_ARGS.items():
        assert tasks[label]["command"] == "python"
        assert tasks[label]["args"] == expected_args

    assert tasks["genesis-v2: api shell"]["isBackground"] is True
    assert tasks["genesis-v2: mcp stdio"]["isBackground"] is True
    assert tasks["genesis-v2: pytest"]["group"] == {"kind": "test", "isDefault": True}
