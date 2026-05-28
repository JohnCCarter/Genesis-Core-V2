from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_local_mcp_script_prints_runtime_config() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "mcp" / "mcp_stdio.py"), "--print-config"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["server_name"] == "genesis-core-v2"
    assert payload["log_level"] == "INFO"
    assert payload["feature_flags"] == {
        "file_operations": True,
        "code_execution": False,
        "git_integration": True,
    }
    assert payload["config_env"].replace("\\", "/").endswith("/config/mcp_settings.json")
    assert payload["config_path"].replace("\\", "/").endswith("/config/mcp_settings.json")
    assert payload["module_file"].replace("\\", "/").endswith("/mcp_server/server.py")
    assert payload["tool_count"] >= 6
