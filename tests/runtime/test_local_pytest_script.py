from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def test_local_pytest_script_prints_runtime_config() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "validate" / "pytest_suite.py"), "--print-config"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["cwd"].replace("\\", "/").endswith("/Genesis-Core-V2")
    assert payload["src_root"].replace("\\", "/").endswith("/Genesis-Core-V2/src")
    assert payload["pytest_args"] == ["-q"]
    assert payload["pythonpath"].split(os.pathsep)[0].replace("\\", "/").endswith(
        "/Genesis-Core-V2/src"
    )


def test_local_pytest_script_runs_focused_runtime_test() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "validate" / "pytest_suite.py"),
            "tests/runtime/test_local_api_shell_script.py",
            "-q",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    combined_output = completed.stdout + completed.stderr

    assert combined_output.strip()
