from __future__ import annotations

from pathlib import Path

import yaml


def test_local_precommit_config_encodes_narrow_dev_hooks() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    payload = yaml.safe_load((repo_root / ".pre-commit-config.yaml").read_text(encoding="utf-8"))

    hook_ids = [hook["id"] for repo in payload["repos"] for hook in repo.get("hooks", [])]
    assert hook_ids == [
        "black",
        "ruff",
        "check-added-large-files",
        "check-merge-conflict",
        "check-yaml",
        "end-of-file-fixer",
        "trailing-whitespace",
        "check-json",
    ]
