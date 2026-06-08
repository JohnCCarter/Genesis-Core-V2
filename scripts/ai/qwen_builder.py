from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"


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


def main(argv: list[str] | None = None) -> int:
    _prefer_local_src()
    from genesis_core_v2_cli.qwen_builder import main as qwen_builder_main

    return int(qwen_builder_main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
