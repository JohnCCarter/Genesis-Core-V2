"""Filesystem layout for the run-trace (ADR 0002).

TRACE_ROOT defaults to ``<repo>/results/trace`` (gitignored) and is overridable via the
``GENESIS_TRACE_ROOT`` environment variable. The root is resolved at call time so tests can
redirect it without import-order coupling.
"""

from __future__ import annotations

import os
from pathlib import Path

_ENV_TRACE_ROOT = "GENESIS_TRACE_ROOT"


def _resolve_repo_root() -> Path:
    """Resolve repo root deterministically from this module's location (never via cwd)."""

    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    # Fallback for unexpected layouts: <root>/src/core/trace/paths.py
    return here.parents[3]


_REPO_ROOT = _resolve_repo_root()


def trace_root() -> Path:
    override = os.environ.get(_ENV_TRACE_ROOT)
    if override:
        return Path(override)
    return _REPO_ROOT / "results" / "trace"


def run_dir(run_id: str, *, root: Path | None = None) -> Path:
    return (root if root is not None else trace_root()) / str(run_id)


def run_json_path(run_id: str, *, root: Path | None = None) -> Path:
    return run_dir(run_id, root=root) / "run.json"


def events_path(run_id: str, *, root: Path | None = None) -> Path:
    return run_dir(run_id, root=root) / "events.jsonl"


def index_path(*, root: Path | None = None) -> Path:
    return (root if root is not None else trace_root()) / "index.jsonl"
