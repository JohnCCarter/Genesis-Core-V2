from __future__ import annotations

import re
import tomllib
from pathlib import Path


def _package_name(spec: str) -> str:
    """Extract the PEP 508 package name from a dependency spec (drop version,
    extras, markers) so the guard tracks the tool, not its pinned version."""
    return re.split(r"[<>=!~;\[ ]", spec, maxsplit=1)[0].strip().lower()


def test_local_pyproject_tracks_expected_dev_tooling() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    pyproject = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))

    dev_dependencies = pyproject["project"]["optional-dependencies"]["dev"]
    # Match by package name, not exact version spec, so Dependabot version bumps
    # do not break this guard — it asserts the tools are tracked, not their pins.
    names = {_package_name(spec) for spec in dev_dependencies}
    expected = {
        "pytest",
        "httpx2",
        "hypothesis",
        "pytest-regressions",
        "black",
        "ruff",
        "pre-commit",
        "pip-audit",
    }
    missing = expected - names
    assert not missing, f"missing dev tools in [dev] extra: {sorted(missing)}"
