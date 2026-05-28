from __future__ import annotations

import ast
from pathlib import Path


_ADMITTED_FILES = [
    "src/core/server.py",
    "src/core/api/__init__.py",
    "src/core/api/account.py",
    "src/core/api/config.py",
    "src/core/api/info.py",
    "src/core/api/models.py",
    "src/core/api/paper.py",
    "src/core/api/public.py",
    "src/core/api/status.py",
    "src/core/api/strategy.py",
    "src/core/api/ui.py",
    "src/core/config/validator.py",
    "src/core/config/legacy_schema_v1.json",
    "tests/integration/test_config_endpoints.py",
]


_EXCLUDED_FILES = [
    "src/core/strategy/features.py",
    "config/runtime.json",
    "config/runtime.seed.json",
]

_EXCLUDED_PREFIXES = [
    "data",
]

_EXCLUDED_JSON_PAYLOAD_DIRS = [
    "config/strategy/champions",
]

_EXCLUDED_MODULE_PREFIXES = [
    "core.strategy.features",
]


def _is_excluded_module(module: str) -> bool:
    return any(
        module == prefix or module.startswith(f"{prefix}.")
        for prefix in _EXCLUDED_MODULE_PREFIXES
    )


def test_seed_contains_admitted_api_service_shell_slice() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _ADMITTED_FILES:
        assert (repo_root / relative_path).exists(), relative_path


def test_seed_excludes_legacy_and_stateful_surfaces() -> None:
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


def test_runtime_source_has_no_excluded_imports() -> None:
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
