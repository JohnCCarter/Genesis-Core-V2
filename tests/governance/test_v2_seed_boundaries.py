from __future__ import annotations

import ast
from pathlib import Path


_ADMITTED_FILES = [
    "src/core/server.py",
    "src/core/api/config.py",
    "src/core/api/models.py",
    "src/core/api/status.py",
    "src/core/api/strategy.py",
    "src/core/config/validator.py",
    "src/core/config/legacy_schema_v1.json",
    "tests/integration/test_config_endpoints.py",
]


_WORKFLOW_FILES = [
    ".github/copilot-instructions.md",
    "AGENTS.md",
    "docs/SKELETON_SCOPE.md",
]


_TASK_FILES = [
    ".vscode/tasks.json",
    "tests/runtime/test_local_vscode_tasks.py",
]


_MCP_FILES = [
    ".vscode/mcp.json",
    "config/mcp_settings.json",
    "mcp_server/__init__.py",
    "mcp_server/config.py",
    "mcp_server/resources.py",
    "mcp_server/server.py",
    "mcp_server/tools.py",
    "mcp_server/utils.py",
    "tests/runtime/test_local_mcp_setup.py",
]


_EXCLUDED_FILES = [
    "config/mcp_settings.remote_git.json",
    "config/mcp_settings.remote_safe.json",
    "mcp_server/remote_server.py",
    "src/core/api/account.py",
    "src/core/api/info.py",
    "src/core/api/paper.py",
    "src/core/api/public.py",
    "src/core/api/ui.py",
    "src/core/pipeline.py",
    "src/core/strategy/features.py",
    "src/core/utils/diffing/optuna_guard.py",
    "src/core/utils/diffing/results_diff.py",
    "src/core/utils/diffing/trial_cache.py",
    "src/core/utils/optuna_helpers.py",
    "config/runtime.json",
    "config/runtime.seed.json",
]

_EXCLUDED_PREFIXES = [
    "src/core/io",
    "src/core/optimizer",
    "data",
]

_EXCLUDED_JSON_PAYLOAD_DIRS = [
    "config/strategy/champions",
]

_EXCLUDED_MODULE_PREFIXES = [
    "core.api.account",
    "core.api.info",
    "core.api.paper",
    "core.api.public",
    "core.api.ui",
    "core.io",
    "core.optimizer",
    "core.pipeline",
    "core.strategy.features",
    "core.utils.diffing.optuna_guard",
    "core.utils.diffing.results_diff",
    "core.utils.diffing.trial_cache",
    "core.utils.optuna_helpers",
]


def _is_excluded_module(module: str) -> bool:
    return any(
        module == prefix or module.startswith(f"{prefix}.")
        for prefix in _EXCLUDED_MODULE_PREFIXES
    )


def test_seed_contains_admitted_local_api_shell_slice() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _ADMITTED_FILES:
        assert (repo_root / relative_path).exists(), relative_path


def test_seed_contains_skeleton_workflow_guidance() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _WORKFLOW_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    agents_text = (repo_root / "AGENTS.md").read_text(encoding="utf-8")
    instructions_text = (repo_root / ".github" / "copilot-instructions.md").read_text(
        encoding="utf-8"
    )
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "Prioritize V2 skeleton completeness before content migration." in agents_text
    assert "Prefer generator-driven changes in `Genesis-Core` over manual drift in this repo." in instructions_text
    assert "Track A — skeleton completeness" in scope_text
    assert "Track B — authority migration" in scope_text


def test_seed_contains_local_mcp_shell() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _MCP_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")
    assert "local MCP stdio shell" in scope_text
    assert "remote MCP surfaces remain deferred" in scope_text


def test_seed_contains_local_vscode_task_loop() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _TASK_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "Local VS Code tasks:" in readme
    assert "genesis-v2: api shell" in readme
    assert ".vscode/tasks.json" in scope_text


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
