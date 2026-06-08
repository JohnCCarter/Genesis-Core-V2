from __future__ import annotations

import tomllib
from pathlib import Path


def test_local_pyproject_tracks_expected_dev_tooling() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    pyproject = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))

    dev_dependencies = pyproject["project"]["optional-dependencies"]["dev"]
    assert "pytest>=8" in dev_dependencies
    assert "hypothesis>=6.0,<7" in dev_dependencies
    assert "pytest-regressions>=2.6,<3" in dev_dependencies
    assert "black>=24.10" in dev_dependencies
    assert "ruff>=0.6" in dev_dependencies
    assert "pre-commit>=3.0" in dev_dependencies
    assert "pip-audit>=2.8,<3" in dev_dependencies
