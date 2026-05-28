from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import uvicorn

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import core.server as server_mod


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local Genesis-Core-V2 API shell")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true")
    parser.add_argument("--print-config", action="store_true")
    return parser


def build_runtime_config(*, host: str, port: int, reload: bool) -> dict[str, Any]:
    return {
        "app": "core.server:app",
        "app_dir": str(SRC_ROOT),
        "host": host,
        "port": port,
        "reload": reload,
        "module_file": str(Path(server_mod.__file__).resolve()),
        "route_count": len(server_mod.app.routes),
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = build_runtime_config(host=str(args.host), port=int(args.port), reload=bool(args.reload))
    if args.print_config:
        print(json.dumps(config, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    uvicorn.run(
        config["app"],
        app_dir=config["app_dir"],
        host=config["host"],
        port=config["port"],
        reload=config["reload"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
