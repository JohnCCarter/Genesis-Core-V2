from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    ("relative_path", "expected_pairs"),
    [
        ("scripts/smoke/fixture_smoke.py", {"action": "NONE"}),
        ("scripts/smoke/backtest_smoke.py", {"trade_count": 1, "deterministic": True}),
        ("scripts/smoke/smoke_suite.py", {"suite": "runtime_smoke_suite_v1"}),
    ],
)
def test_local_smoke_scripts_execute_without_editable_install(
    relative_path: str,
    expected_pairs: dict[str, object],
) -> None:
    repo_root = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [sys.executable, str(repo_root / relative_path)],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(completed.stdout)

    for key, expected_value in expected_pairs.items():
        assert payload.get(key) == expected_value
