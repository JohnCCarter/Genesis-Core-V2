from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def _load_lint_module():
    repo_root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location(
        "research_wiki_lint", repo_root / "scripts" / "audit" / "research_wiki_lint.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


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


def test_research_wiki_lint_script_reports_referential_integrity() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "audit" / "research_wiki_lint.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(completed.stdout)

    # Referential findings are warn-only: they are reported but never flip the structural `ok`.
    assert "referential_ok" in payload
    # Every dated content page must be registered in its section index.md, and every registry
    # reference must resolve.
    assert payload["unregistered_pages"] == []
    assert payload["dangling_references"] == []
    assert payload["referential_ok"] is True


def test_referential_checks_fire_on_unregistered_and_dangling(tmp_path, monkeypatch) -> None:
    module = _load_lint_module()

    research_root = tmp_path / "docs" / "research"
    queries = research_root / "queries"
    queries.mkdir(parents=True)
    # a section index with no entry for the page below -> the page is unregistered
    (queries / "index.md").write_text("## Current registry\n", encoding="utf-8")
    (queries / "2026-01-01-orphan.md").write_text("# orphan\n", encoding="utf-8")
    # a registry that points at a page which does not resolve -> dangling reference
    (research_root / "map.md").write_text("see `queries/nope.md`\n", encoding="utf-8")

    monkeypatch.setattr(module, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(module, "RESEARCH_ROOT", research_root)

    result = module.run_referential_checks()

    assert result["referential_ok"] is False
    assert "queries/2026-01-01-orphan.md" in result["unregistered_pages"]
    assert any(ref["ref"] == "queries/nope.md" for ref in result["dangling_references"])


def test_research_wiki_lint_script_reports_semantic_integrity() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "audit" / "research_wiki_lint.py")],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(completed.stdout)

    # Semantic findings are warn-only on their own `semantic_ok`, decoupled from `referential_ok`
    # and the structural `ok`. No page is unreachable, and no markdown intra-wiki link is broken.
    assert "semantic_ok" in payload
    assert payload["orphan_pages"] == []
    assert payload["broken_links"] == []
    assert payload["semantic_ok"] is True


def test_semantic_checks_fire_on_orphan_and_broken_link(tmp_path, monkeypatch) -> None:
    module = _load_lint_module()

    research_root = tmp_path / "docs" / "research"
    research_root.mkdir(parents=True)
    # map.md (a registry) reaches topic-a via a backtick mention -> topic-a is not an orphan
    (research_root / "map.md").write_text("see `topic-a.md`\n", encoding="utf-8")
    # topic-a is reachable but carries a broken markdown link (real `[text](target.md)` syntax;
    # a backtick mention would NOT count -- broken-link detection targets markdown links only).
    # The code-span link must be ignored: documenting link syntax is not a broken link.
    (research_root / "topic-a.md").write_text(
        "[gone](missing.md)\nsyntax is `[x](in-code.md)`\n", encoding="utf-8"
    )
    # topic-orphan is referenced by nobody -> orphan
    (research_root / "topic-orphan.md").write_text("# orphan\n", encoding="utf-8")

    monkeypatch.setattr(module, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(module, "RESEARCH_ROOT", research_root)

    result = module.run_semantic_checks()

    assert result["semantic_ok"] is False
    assert "topic-orphan.md" in result["orphan_pages"]
    assert "topic-a.md" not in result["orphan_pages"]
    assert any(link["link"] == "missing.md" for link in result["broken_links"])
    # the code-span link is literal text, not a link -> never reported
    assert not any(link["link"] == "in-code.md" for link in result["broken_links"])
