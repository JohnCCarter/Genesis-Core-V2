from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = REPO_ROOT / "config" / "mcp_settings.json"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ["GENESIS_MCP_CONFIG_PATH"] = str(DEFAULT_CONFIG_PATH)

import mcp_server.server as server_mod


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local Genesis-Core-V2 MCP stdio shell")
    parser.add_argument("--print-config", action="store_true")
    return parser


def build_runtime_config() -> dict[str, Any]:
    return {
        "config_env": os.environ.get("GENESIS_MCP_CONFIG_PATH", ""),
        "config_path": str(DEFAULT_CONFIG_PATH),
        "feature_flags": {
            "file_operations": server_mod.config.features.file_operations,
            "code_execution": server_mod.config.features.code_execution,
            "git_integration": server_mod.config.features.git_integration,
        },
        "log_level": server_mod.config.log_level,
        "module_file": str(Path(server_mod.__file__).resolve()),
        "server_name": server_mod.config.server_name,
        "tool_count": len(server_mod.TOOLS),
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = build_runtime_config()
    if args.print_config:
        print(json.dumps(config, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    asyncio.run(server_mod.main())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
