# Copilot Instructions — Genesis-Core-V2

This repository is a skeleton-first, local-only V2 seed.
Read `AGENTS.md` and `docs/SKELETON_SCOPE.md` before widening scope.

## Default behavior

- Prefer the smallest admissible slice.
- Prioritize V2 skeleton completeness before content migration.
- Keep `Genesis-Core` as the source of truth for authority-bearing behavior until a slice is admitted.
- Prefer generator-driven changes in `Genesis-Core` over manual drift in this repo.
- Keep the local-only API shell runnable and tested.
- Keep the Batch E1 public candles endpoint semantics (`core.api.public`) bound only through the generated `core.server.get_exchange_client` surface.
- Keep the Batch E2 read-only account semantics (`core.api.account`) bound only through the generated `core.server.bfx_read` surface.
- Keep the Batch E3 local paper semantics (`core.api.paper`) limited to offline/local verification through generated `core.server` helper seams; do not treat it as live-ready transport admission.
- Keep the admitted Bitfinex transport family (`core.io.bitfinex.*`) dormant as package surface only; do not rebind it into server routes, startup wiring, or paper/live execution.
- Keep Batch G2 generated public/account route defaults bound only through `core.server.get_exchange_client` and `core.server.bfx_read` to that admitted REST read spine.
- Keep Batch H1 pure runtime decision/component/intelligence helper and composable-config admissions isolated from transport, optimizer, and runtime-authority widening.
- Keep Batch I1 dormant optimizer/package admissions (`core.optimizer.*`, `core.utils.optuna_helpers`, `core.utils.diffing.{config_equivalence,optuna_guard,trial_cache}`, `config/optimizer/**`) limited to import/test completeness only; do not admit execution roots, startup/server bindings, or runtime-authority payloads.
- Keep the admitted local UI shell (`core.api.ui`) aligned with admitted local endpoints only; do not expand it into deployment or live-ops claims.
- Keep the local MCP stdio shell local-first and safe by default.
- Keep the admitted strategy authority helpers (`core.config.authority_mode_resolver`, `core.strategy.family_registry`, `core.strategy.family_admission`, `core.strategy.run_intent`) runnable and tested.
- Keep the admitted config/runtime authority semantics (`core.config.authority`, `core.config.schema`, `core.api.config`) verification-only, with repo-tracked `config/runtime.seed.json` preserved read-only and local `config/runtime.json` still excluded from the seed.
- Keep the admitted Batch F verified champion subset (`config/strategy/champions/tBTCUSD_1h.json`, `config/strategy/champions/tBTCUSD_3h.json`) read-only; candidate/test/backup champion payloads remain deferred.
- Keep the admitted backtest comparison/diff semantics (`core.utils.diffing.results_diff`, `tools.compare_backtest_results`) tmp-path-isolated and out of execution-root expansion.
- Keep the admitted remote MCP semantics (`mcp_server.remote_server`, `config/mcp_settings.remote_{safe,git}.json`) limited to authorization, safe-mode, confirm-token, and transport-alias behavior already present in source.
- Prefer generated local `scripts/mcp/mcp_stdio.py` or `.vscode/mcp.json` for non-installed MCP startup.
- Prefer generated local `scripts/api/api_shell.py` or editor task/debug profiles for non-installed API startup.
- Prefer generated local `scripts/validate/pytest_suite.py` or editor task/debug profiles for non-installed pytest loops.
- Prefer generated local `scripts/smoke/*.py` wrappers or `python -m core.bootstrap...` commands for non-installed smoke loops.
- Prefer the generated local VS Code tasks, debug profiles, settings, and extension recommendations for repeatable API/smoke/test loops when working interactively.
- Prefer fixture-backed smoke tests before moving wider runtime content.

## Out of scope by default

- activation of the dormant Bitfinex transport family into server/startup/paper/live runtime paths
- remote MCP operational launchers, deployment/tunnel/proxy guidance, and other live-adjacent surfaces
- local runtime override payloads and non-authoritative champion payloads
- backtest execution roots, results corpora, promotion surfaces, and freeze-sensitive surfaces
- optimizer execution roots (`scripts/run/run_backtest.py`, `scripts/optimize/**`, preflight/validation CLIs), runtime-authority payload widening, and server/startup activation of the dormant optimizer package
- unverified content migration for its own sake
