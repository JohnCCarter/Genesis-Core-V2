from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_local_api_shell_script_prints_runtime_config() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "api" / "api_shell.py"), "--print-config"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["app"] == "core.server:app"
    assert payload["host"] == "127.0.0.1"
    assert payload["port"] == 8000
    assert payload["reload"] is False
    assert payload["module_file"].replace("\\", "/").endswith("/src/core/server.py")
    assert payload["route_count"] >= 4
