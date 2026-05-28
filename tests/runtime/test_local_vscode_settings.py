from __future__ import annotations

import json
from pathlib import Path


def test_local_vscode_settings_align_python_analysis_and_test_discovery() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    payload = json.loads((repo_root / ".vscode" / "settings.json").read_text(encoding="utf-8"))

    assert payload["python.analysis.extraPaths"] == ["${workspaceFolder}/src"]
    assert payload["python.envFile"] == "${workspaceFolder}/.env"
    assert payload["python.testing.cwd"] == "${workspaceFolder}"
    assert payload["python.testing.pytestArgs"] == ["-q"]
    assert payload["python.testing.pytestEnabled"] is True
    assert payload["python.testing.unittestEnabled"] is False
