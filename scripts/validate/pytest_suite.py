from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
DEFAULT_PYTEST_ARGS = ["-q"]


def _prefer_local_src() -> None:
    normalized_src = str(SRC_ROOT)
    normalized_repo = str(REPO_ROOT)

    if normalized_repo not in sys.path:
        sys.path.insert(0, normalized_repo)
    if normalized_src not in sys.path:
        sys.path.insert(0, normalized_src)

    existing = [entry for entry in os.environ.get("PYTHONPATH", "").split(os.pathsep) if entry]
    desired_prefix = [normalized_src, normalized_repo]
    filtered_existing = [entry for entry in existing if entry not in desired_prefix]
    os.environ["PYTHONPATH"] = os.pathsep.join([*desired_prefix, *filtered_existing])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local Genesis-Core-V2 pytest suite")
    parser.add_argument("--print-config", action="store_true")
    return parser


def build_runtime_config(pytest_args: list[str] | None = None) -> dict[str, Any]:
    return {
        "cwd": str(REPO_ROOT),
        "src_root": str(SRC_ROOT),
        "pythonpath": os.environ.get("PYTHONPATH", ""),
        "pytest_args": list(pytest_args or DEFAULT_PYTEST_ARGS),
    }


def main(argv: list[str] | None = None) -> int:
    _prefer_local_src()
    parsed_args, pytest_args = build_parser().parse_known_args(argv)
    config = build_runtime_config(pytest_args or DEFAULT_PYTEST_ARGS)
    if parsed_args.print_config:
        print(json.dumps(config, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    return int(pytest.main(config["pytest_args"]))


if __name__ == "__main__":
    raise SystemExit(main())
