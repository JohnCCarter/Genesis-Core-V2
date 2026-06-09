from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_research_wiki_lint_script_prints_runtime_config() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "audit" / "research_wiki_lint.py"),
            "--print-config",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["research_root"].replace("\\", "/").endswith("/Genesis-Core-V2/docs/research")
    assert "docs/research/index.md" in payload["required_paths"]
    assert "docs/research/operations.md" in payload["required_paths"]
    assert (
        "docs/research/queries/2026-06-04-karpathy-agent-discipline.md" in payload["required_paths"]
    )
    assert (
        "docs/research/queries/2026-06-04-nvidia-skills-cherry-pick-review.md"
        in payload["required_paths"]
    )
    assert "docs/research/templates/capability-card-template.md" in payload["required_paths"]
    assert "docs/research/templates/evidence-pipeline-template.md" in payload["required_paths"]
    assert "docs/research/templates/evaluation-record-template.md" in payload["required_paths"]
    assert (
        "docs/research/templates/endpoint-security-checklist-template.md"
        in payload["required_paths"]
    )
    assert payload["marker_count"] >= 50


def test_research_wiki_lint_script_passes_for_current_repo() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "audit" / "research_wiki_lint.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["ok"] is True
    assert payload["missing_paths"] == []
    assert payload["missing_markers"] == []
