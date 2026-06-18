from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
RESEARCH_ROOT = REPO_ROOT / "docs" / "research"

REQUIRED_PATHS = [
    "docs/research/index.md",
    "docs/research/map.md",
    "docs/research/log.md",
    "docs/research/patterns.md",
    "docs/research/operations.md",
    "docs/research/sources/index.md",
    "docs/research/artifacts/index.md",
    "docs/research/experiments/index.md",
    "docs/research/handoff.md",
    "docs/research/queries/index.md",
    "docs/research/lint/index.md",
    "docs/research/lint/2026-06-04-structure-health-check.md",
    "docs/research/templates/topic-template.md",
    "docs/research/templates/artifact-template.md",
    "docs/research/templates/experiment-template.md",
    "docs/research/templates/evidence-pipeline-template.md",
    "docs/research/templates/handoff-template.md",
    "docs/research/templates/query-template.md",
    "docs/research/templates/lint-template.md",
    "docs/research/templates/capability-card-template.md",
    "docs/research/templates/evaluation-record-template.md",
    "docs/research/templates/endpoint-security-checklist-template.md",
    "docs/research/queries/2026-06-04-karpathy-agent-discipline.md",
    "docs/research/queries/2026-06-04-nvidia-skills-cherry-pick-review.md",
]

REQUIRED_MARKERS = {
    "docs/research/index.md": [
        "## Karpathy-style architecture mapping",
        "`operations.md` defines the ingest/query/lint loop",
        "`queries/index.md` ÔÇö inventory/contract for durable query answers",
    ],
    "docs/research/map.md": [
        "Agents working against the research wiki should read this file first",
        "## File back a query answer",
        "## Run a lint pass",
        "## Add a capability card",
        "## Add a scan/review/evidence pipeline",
        "## Add an evaluation/performance record",
        "## Run an endpoint security checklist",
    ],
    "docs/research/log.md": [
        "## Entry format",
        "## [2026-06-04] update | align product to full karpathy llm-wiki shape",
    ],
    "docs/research/operations.md": [
        "## Ingest",
        "## Query",
        "## Lint",
    ],
    "docs/research/sources/index.md": [
        "## Raw-source rule",
        "## Current source families",
    ],
    "docs/research/queries/index.md": [
        "## Current registry",
        "`2026-06-04-karpathy-agent-discipline.md`",
    ],
    "docs/research/lint/index.md": [
        "## Current registry",
    ],
    "docs/research/lint/2026-06-04-structure-health-check.md": [
        "## Scope",
        "## Findings",
    ],
    "docs/research/templates/query-template.md": [
        "## Question",
        "## Consulted surfaces",
    ],
    "docs/research/templates/lint-template.md": [
        "## Scope",
        "## Findings",
    ],
    "docs/research/templates/capability-card-template.md": [
        "## Trigger / when to use",
        "## Owner and compatibility",
        "## Version and provenance",
        "## Limitations",
        "## Scan / review / evidence state",
        "## Secret and data boundary",
        "## Promotion path",
    ],
    "docs/research/templates/evidence-pipeline-template.md": [
        "## Scan stage",
        "## Review stage",
        "## Evidence decision stage",
        "## Admission boundary",
    ],
    "docs/research/templates/evaluation-record-template.md": [
        "## Evaluation question",
        "## Artifact layout",
        "## Quality signals",
        "## Performance signals",
        "## Summary table",
        "## Failure table",
        "## Promotion decision",
    ],
    "docs/research/templates/endpoint-security-checklist-template.md": [
        "## Trust boundary",
        "## Endpoint trust confirmation",
        "## Auth and secret handling",
        "## No secrets in prompts",
        "## Egress and endpoint controls",
        "## Path/method scoped external calls",
        "## Validation evidence",
    ],
}


# Referential-integrity scope. Dated content pages in these sections must be registered
# in their section index.md; dangling-reference scanning is limited to the registries below,
# where backtick path semantics are consistent. Contradiction/staleness detection stays an
# agent task (see operations.md), not a script concern.
CONTENT_SECTIONS = ["queries", "lint", "artifacts", "experiments"]
REGISTRY_FILES = [
    "docs/research/map.md",
    "docs/research/queries/index.md",
    "docs/research/lint/index.md",
    "docs/research/artifacts/index.md",
    "docs/research/experiments/index.md",
    "docs/research/sources/index.md",
]
DATED_PAGE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-.*\.md$")
BACKTICK_MD_RE = re.compile(r"`([^`]*?\.md)`")


def _is_placeholder_ref(ref: str) -> bool:
    # Naming-convention placeholders in prose (e.g. `YYYY-MM-DD-{topic}.md`) are not links.
    return "{" in ref or "YYYY" in ref


def _reference_resolves(registry_dir: Path, ref: str) -> bool:
    ref_path = ref.split("#", 1)[0].strip()
    if not ref_path:
        return True
    for base in (registry_dir, RESEARCH_ROOT, REPO_ROOT):
        if (base / ref_path).exists():
            return True
    return False


def run_referential_checks() -> dict[str, Any]:
    unregistered_pages: list[str] = []
    dangling_references: list[dict[str, str]] = []

    for section in CONTENT_SECTIONS:
        section_dir = RESEARCH_ROOT / section
        index_path = section_dir / "index.md"
        if not index_path.exists():
            continue
        index_text = index_path.read_text(encoding="utf-8")
        for child in sorted(section_dir.glob("*.md")):
            if child.name == "index.md" or not DATED_PAGE_RE.match(child.name):
                continue
            if child.name not in index_text:
                unregistered_pages.append(f"{section}/{child.name}")

    for relative_path in REGISTRY_FILES:
        registry_path = REPO_ROOT / relative_path
        if not registry_path.exists():
            continue
        text = registry_path.read_text(encoding="utf-8")
        for ref in BACKTICK_MD_RE.findall(text):
            if _is_placeholder_ref(ref):
                continue
            if not _reference_resolves(registry_path.parent, ref):
                dangling_references.append({"registry": relative_path, "ref": ref})

    return {
        "referential_ok": not unregistered_pages and not dangling_references,
        "unregistered_pages": unregistered_pages,
        "dangling_references": dangling_references,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run structural checks for the local Genesis-Core-V2 research wiki"
    )
    parser.add_argument("--print-config", action="store_true")
    return parser


def build_runtime_config() -> dict[str, Any]:
    return {
        "repo_root": str(REPO_ROOT),
        "research_root": str(RESEARCH_ROOT),
        "required_paths": list(REQUIRED_PATHS),
        "marker_file_count": len(REQUIRED_MARKERS),
        "marker_count": sum(len(markers) for markers in REQUIRED_MARKERS.values()),
    }


def run_lint() -> int:
    missing_paths: list[str] = []
    missing_markers: list[dict[str, str]] = []

    for relative_path in REQUIRED_PATHS:
        if not (REPO_ROOT / relative_path).exists():
            missing_paths.append(relative_path)

    for relative_path, markers in REQUIRED_MARKERS.items():
        target_path = REPO_ROOT / relative_path
        if not target_path.exists():
            continue

        text = target_path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                missing_markers.append({"file": relative_path, "marker": marker})

    referential = run_referential_checks()

    payload = {
        # `ok` stays purely structural; referential findings are warn-only and do not gate it
        # or the exit code (the script is not wired into CI/pre-commit today).
        "ok": not missing_paths and not missing_markers,
        "repo_root": str(REPO_ROOT),
        "research_root": str(RESEARCH_ROOT),
        "checked_path_count": len(REQUIRED_PATHS),
        "checked_marker_count": sum(len(markers) for markers in REQUIRED_MARKERS.values()),
        "missing_paths": missing_paths,
        "missing_markers": missing_markers,
        "referential_ok": referential["referential_ok"],
        "unregistered_pages": referential["unregistered_pages"],
        "dangling_references": referential["dangling_references"],
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if payload["ok"] else 1


def main(argv: list[str] | None = None) -> int:
    parsed_args = build_parser().parse_args(argv)
    if parsed_args.print_config:
        print(json.dumps(build_runtime_config(), indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    return run_lint()


if __name__ == "__main__":
    raise SystemExit(main())
