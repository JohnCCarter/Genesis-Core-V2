from __future__ import annotations

import ast
import json
from pathlib import Path


_ADMITTED_FILES = [
    "src/core/server.py",
    "src/core/api/config.py",
    "src/core/api/info.py",
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


_SETTINGS_FILES = [
    ".vscode/settings.json",
    "tests/runtime/test_local_vscode_settings.py",
]


_ENV_TEMPLATE_FILES = [
    ".env.example",
    "tests/runtime/test_local_env_template.py",
]


_PRECOMMIT_FILES = [
    ".pre-commit-config.yaml",
    "tests/runtime/test_local_precommit_config.py",
]


_EXTENSIONS_FILES = [
    ".vscode/extensions.json",
    "tests/runtime/test_local_vscode_extensions.py",
]


_API_SCRIPT_FILES = [
    "scripts/api/api_shell.py",
    "tests/runtime/test_local_api_shell_script.py",
]


_INFO_ROUTE_FILES = [
    "src/core/api/info.py",
    "tests/runtime/test_local_info_endpoints.py",
]


_MCP_SCRIPT_FILES = [
    "scripts/mcp/mcp_stdio.py",
    "tests/runtime/test_local_mcp_script.py",
]


_PYTEST_SCRIPT_FILES = [
    "scripts/validate/pytest_suite.py",
    "tests/runtime/test_local_pytest_script.py",
]


_SCRIPT_FILES = [
    "scripts/smoke/backtest_smoke.py",
    "scripts/smoke/champion_smoke.py",
    "scripts/smoke/evaluate_champion_smoke.py",
    "scripts/smoke/fixture_smoke.py",
    "scripts/smoke/model_smoke.py",
    "scripts/smoke/smoke_suite.py",
    "tests/runtime/test_local_smoke_scripts.py",
]


_CONSOLE_SCRIPT_FILES = [
    "pyproject.toml",
    "src/genesis_core_v2_cli/console_scripts.py",
    "tests/governance/test_pyproject_console_scripts.py",
    "tests/runtime/test_installed_console_scripts.py",
]


_INSTALL_VERIFICATION_FILES = [
    "seed_manifest.json",
    "tests/runtime/test_installed_console_scripts.py",
]


_WORKSPACE_VERIFICATION_FILES = [
    "seed_manifest.json",
    ".vscode/tasks.json",
    ".vscode/launch.json",
    ".vscode/settings.json",
    ".vscode/extensions.json",
    "tests/runtime/test_local_vscode_tasks.py",
    "tests/runtime/test_local_vscode_launch.py",
    "tests/runtime/test_local_vscode_settings.py",
    "tests/runtime/test_local_vscode_extensions.py",
]


_BOOTSTRAP_VERIFICATION_FILES = [
    "seed_manifest.json",
    ".env.example",
    ".pre-commit-config.yaml",
    "tests/runtime/test_local_env_template.py",
    "tests/runtime/test_local_precommit_config.py",
]


_MCP_VERIFICATION_FILES = [
    "seed_manifest.json",
    ".vscode/mcp.json",
    "config/mcp_settings.json",
    "scripts/mcp/mcp_stdio.py",
    "tests/runtime/test_local_mcp_setup.py",
    "tests/runtime/test_local_mcp_script.py",
]


_REMOTE_MCP_VERIFICATION_FILES = [
    "seed_manifest.json",
    "config/mcp_settings.remote_git.json",
    "config/mcp_settings.remote_safe.json",
    "mcp_server/remote_server.py",
    "tests/governance/test_mcp_remote_authorization.py",
    "tests/integration/test_mcp_git_status_remote_filters.py",
    "tests/integration/test_mcp_remote_git_workflow_confirm.py",
    "tests/utils/test_remote_server_fastmcp_sse_alias.py",
]


_PIPELINE_VERIFICATION_FILES = [
    "seed_manifest.json",
    "src/core/pipeline.py",
    "src/core/utils/random_seeds.py",
    "tests/runtime/test_pipeline_defaults.py",
]


_BACKTEST_COMPARISON_VERIFICATION_FILES = [
    "seed_manifest.json",
    "src/core/utils/diffing/results_diff.py",
    "tools/compare_backtest_results.py",
    "tests/backtest/test_compare_backtest_results.py",
    "tests/utils/diffing/test_results_diff.py",
]


_CONFIG_AUTHORITY_VERIFICATION_FILES = [
    "seed_manifest.json",
    "src/core/api/config.py",
    "src/core/config/authority.py",
    "src/core/config/authority_mode_resolver.py",
    "src/core/config/schema.py",
    "tests/governance/test_authority_mode_resolver.py",
    "tests/integration/test_config_endpoints.py",
    "tests/runtime/test_config_authority_semantics.py",
]


_STRATEGY_AUTHORITY_VERIFICATION_FILES = [
    "seed_manifest.json",
    "src/core/config/authority_mode_resolver.py",
    "src/core/strategy/family_registry.py",
    "src/core/strategy/family_admission.py",
    "src/core/strategy/run_intent.py",
    "tests/core/strategy/test_families.py",
    "tests/core/strategy/test_family_admission.py",
    "tests/runtime/test_strategy_authority.py",
]


_DETERMINISM_VERIFICATION_FILES = [
    "seed_manifest.json",
    "tests/governance/test_pipeline_fast_hash_guard.py",
    "tests/utils/test_features_asof_cache_key_deterministic.py",
]


_RUNTIME_GUARDRAIL_FILES = [
    "tests/governance/test_no_legacy_feature_imports.py",
    "tests/governance/test_dead_code_tripwires.py",
]


_MODULE_LOOP_FILES = [
    "src/core/server.py",
    "mcp_server/server.py",
    "scripts/validate/pytest_suite.py",
    "src/core/bootstrap/model_smoke.py",
    "src/core/bootstrap/smoke_suite.py",
    "tests/runtime/test_installed_console_scripts.py",
]


_LAUNCH_FILES = [
    ".vscode/launch.json",
    "tests/runtime/test_local_vscode_launch.py",
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
    "src/core/api/account.py",
    "src/core/api/paper.py",
    "src/core/api/public.py",
    "src/core/api/ui.py",
    "src/core/strategy/features.py",
    "src/core/utils/diffing/optuna_guard.py",
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
    "core.api.paper",
    "core.api.public",
    "core.api.ui",
    "core.io",
    "core.optimizer",
    "core.strategy.features",
    "core.utils.diffing.optuna_guard",
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
    assert "constrained remote MCP HTTP semantics without deployment helpers" in scope_text


def test_seed_contains_local_mcp_script() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _MCP_SCRIPT_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "Non-installed local MCP launcher:" in readme
    assert "scripts/mcp/mcp_stdio.py" in readme
    assert "scripts/mcp/mcp_stdio.py" in scope_text


def test_seed_contains_local_vscode_task_loop() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _TASK_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "Local VS Code tasks:" in readme
    assert "genesis-v2: api shell" in readme
    assert "genesis-v2: mcp stdio" in readme
    assert "genesis-v2: pytest" in readme
    assert "genesis-v2: mcp stdio" in scope_text
    assert ".vscode/tasks.json" in scope_text


def test_seed_contains_local_vscode_settings() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _SETTINGS_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert ".vscode/settings.json" in readme
    assert "Python analysis/test settings" in readme
    assert ".vscode/settings.json" in scope_text


def test_seed_contains_local_env_template() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _ENV_TEMPLATE_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert ".env.example" in readme
    assert "tracked env bootstrap template" in readme
    assert ".env.example" in scope_text


def test_seed_contains_local_precommit_workflow() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _PRECOMMIT_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert ".pre-commit-config.yaml" in readme
    assert "Local pre-commit workflow" in readme
    assert ".pre-commit-config.yaml" in scope_text


def test_seed_contains_local_vscode_extensions() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _EXTENSIONS_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert ".vscode/extensions.json" in readme
    assert "Suggested VS Code extensions" in readme
    assert ".vscode/extensions.json" in scope_text


def test_seed_contains_local_api_shell_script() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _API_SCRIPT_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "Non-installed local API launcher:" in readme
    assert "scripts/api/api_shell.py" in readme
    assert "scripts/api/api_shell.py" in scope_text


def test_seed_contains_local_info_routes() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _INFO_ROUTE_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "src/core/api/{config,info,models,status,strategy}.py" in readme
    assert "local-only API shell (`config`, `info`, `status`, `models`, `strategy`)" in scope_text


def test_seed_contains_local_pytest_script() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _PYTEST_SCRIPT_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "Non-installed local pytest launcher:" in readme
    assert "scripts/validate/pytest_suite.py" in readme
    assert "scripts/validate/pytest_suite.py" in scope_text


def test_seed_contains_local_smoke_scripts() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _SCRIPT_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "Non-installed local smoke scripts:" in readme
    assert "scripts/smoke/evaluate_champion_smoke.py" in readme
    assert "scripts/smoke/model_smoke.py" in readme
    assert "scripts/smoke/smoke_suite.py" in readme
    assert "scripts/smoke/model_smoke.py" in scope_text
    assert "scripts/smoke/*.py" in scope_text


def test_seed_contains_installed_console_script_loop() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _CONSOLE_SCRIPT_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "Console scripts after editable install:" in readme
    assert "genesis-v2-api-shell" in readme
    assert "genesis-v2-model-smoke" in readme
    assert "genesis-v2-api-shell" in scope_text
    assert "genesis-v2-model-smoke" in scope_text
    assert 'python -m pip install -e ".[dev,mcp]"' in scope_text
    assert "tests/runtime/test_installed_console_scripts.py" in scope_text


def test_seed_contains_install_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _INSTALL_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["install_verification"] == {
        "editable_install_command": 'python -m pip install -e ".[dev,mcp]"',
        "installed_console_script_test_command": "pytest tests/runtime/test_installed_console_scripts.py -q",
        "installed_console_script_test_file": "tests/runtime/test_installed_console_scripts.py",
        "optional_mcp_install_command": 'python -m pip install -e ".[mcp]"',
    }
    assert manifest["install_verification"]["editable_install_command"] in readme
    assert manifest["install_verification"]["editable_install_command"] in scope_text
    assert manifest["install_verification"]["installed_console_script_test_command"] in readme
    assert manifest["install_verification"]["installed_console_script_test_command"] in scope_text


def test_seed_contains_workspace_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _WORKSPACE_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))

    assert manifest["workspace_verification"] == {
        "extensions": {
            "runtime_test_file": "tests/runtime/test_local_vscode_extensions.py",
            "workspace_file": ".vscode/extensions.json",
        },
        "launch": {
            "runtime_test_file": "tests/runtime/test_local_vscode_launch.py",
            "workspace_file": ".vscode/launch.json",
        },
        "settings": {
            "runtime_test_file": "tests/runtime/test_local_vscode_settings.py",
            "workspace_file": ".vscode/settings.json",
        },
        "tasks": {
            "runtime_test_file": "tests/runtime/test_local_vscode_tasks.py",
            "workspace_file": ".vscode/tasks.json",
        },
    }


def test_seed_contains_bootstrap_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _BOOTSTRAP_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))

    assert manifest["bootstrap_verification"] == {
        "env_template": {
            "runtime_test_file": "tests/runtime/test_local_env_template.py",
            "tracked_file": ".env.example",
        },
        "precommit": {
            "runtime_test_file": "tests/runtime/test_local_precommit_config.py",
            "tracked_file": ".pre-commit-config.yaml",
        },
    }


def test_seed_contains_mcp_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _MCP_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))

    assert manifest["mcp_verification"] == {
        "workspace_registration": {
            "workspace_file": ".vscode/mcp.json",
            "config_file": "config/mcp_settings.json",
            "runtime_test_file": "tests/runtime/test_local_mcp_setup.py",
        },
        "local_launcher": {
            "tracked_file": "scripts/mcp/mcp_stdio.py",
            "runtime_test_file": "tests/runtime/test_local_mcp_script.py",
        },
    }


def test_seed_contains_remote_mcp_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _REMOTE_MCP_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")
    remote_safe = json.loads(
        (repo_root / "config" / "mcp_settings.remote_safe.json").read_text(encoding="utf-8")
    )
    remote_git = json.loads(
        (repo_root / "config" / "mcp_settings.remote_git.json").read_text(encoding="utf-8")
    )

    assert manifest["remote_mcp_verification"] == {
        "authorization_and_transport": {
            "module_file": "mcp_server/remote_server.py",
            "auth_test_file": "tests/governance/test_mcp_remote_authorization.py",
            "transport_test_file": "tests/utils/test_remote_server_fastmcp_sse_alias.py",
        },
        "remote_git_workflow": {
            "config_file": "config/mcp_settings.remote_git.json",
            "confirm_test_file": "tests/integration/test_mcp_remote_git_workflow_confirm.py",
        },
        "remote_safe_config": {
            "config_file": "config/mcp_settings.remote_safe.json",
            "filter_test_file": "tests/integration/test_mcp_git_status_remote_filters.py",
        },
    }
    assert remote_safe["features"] == {
        "code_execution": False,
        "file_operations": True,
        "git_integration": True,
    }
    assert remote_git["features"] == {
        "code_execution": True,
        "file_operations": True,
        "git_integration": True,
    }
    assert ".github" not in remote_safe["security"]["allowed_paths"]
    assert ".github" in remote_git["security"]["allowed_paths"]
    assert "results" not in remote_safe["security"]["allowed_paths"]
    assert "results" in remote_git["security"]["allowed_paths"]
    assert remote_safe["security"]["max_file_size_mb"] == 5
    assert remote_git["security"]["max_file_size_mb"] == 10
    assert "config/runtime.json" in remote_safe["security"]["blocked_patterns"]
    assert "config/runtime.json" in remote_git["security"]["blocked_patterns"]
    assert not (repo_root / "scripts" / "mcp" / "start_mcp_remote.ps1").exists()
    assert not (repo_root / "scripts" / "mcp_session_preflight.py").exists()
    assert "Genesis-Core-V2 admits constrained remote MCP semantics limited to authorization, safe-mode," in readme
    assert "Genesis-Core-V2 admits constrained remote MCP semantics limited to authorization, safe-mode," in scope_text


def test_seed_contains_pipeline_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _PIPELINE_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["pipeline_verification"] == {
        "defaults_and_seeding": {
            "module_file": "src/core/pipeline.py",
            "seed_helper_file": "src/core/utils/random_seeds.py",
            "runtime_test_file": "tests/runtime/test_pipeline_defaults.py",
        }
    }
    assert "runtime pipeline orchestration (`src/core/pipeline.py`)" in readme
    assert "src/core/pipeline.py" in scope_text


def test_seed_contains_backtest_comparison_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    diffing_init = repo_root / "src" / "core" / "utils" / "diffing" / "__init__.py"

    for relative_path in _BACKTEST_COMPARISON_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["backtest_comparison_verification"] == {
        "compare_tool": {
            "module_file": "tools/compare_backtest_results.py",
            "test_file": "tests/backtest/test_compare_backtest_results.py",
        },
        "results_diff": {
            "module_file": "src/core/utils/diffing/results_diff.py",
            "test_file": "tests/utils/diffing/test_results_diff.py",
        },
    }
    assert not (repo_root / "scripts" / "run" / "run_backtest.py").exists()
    init_text = diffing_init.read_text(encoding="utf-8")
    assert "results_diff" not in init_text
    assert "optuna_guard" not in init_text
    assert "trial_cache" not in init_text
    assert "Backtest comparison/diff semantics and associated tmp-path-isolated tests are admitted" in readme
    assert "Backtest comparison/diff semantics and associated tmp-path-isolated tests are admitted" in scope_text


def test_seed_contains_config_authority_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _CONFIG_AUTHORITY_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["config_authority_verification"] == {
        "authority_mode_resolver": {
            "module_file": "src/core/config/authority_mode_resolver.py",
            "test_file": "tests/governance/test_authority_mode_resolver.py",
        },
        "runtime_authority_semantics": {
            "api_file": "src/core/api/config.py",
            "authority_file": "src/core/config/authority.py",
            "runtime_test_file": "tests/runtime/test_config_authority_semantics.py",
            "schema_file": "src/core/config/schema.py",
            "validate_smoke_test_file": "tests/integration/test_config_endpoints.py",
        },
    }
    assert "Config runtime-authority semantics are admitted for source/verification purposes only" in readme
    assert "Config runtime-authority semantics are admitted for source/verification purposes only" in scope_text


def test_seed_contains_strategy_authority_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _STRATEGY_AUTHORITY_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["strategy_authority_verification"] == {
        "authority_mode_resolver": {
            "module_file": "src/core/config/authority_mode_resolver.py",
            "runtime_test_file": "tests/runtime/test_strategy_authority.py",
        },
        "family_admission": {
            "module_file": "src/core/strategy/family_admission.py",
            "run_intent_file": "src/core/strategy/run_intent.py",
            "test_file": "tests/core/strategy/test_family_admission.py",
        },
        "family_registry": {
            "module_file": "src/core/strategy/family_registry.py",
            "test_file": "tests/core/strategy/test_families.py",
        },
    }
    assert "admitted strategy authority helpers" in readme
    assert "admitted strategy authority helpers" in scope_text


def test_seed_contains_determinism_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _DETERMINISM_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["determinism_verification"] == {
        "feature_cache_hash_stability": {
            "test_file": "tests/utils/test_features_asof_cache_key_deterministic.py"
        },
        "pipeline_fast_hash_guard": {
            "test_file": "tests/governance/test_pipeline_fast_hash_guard.py"
        },
    }
    assert "runtime determinism guardrails" in readme
    assert "runtime determinism guardrails" in scope_text


def test_seed_contains_runtime_governance_guardrails() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _RUNTIME_GUARDRAIL_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    assert "runtime-only governance guardrails" in readme


def test_seed_contains_editable_install_module_loop() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _MODULE_LOOP_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "python -m uvicorn core.server:app --app-dir src --reload" in readme
    assert "python -m mcp_server.server" in readme
    assert "python -m pytest -q" in readme
    assert "python -m core.bootstrap.model_smoke" in readme
    assert "python -m core.bootstrap.smoke_suite" in readme
    assert "python -m uvicorn core.server:app --app-dir src --reload" in scope_text
    assert "python -m mcp_server.server" in scope_text
    assert "python -m pytest -q" in scope_text
    assert "python -m core.bootstrap.model_smoke" in scope_text
    assert "python -m core.bootstrap.smoke_suite" in scope_text


def test_seed_contains_local_vscode_launch_loop() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _LAUNCH_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "Local VS Code debug profiles:" in readme
    assert "genesis-v2: mcp stdio" in readme
    assert "genesis-v2: smoke suite" in readme
    assert "genesis-v2: mcp stdio" in scope_text
    assert ".vscode/launch.json" in scope_text


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
