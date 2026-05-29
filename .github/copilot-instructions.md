# Copilot Instructions — Genesis-Core-V2

This repository is a skeleton-first, local-only V2 seed.
Read `AGENTS.md` and `docs/SKELETON_SCOPE.md` before widening scope.

## Default behavior

- Prefer the smallest admissible slice.
- Prioritize V2 skeleton completeness before content migration.
- Keep `Genesis-Core` as the source of truth for authority-bearing behavior until a slice is admitted.
- Prefer generator-driven changes in `Genesis-Core` over manual drift in this repo.
- Keep the local-only API shell runnable and tested.
- Keep the local MCP stdio shell local-first and safe by default.
- Keep the admitted strategy authority helpers (`core.config.authority_mode_resolver`, `core.strategy.family_registry`, `core.strategy.family_admission`, `core.strategy.run_intent`) runnable and tested.
- Keep the admitted config/runtime authority semantics (`core.config.authority`, `core.config.schema`, `core.api.config`) verification-only and isolated from repo-root runtime payload writes.
- Keep the admitted backtest comparison/diff semantics (`core.utils.diffing.results_diff`, `tools.compare_backtest_results`) tmp-path-isolated and out of execution-root expansion.
- Keep the admitted remote MCP semantics (`mcp_server.remote_server`, `config/mcp_settings.remote_{safe,git}.json`) limited to authorization, safe-mode, confirm-token, and transport-alias behavior already present in source.
- Prefer generated local `scripts/mcp/mcp_stdio.py` or `.vscode/mcp.json` for non-installed MCP startup.
- Prefer generated local `scripts/api/api_shell.py` or editor task/debug profiles for non-installed API startup.
- Prefer generated local `scripts/validate/pytest_suite.py` or editor task/debug profiles for non-installed pytest loops.
- Prefer generated local `scripts/smoke/*.py` wrappers or `python -m core.bootstrap...` commands for non-installed smoke loops.
- Prefer the generated local VS Code tasks, debug profiles, settings, and extension recommendations for repeatable API/smoke/test loops when working interactively.
- Prefer fixture-backed smoke tests before moving wider runtime content.

## Out of scope by default

- exchange, paper, UI, and private runtime edges
- remote MCP operational launchers, deployment/tunnel/proxy guidance, and other live-adjacent surfaces
- runtime state and champion authority payloads
- backtest execution roots, results corpora, promotion surfaces, and freeze-sensitive surfaces
- unverified content migration for its own sake
