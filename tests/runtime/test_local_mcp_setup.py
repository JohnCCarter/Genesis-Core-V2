from __future__ import annotations

import json
from pathlib import Path

from mcp_server.config import load_config
from mcp_server.server import TOOLS


def test_local_mcp_files_encode_safe_skeleton_defaults() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    vscode_payload = json.loads((repo_root / ".vscode" / "mcp.json").read_text(encoding="utf-8"))
    settings_payload = json.loads(
        (repo_root / "config" / "mcp_settings.json").read_text(encoding="utf-8")
    )

    server = vscode_payload["servers"]["genesis-core-v2"]
    assert server["args"] == ["-m", "mcp_server.server"]
    assert server["env"]["GENESIS_MCP_CONFIG_PATH"] == "config/mcp_settings.json"

    assert settings_payload["server_name"] == "genesis-core-v2"
    assert settings_payload["features"] == {
        "code_execution": False,
        "file_operations": True,
        "git_integration": True,
    }
    assert ".vscode" in settings_payload["security"]["allowed_paths"]
    assert "mcp_server" in settings_payload["security"]["allowed_paths"]
    assert ".env" in settings_payload["security"]["blocked_patterns"]
    assert "config/runtime.json" in settings_payload["security"]["blocked_patterns"]


def test_local_mcp_server_loads_generated_v2_settings() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    config = load_config(repo_root / "config" / "mcp_settings.json")
    tool_names = {tool.name for tool in TOOLS}

    assert config.server_name == "genesis-core-v2"
    assert config.features.file_operations is True
    assert config.features.code_execution is False
    assert config.features.git_integration is True
    assert {
        "read_file",
        "write_file",
        "list_directory",
        "get_project_structure",
        "search_code",
        "get_git_status",
    }.issubset(tool_names)
