from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

_ADMITTED_FILES = [
    "src/core/server.py",
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


_WORKFLOW_FILES = [
    ".github/copilot-instructions.md",
    "AGENTS.md",
    "docs/SKELETON_SCOPE.md",
]


_ADR_FILES = [
    "docs/adr/0000-template.md",
    "docs/adr/README.md",
]


_ISSUE_TEMPLATE_FILES = [
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
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


_AUDIT_SCRIPT_FILES = [
    "scripts/audit/pip_audit.py",
    "tests/runtime/test_local_pip_audit_script.py",
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


_FETCH_SCRIPT_FILES = [
    "scripts/data/fetch_historical.py",
    "tests/runtime/test_local_fetch_historical_script.py",
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


_ACCOUNT_API_VERIFICATION_FILES = [
    "seed_manifest.json",
    "src/core/api/account.py",
    "src/core/server.py",
    "tests/runtime/test_account_endpoints.py",
]


_PAPER_UI_VERIFICATION_FILES = [
    "seed_manifest.json",
    "src/core/api/paper.py",
    "src/core/api/ui.py",
    "src/core/server.py",
    "tests/runtime/test_paper_endpoints.py",
    "tests/runtime/test_ui_endpoints.py",
]


_STATEFUL_AUTHORITY_VERIFICATION_FILES = [
    "seed_manifest.json",
    "config/runtime.seed.json",
    "config/strategy/champions/tBTCUSD_1h.json",
    "config/strategy/champions/tBTCUSD_3h.json",
    "src/core/strategy/champion_loader.py",
    "tests/runtime/test_stateful_authority_payloads.py",
]


_TRANSPORT_READ_VERIFICATION_FILES = [
    "seed_manifest.json",
    "src/core/io/__init__.py",
    "src/core/io/bitfinex/__init__.py",
    "src/core/io/bitfinex/exchange_client.py",
    "src/core/io/bitfinex/read_helpers.py",
    "src/core/io/bitfinex/rest_public.py",
    "src/core/io/bitfinex/rest_auth.py",
    "src/core/io/bitfinex/ws_public.py",
    "src/core/io/bitfinex/ws_auth.py",
    "src/core/io/bitfinex/ws_reconnect.py",
    "tests/runtime/test_transport_read_spine.py",
    "tests/runtime/test_transport_route_inertness.py",
    "tests/utils/test_bitfinex_transport_imports.py",
    "tests/utils/test_rest_auth_routes_to_exchange_client.py",
    "tests/utils/test_rest_public_min.py",
    "tests/utils/test_ws_auth_min.py",
    "tests/utils/test_ws_public_min.py",
    "tests/utils/test_ws_reconnect.py",
]


_PUBLIC_API_VERIFICATION_FILES = [
    "seed_manifest.json",
    "src/core/api/public.py",
    "src/core/server.py",
    "tests/runtime/test_public_candles_endpoint.py",
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


_OPTIMIZER_PACKAGE_VERIFICATION_FILES = [
    "seed_manifest.json",
    "src/core/optimizer/__init__.py",
    "src/core/optimizer/champion.py",
    "src/core/optimizer/constraints.py",
    "src/core/optimizer/param_transforms.py",
    "src/core/optimizer/runner.py",
    "src/core/optimizer/runner_config.py",
    "src/core/optimizer/runner_optuna_orchestration.py",
    "src/core/optimizer/runner_trial_backtest.py",
    "src/core/optimizer/runner_trial_results.py",
    "src/core/optimizer/runner_validation.py",
    "src/core/optimizer/scoring.py",
    "src/core/utils/optuna_helpers.py",
    "src/core/utils/diffing/config_equivalence.py",
    "src/core/utils/diffing/optuna_guard.py",
    "src/core/utils/diffing/trial_cache.py",
    "scripts/audit/audit_optuna_objective_parity.py",
    "tests/governance/test_import_smoke_backtest_optuna.py",
    "tests/utils/diffing/test_config_equivalence.py",
    "tests/utils/diffing/test_optuna_diff.py",
    "tests/utils/test_optimizer_champion.py",
    "tests/utils/test_optimizer_direct_execution_canonical_guard.py",
    "tests/utils/test_optimizer_duplicate_fixes.py",
    "tests/utils/test_optimizer_json_cache_env_flag.py",
    "tests/utils/test_optimizer_param_transforms.py",
    "tests/utils/test_optimizer_param_transforms_dirichlet.py",
    "tests/utils/test_optimizer_performance.py",
    "tests/utils/test_optimizer_runner.py",
    "tests/utils/test_optuna_config_cache.py",
    "tests/utils/test_optuna_rdbstorage_engine_kwargs.py",
    "tests/utils/test_optuna_resume_signature.py",
    "tests/utils/test_set_global_seeds_parity.py",
]


_OPTIMIZER_CONFIG_ADMISSION_FILES = [
    "seed_manifest.json",
    "config/optimizer/README.md",
    "config/optimizer/1h/tBTCUSD_1h_coarse_grid.yaml",
    "config/optimizer/1h/tBTCUSD_1h_risk_optuna_smoke.yaml",
    "config/optimizer/1h/phased_v1/tBTCUSD_1h_phased_v1_fib_gate_matrix.yaml",
    "config/optimizer/1h/phased_v1/tBTCUSD_1h_phased_v1_phaseA.yaml",
    "config/optimizer/1h/phased_v1/tBTCUSD_1h_phased_v1_phaseB.yaml",
    "config/optimizer/1h/phased_v1/tBTCUSD_1h_phased_v1_phaseB_seeded.yaml",
    "config/optimizer/1h/phased_v1/tBTCUSD_1h_phased_v1_phaseC_seeded_oos.yaml",
    "config/optimizer/3h/tBTCUSD_3h_explore_validate_2024_2025.yaml",
    "config/optimizer/3h/phased_v3/PHASED_V3_RESULTS.md",
    "config/optimizer/3h/phased_v3/tBTCUSD_3h_phased_v3_phaseA.yaml",
    "config/optimizer/3h/phased_v3/tBTCUSD_3h_phased_v3_phaseB.yaml",
    "config/optimizer/3h/phased_v3/tBTCUSD_3h_phased_v3_phaseC.yaml",
    "config/optimizer/3h/phased_v3/tBTCUSD_3h_phased_v3_phaseD.yaml",
    "config/optimizer/3h/phased_v3/tBTCUSD_3h_phased_v3_phaseE_oos.yaml",
    "config/optimizer/3h/phased_v3/best_trials/phaseA_best_trial.json",
    "config/optimizer/3h/phased_v3/best_trials/phaseB_v2_best_trial.json",
    "config/optimizer/3h/phased_v3/best_trials/phaseB_v3_best_trial.json",
    "config/optimizer/3h/phased_v3/best_trials/phaseC_oos_trial.json",
    "config/optimizer/3h/ri_train_validate_blind_v1/tBTCUSD_3h_ri_train_validate_2023_2024_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_challenger_family_slice2_2024_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_challenger_family_slice3_2024_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_challenger_family_slice4_2024_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_challenger_family_slice5_2024_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_challenger_family_slice6_2024_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_challenger_family_slice7_2024_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_challenger_family_slice8_2024_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_challenger_family_slice8_cross_regime_oos_2025_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_challenger_family_slice9_2024_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_challenger_family_slice10_2024_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_decision_ev_edge_slice1_2024_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_decision_ev_edge_slice1_smoke_20260327.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_decision_risk_state_transition_guard_slice1_2024_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_decision_risk_state_transition_guard_slice1_smoke_20260327.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_signal_regime_definition_slice1_2024_v1.yaml",
    "config/optimizer/3h/ri_challenger_family_v1/tBTCUSD_3h_ri_signal_slice1_2024_v1.yaml",
    "config/optimizer/6h/PHASED_NORMALIZATION_PLAN.md",
    "config/optimizer/6h/phased_v1/tBTCUSD_6h_phased_v1_debug_baseline.yaml",
    "config/optimizer/6h/phased_v1/tBTCUSD_6h_phased_v1_phaseA.yaml",
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
    "src/core/strategy/features.py",
    "scripts/run/run_backtest.py",
    "scripts/preflight/preflight_optuna_check.py",
    "scripts/validate/validate_optimizer_config.py",
    "config/runtime.json",
    "config/strategy/champions/tBTCUSD_1h_quality_v2_candidate_scoped.json",
    "config/strategy/champions/tBTCUSD_1h_quality_v2_candidate_scoped_relaxed_size.json",
    "config/strategy/champions/tTEST_1h.json",
]

_EXCLUDED_PREFIXES = [
    "config/strategy/candidates",
    "data",
    "scripts/optimize",
]

_EXCLUDED_JSON_PAYLOAD_DIRS = [
    "config/strategy/champions/backup",
]

_EXCLUDED_MODULE_PREFIXES = [
    "core.io",
    "core.strategy.features",
]


_EXPLICIT_TRANSPORT_MODULE_ADMISSIONS = [
    "core.io.bitfinex.exchange_client",
    "core.io.bitfinex.read_helpers",
    "core.io.bitfinex.rest_public",
    "core.io.bitfinex.rest_auth",
    "core.io.bitfinex.ws_public",
    "core.io.bitfinex.ws_auth",
    "core.io.bitfinex.ws_reconnect",
]

_EXPLICIT_TRANSPORT_PACKAGE_MODULES = [
    "core.io.bitfinex",
]


def _is_excluded_module(module: str) -> bool:
    if module in _EXPLICIT_TRANSPORT_PACKAGE_MODULES:
        return False
    if any(
        module == admitted or module.startswith(f"{admitted}.")
        for admitted in _EXPLICIT_TRANSPORT_MODULE_ADMISSIONS
    ):
        return False
    return any(
        module == prefix or module.startswith(f"{prefix}.") for prefix in _EXCLUDED_MODULE_PREFIXES
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
    assert (
        "Prefer generator-driven changes in `Genesis-Core` over manual drift in this repo."
        in instructions_text
    )
    assert "Track A — skeleton completeness" in scope_text
    assert "Track B — authority migration" in scope_text


def test_seed_contains_adr_template_workflow() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _ADR_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["adr_verification"] == {
        "template": {
            "tracked_files": [
                "docs/adr/0000-template.md",
                "docs/adr/README.md",
            ],
            "governance_test_file": "tests/governance/test_v2_seed_boundaries.py",
        }
    }
    assert "docs/adr/0000-template.md" in readme
    assert "docs/adr/0000-template.md" in scope_text


def test_seed_contains_issue_template_workflow() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _ISSUE_TEMPLATE_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["issue_template_verification"] == {
        "tracked_files": [
            ".github/ISSUE_TEMPLATE/bug_report.yml",
            ".github/ISSUE_TEMPLATE/feature_request.yml",
            ".github/ISSUE_TEMPLATE/config.yml",
        ],
        "governance_test_file": "tests/governance/test_v2_seed_boundaries.py",
    }
    assert ".github/ISSUE_TEMPLATE/*.yml" in readme
    assert ".github/ISSUE_TEMPLATE/*.yml" in scope_text


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


def test_seed_contains_local_dependency_audit_script() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _AUDIT_SCRIPT_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["audit_verification"] == {
        "dependency_audit": {
            "runtime_test_file": "tests/runtime/test_local_pip_audit_script.py",
            "tracked_file": "scripts/audit/pip_audit.py",
        }
    }
    assert "scripts/audit/pip_audit.py" in readme
    assert "scripts/audit/pip_audit.py" in scope_text
    assert "uv run python scripts/audit/pip_audit.py" in readme
    assert "python scripts/audit/pip_audit.py" in scope_text


def test_seed_contains_local_info_routes() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _INFO_ROUTE_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "src/core/api/{account,config,info,models,paper,public,status,strategy,ui}.py" in readme
    assert (
        "local-only API shell (`account`, `config`, `info`, `status`, `models`, `paper`, `public`, `strategy`, `ui`)"
        in scope_text
    )


def test_seed_contains_local_pytest_script() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _PYTEST_SCRIPT_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "Non-installed local pytest launcher:" in readme
    assert "scripts/validate/pytest_suite.py" in readme
    assert "scripts/validate/pytest_suite.py" in scope_text


def test_seed_contains_local_fetch_historical_script() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _FETCH_SCRIPT_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert "scripts/data/fetch_historical.py" in readme
    assert "scripts/data/fetch_historical.py" in scope_text


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
    assert 'uv sync --extra dev --extra mcp' in scope_text
    assert "tests/runtime/test_installed_console_scripts.py" in scope_text


def test_seed_contains_install_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _INSTALL_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["install_verification"] == {
        "editable_install_command": 'uv sync --extra dev --extra mcp',
        "installed_console_script_test_command": "uv run pytest tests/runtime/test_installed_console_scripts.py -q",
        "installed_console_script_test_file": "tests/runtime/test_installed_console_scripts.py",
        "optional_mcp_install_command": 'uv sync --extra mcp',
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
    assert (
        "Genesis-Core-V2 admits constrained remote MCP semantics limited to authorization, safe-mode,"
        in readme
    )
    assert (
        "Genesis-Core-V2 admits constrained remote MCP semantics limited to authorization, safe-mode,"
        in scope_text
    )


def test_seed_contains_account_api_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    account_text = (repo_root / "src" / "core" / "api" / "account.py").read_text(encoding="utf-8")

    for relative_path in _ACCOUNT_API_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["account_api_verification"] == {
        "read_only_account_routes": {
            "module_file": "src/core/api/account.py",
            "runtime_test_file": "tests/runtime/test_account_endpoints.py",
            "server_hook_file": "src/core/server.py",
        }
    }
    assert "core.io" not in account_text
    assert (
        "Batch E2 admits only the read-only account endpoint semantics from `src/core/api/account.py` through an injected `core.server.bfx_read` seam for offline verification."
        in readme
    )
    assert (
        "Batch E2 admits only the read-only account endpoint semantics from `src/core/api/account.py` through an injected `core.server.bfx_read` seam for offline verification."
        in scope_text
    )


def test_seed_contains_public_api_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _PUBLIC_API_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["public_api_verification"] == {
        "public_candles": {
            "module_file": "src/core/api/public.py",
            "runtime_test_file": "tests/runtime/test_public_candles_endpoint.py",
            "server_hook_file": "src/core/server.py",
        }
    }
    assert (
        "Batch E1 admits the public candles endpoint semantics from `src/core/api/public.py` through an injected `core.server.get_exchange_client` seam for offline verification while broader transport remains deferred."
        in readme
    )
    assert (
        "Batch E1 admits the public candles endpoint semantics from `src/core/api/public.py` through an injected `core.server.get_exchange_client` seam for offline verification while broader transport remains deferred."
        in scope_text
    )


def test_seed_contains_paper_ui_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    paper_text = (repo_root / "src" / "core" / "api" / "paper.py").read_text(encoding="utf-8")
    server_text = (repo_root / "src" / "core" / "server.py").read_text(encoding="utf-8")

    for relative_path in _PAPER_UI_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["paper_ui_verification"] == {
        "paper_routes": {
            "module_file": "src/core/api/paper.py",
            "runtime_test_file": "tests/runtime/test_paper_endpoints.py",
            "server_hook_file": "src/core/server.py",
        },
        "ui_route": {
            "module_file": "src/core/api/ui.py",
            "runtime_test_file": "tests/runtime/test_ui_endpoints.py",
            "server_hook_file": "src/core/server.py",
        },
    }
    assert "core.io" not in paper_text
    assert "paper_router" in server_text
    assert "ui_router" in server_text
    assert "auth/w/order/submit" not in server_text
    assert (
        "Batch E3 admits the local paper/UI semantics from `src/core/api/{paper,ui}.py` through injected `core.server` helper seams for offline/local verification only."
        in readme
    )
    assert (
        "Batch E3 admits the local paper/UI semantics from `src/core/api/{paper,ui}.py` through injected `core.server` helper seams for offline/local verification only."
        in scope_text
    )


def test_seed_contains_stateful_authority_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    champions_dir = repo_root / "config" / "strategy" / "champions"
    runtime_seed = json.loads(
        (repo_root / "config" / "runtime.seed.json").read_text(encoding="utf-8")
    )
    champion_1h = json.loads((champions_dir / "tBTCUSD_1h.json").read_text(encoding="utf-8"))
    champion_3h = json.loads((champions_dir / "tBTCUSD_3h.json").read_text(encoding="utf-8"))

    for relative_path in _STATEFUL_AUTHORITY_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")

    assert manifest["stateful_authority_verification"] == {
        "runtime_seed_baseline": {
            "runtime_test_file": "tests/runtime/test_stateful_authority_payloads.py",
            "tracked_file": "config/runtime.seed.json",
        },
        "verified_champion_subset": {
            "fallback_loader_file": "src/core/strategy/champion_loader.py",
            "runtime_test_file": "tests/runtime/test_stateful_authority_payloads.py",
            "tracked_files": [
                "config/strategy/champions/tBTCUSD_1h.json",
                "config/strategy/champions/tBTCUSD_3h.json",
            ],
        },
    }
    assert manifest["championless_fallback_contract"] == {
        "fallback_loader": "core.strategy.champion_loader.ChampionLoader",
        "phase_one_champion_policy": "admit_verified_runtime_champion_subset",
        "runtime_behavior": "fallback_to_runtime_seed_when_champion_missing_or_invalid",
        "runtime_fallback_source": "config/runtime.seed.json",
    }
    assert not (repo_root / "config" / "runtime.json").exists()
    assert {path.name for path in champions_dir.glob("*.json")} == {
        "tBTCUSD_1h.json",
        "tBTCUSD_3h.json",
    }
    assert not (champions_dir / "backup").exists()
    assert runtime_seed["cfg"]["strategy_family"] == "ri"
    assert (
        runtime_seed["cfg"]["multi_timeframe"]["regime_intelligence"]["authority_mode"]
        == "regime_module"
    )
    for payload in (champion_1h, champion_3h):
        assert payload["strategy_family"] == "ri"
        assert payload["merged_config"]["strategy_family"] == "ri"
        assert (
            payload["merged_config"]["multi_timeframe"]["regime_intelligence"]["authority_mode"]
            == "regime_module"
        )
    assert (
        "Batch F admits repo-tracked `config/runtime.seed.json` plus `config/strategy/champions/tBTCUSD_1h.json` and `config/strategy/champions/tBTCUSD_3h.json` while local `config/runtime.json`, candidate/test/backup champions, and `data/**` remain excluded."
        in readme
    )
    assert (
        "Batch F admits repo-tracked `config/runtime.seed.json` plus `config/strategy/champions/tBTCUSD_1h.json` and `config/strategy/champions/tBTCUSD_3h.json` while local `config/runtime.json`, candidate/test/backup champions, and `data/**` remain excluded."
        in scope_text
    )
    assert (
        "`ChampionLoader` falls back to the repo-tracked RI baseline in `config/runtime.seed.json` when a requested champion is missing or invalid."
        in readme
    )
    assert (
        "Genesis-Core-V2 runs `ri` as the only active strategy family on runtime authority and champion-default surfaces."
        in readme
    )


def test_seed_contains_transport_read_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_path in _TRANSPORT_READ_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")
    server_text = (repo_root / "src" / "core" / "server.py").read_text(encoding="utf-8")

    assert manifest["explicit_transport_admissions"] == [
        "src/core/io/__init__.py",
        "src/core/io/bitfinex/__init__.py",
        "src/core/io/bitfinex/exchange_client.py",
        "src/core/io/bitfinex/read_helpers.py",
        "src/core/io/bitfinex/rest_public.py",
        "src/core/io/bitfinex/rest_auth.py",
        "src/core/io/bitfinex/ws_public.py",
        "src/core/io/bitfinex/ws_auth.py",
        "src/core/io/bitfinex/ws_reconnect.py",
    ]
    assert manifest["transport_read_verification"] == {
        "bitfinex_rest_read_spine": {
            "module_files": [
                "src/core/io/bitfinex/exchange_client.py",
                "src/core/io/bitfinex/read_helpers.py",
            ],
            "runtime_test_file": "tests/runtime/test_transport_read_spine.py",
        }
    }
    assert manifest["transport_route_convergence"] == {
        "public_account_defaults": {
            "route_module_files": [
                "src/core/api/account.py",
                "src/core/api/public.py",
            ],
            "runtime_test_files": [
                "tests/runtime/test_account_endpoints.py",
                "tests/runtime/test_public_candles_endpoint.py",
            ],
            "server_file": "src/core/server.py",
        }
    }
    assert "_DeferredPublicExchangeClient" not in server_text
    assert "_DeferredAccountReadHelpers" not in server_text
    assert (
        "from core.io.bitfinex.exchange_client import aclose_http_client, get_exchange_client"
        in server_text
    )
    assert "from core.io.bitfinex import read_helpers as bfx_read" in server_text
    assert "rest_auth" not in server_text
    assert "ws_auth" not in server_text
    assert "ws_public" not in server_text
    assert "ws_reconnect" not in server_text
    assert (
        "Batch G2 binds generated public/account route defaults through `src/core/server.py` to the admitted Bitfinex REST read spine only; websocket, standalone auth, and paper-route transport widening remain deferred."
        in readme
    )
    assert (
        "Batch H2 widens transport family to include the remaining Bitfinex REST/WebSocket modules as dormant package surface only; this slice does not rebind server routes, startup wiring, or paper/live execution."
        in readme
    )
    assert (
        "Batch G2 binds generated public/account route defaults through `src/core/server.py` to the admitted Bitfinex REST read spine only; websocket, standalone auth, and paper-route transport widening remain deferred."
        in scope_text
    )
    assert (
        "Batch H2 widens transport family to include the remaining Bitfinex REST/WebSocket modules as dormant package surface only; this slice does not rebind server routes, startup wiring, or paper/live execution."
        in scope_text
    )


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
    assert (
        "Backtest comparison/diff semantics and associated tmp-path-isolated tests are admitted"
        in readme
    )
    assert (
        "Backtest comparison/diff semantics and associated tmp-path-isolated tests are admitted"
        in scope_text
    )


def test_seed_contains_optimizer_package_verification_manifest() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    diffing_init = repo_root / "src" / "core" / "utils" / "diffing" / "__init__.py"
    server_text = (repo_root / "src" / "core" / "server.py").read_text(encoding="utf-8")

    for relative_path in _OPTIMIZER_PACKAGE_VERIFICATION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    for relative_path in _OPTIMIZER_CONFIG_ADMISSION_FILES:
        assert (repo_root / relative_path).exists(), relative_path

    manifest = json.loads((repo_root / "seed_manifest.json").read_text(encoding="utf-8"))
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    scope_text = (repo_root / "docs" / "SKELETON_SCOPE.md").read_text(encoding="utf-8")
    pyproject_text = (repo_root / "pyproject.toml").read_text(encoding="utf-8")
    init_text = diffing_init.read_text(encoding="utf-8")

    assert manifest["optimizer_package_verification"] == {
        "audit_script_files": [
            "scripts/audit/audit_optuna_objective_parity.py",
        ],
        "dependency_contract": {
            "import_smoke_test_file": "tests/governance/test_import_smoke_backtest_optuna.py",
            "runtime_dependency": "optuna>=3.5,<5",
        },
        "dormant_package": {
            "module_files": [
                "src/core/optimizer/__init__.py",
                "src/core/optimizer/champion.py",
                "src/core/optimizer/constraints.py",
                "src/core/optimizer/param_transforms.py",
                "src/core/optimizer/runner.py",
                "src/core/optimizer/runner_config.py",
                "src/core/optimizer/runner_optuna_orchestration.py",
                "src/core/optimizer/runner_trial_backtest.py",
                "src/core/optimizer/runner_trial_results.py",
                "src/core/optimizer/runner_validation.py",
                "src/core/optimizer/scoring.py",
                "src/core/utils/optuna_helpers.py",
                "src/core/utils/diffing/config_equivalence.py",
                "src/core/utils/diffing/optuna_guard.py",
                "src/core/utils/diffing/trial_cache.py",
            ],
            "test_files": [
                "tests/governance/test_import_smoke_backtest_optuna.py",
                "tests/utils/diffing/test_config_equivalence.py",
                "tests/utils/diffing/test_optuna_diff.py",
                "tests/utils/test_optimizer_champion.py",
                "tests/utils/test_optimizer_direct_execution_canonical_guard.py",
                "tests/utils/test_optimizer_duplicate_fixes.py",
                "tests/utils/test_optimizer_json_cache_env_flag.py",
                "tests/utils/test_optimizer_param_transforms.py",
                "tests/utils/test_optimizer_param_transforms_dirichlet.py",
                "tests/utils/test_optimizer_performance.py",
                "tests/utils/test_optimizer_runner.py",
                "tests/utils/test_optuna_config_cache.py",
                "tests/utils/test_optuna_rdbstorage_engine_kwargs.py",
                "tests/utils/test_optuna_resume_signature.py",
                "tests/utils/test_set_global_seeds_parity.py",
            ],
        },
        "read_only_config_corpus": {
            "tracked_files": _OPTIMIZER_CONFIG_ADMISSION_FILES[1:],
        },
    }
    assert "optuna>=3.5,<5" in pyproject_text
    assert (
        "from .optuna_guard import TrialFingerprint, estimate_zero_trade, evaluate_trial_with_cache"
        in init_text
    )
    assert "from .trial_cache import TrialResultCache" in init_text
    assert "from .results_diff import (" in init_text
    assert "core.optimizer" not in server_text
    assert "scripts.run.run_backtest" not in server_text
    assert (
        "Batch I1 admits the dormant optimizer package and read-only `config/optimizer/**` research corpus for import/test completeness only."
        in readme
    )
    assert (
        "Batch I1 admits the dormant optimizer package and read-only `config/optimizer/**` research corpus for import/test completeness only."
        in scope_text
    )
    assert (
        "Generated dependency widening for the dormant optimizer slice is limited to `optuna>=3.5,<5`"
        in readme
    )


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
    assert (
        "Config runtime-authority semantics are admitted for source/verification purposes only"
        in readme
    )
    assert (
        "Config runtime-authority semantics are admitted for source/verification purposes only"
        in scope_text
    )


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
        candidate = repo_root / prefix
        if prefix == "data":
            if not candidate.exists():
                continue
            tracked = subprocess.run(
                ["git", "ls-files", "--", prefix],
                cwd=repo_root,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            assert not tracked, tracked
            continue
        assert not candidate.exists(), prefix

    server_text = (repo_root / "src" / "core" / "server.py").read_text(encoding="utf-8")
    assert "core.optimizer" not in server_text


def test_phase_one_seed_has_no_excluded_json_payloads() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    for relative_dir in _EXCLUDED_JSON_PAYLOAD_DIRS:
        candidate_dir = repo_root / relative_dir
        if not candidate_dir.exists():
            continue
        leaked = sorted(
            path.relative_to(repo_root).as_posix() for path in candidate_dir.rglob("*.json")
        )
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
