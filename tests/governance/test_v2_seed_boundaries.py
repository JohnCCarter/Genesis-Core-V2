from __future__ import annotations

import ast
from pathlib import Path


_EXCLUDED_FILES = [
    "src/core/server.py",
    "src/core/strategy/features.py",
    "src/core/config/validator.py",
    "config/runtime.json",
    "config/runtime.seed.json",
]

_EXCLUDED_PREFIXES = [
    "src/core/api",
    "data",
]

_EXCLUDED_JSON_PAYLOAD_DIRS = [
    "config/strategy/champions",
]

_EXCLUDED_MODULE_PREFIXES = [
    "core.server",
    "core.api",
    "core.strategy.features",
    "core.config.validator",
]


def _is_excluded_module(module: str) -> bool:
    return any(
        module == prefix or module.startswith(f"{prefix}.")
        for prefix in _EXCLUDED_MODULE_PREFIXES
    )


def test_phase_one_seed_excludes_service_and_legacy_surfaces() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _EXCLUDED_FILES:
        assert not (repo_root / relative_path).exists(), relative_path

    for prefix in _EXCLUDED_PREFIXES:
        assert not (repo_root / prefix).exists(), prefix


def test_phase_one_seed_has_no_excluded_json_payloads() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_dir in _EXCLUDED_JSON_PAYLOAD_DIRS:
        candidate_dir = repo_root / relative_dir
        if not candidate_dir.exists():
            continue
        leaked = sorted(path.relative_to(repo_root).as_posix() for path in candidate_dir.rglob("*.json"))
        assert not leaked, relative_dir + "\n" + "\n".join(leaked)


def test_runtime_source_has_no_service_or_legacy_imports() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    src_root = repo_root / "src"
    assert src_root.exists()

    violations: list[str] = []
    for path in src_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        rel_path = path.relative_to(repo_root).as_posix()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported = alias.name
                    if _is_excluded_module(imported):
                        violations.append(f"{rel_path}:{node.lineno} import {imported}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if _is_excluded_module(module):
                    violations.append(f"{rel_path}:{node.lineno} from {module}")

    assert not violations, "Excluded import found:\n" + "\n".join(violations)
