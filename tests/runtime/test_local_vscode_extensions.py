from __future__ import annotations

import json
from pathlib import Path


def test_local_vscode_extensions_recommend_python_workflow_stack() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    payload = json.loads((repo_root / ".vscode" / "extensions.json").read_text(encoding="utf-8"))

    assert payload["recommendations"] == [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff",
    ]
    assert payload["unwantedRecommendations"] == []
