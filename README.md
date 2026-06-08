# Genesis-Core-V2

Runtime-first seed with admitted local-only API shell and constrained remote MCP semantics
generated from the current `Genesis-Core` repository.

Source Genesis-Core HEAD: `6025ad87`

## What is included

- runtime kernel roots (`backtest`, `strategy`, `regime`)
- runtime pipeline orchestration (`src/core/pipeline.py`)
- local dependency closure required by those roots
- admitted local-only API shell (`src/core/server.py`,
  `src/core/api/{account,config,info,models,paper,public,status,strategy,ui}.py`)
- source-backed config validation seam (`src/core/config/validator.py`,
  `src/core/config/legacy_schema_v1.json`)
- source-backed config endpoint integration smoke (`tests/integration/test_config_endpoints.py`)
- narrow config bootstrap (`config/__init__.py`, `config/timeframe_configs.py`,
  `config/backtest_defaults.yaml`)
- local MCP stdio shell (`mcp_server/*.py`, `.vscode/mcp.json`, `config/mcp_settings.json`)
- local VS Code task/debug loop (`.vscode/tasks.json`, `.vscode/launch.json`)
- local VS Code Python analysis/test settings (`.vscode/settings.json`)
- local VS Code extension recommendations (`.vscode/extensions.json`)
- tracked env bootstrap template (`.env.example`)
- local pre-commit hook config (`.pre-commit-config.yaml`)
- narrow local QA defaults in `pyproject.toml`
- repo-local MCP launcher (`scripts/mcp/mcp_stdio.py`)
- repo-local API launcher (`scripts/api/api_shell.py`)
- repo-local pytest launcher (`scripts/validate/pytest_suite.py`)
- repo-local Bitfinex candle fetch script (`scripts/data/fetch_historical.py`) for local raw JSON + raw-frozen parquet refreshes under excluded `data/**`
- repo-local smoke scripts (`scripts/smoke/{backtest_smoke,champion_smoke,evaluate_champion_smoke,fixture_smoke,model_smoke,smoke_suite}.py`)
- admitted strategy authority helpers (`src/core/config/authority_mode_resolver.py`,
  `src/core/strategy/{family_registry,family_admission,run_intent}.py`)
- admitted config/runtime authority semantics (`src/core/config/{authority,authority_mode_resolver,schema}.py`,
  `src/core/api/config.py`) with repo-tracked `config/runtime.seed.json` while local runtime override remains excluded
- verified champion subset (`config/strategy/champions/tBTCUSD_1h.json`,
  `config/strategy/champions/tBTCUSD_3h.json`) while candidate/test/backup champion payloads stay excluded
- admitted backtest comparison/diff semantics (`src/core/utils/diffing/results_diff.py`,
  `tools/compare_backtest_results.py`) without carrying execution roots or results corpora
- admitted constrained remote MCP semantics (`mcp_server/remote_server.py`,
  `config/mcp_settings.remote_{safe,git}.json`) without operational launchers or deployment guidance
- Batch E1 public candles endpoint semantics (`src/core/api/public.py`) through the injected `core.server.get_exchange_client` verification seam while broader transport stays deferred
- Batch E2 read-only account endpoint semantics (`src/core/api/account.py`) through the injected `core.server.bfx_read` verification seam while broader transport stays deferred
- Batch E3 local paper/UI semantics (`src/core/api/{paper,ui}.py`) through injected `core.server` helper seams while broader transport, deployment guidance, and live-ready transport authority stay deferred
- Batch G1 Bitfinex REST read spine (`src/core/io/bitfinex/{exchange_client,read_helpers}.py`) with direct verification in `tests/runtime/test_transport_read_spine.py`
- Batch G2 binds generated public/account route defaults through `src/core/server.py` to the admitted Bitfinex REST read spine only; websocket, standalone auth, and paper-route transport widening remain deferred.
- Batch H1 admits pure runtime decision logic, composable strategy components, intelligence helper packages, and repo-tracked composable strategy configs/tests without widening transport, optimizer, or runtime-authority surfaces.
- Batch H2 widens transport family to include the remaining Bitfinex REST/WebSocket modules as dormant package surface only; this slice does not rebind server routes, startup wiring, or paper/live execution.
- Batch I1 admits the dormant optimizer package (`src/core/optimizer/**`), supporting diffing/Optuna helpers, and repo-tracked `config/optimizer/**` research corpus for import/test completeness only.
- runtime-only governance guardrails
- runtime determinism guardrails for pipeline fast-hash policy and feature-cache hash stability
- subsystem-local `index.md` guidance in major folders plus deterministic premortem reflection convention
- admitted source model payloads under `config/models/**`
- deterministic fixture model-registry/prob-model smoke
  (`registry/fixtures/model_registry/config/models/{registry.json,tBTCUSD_1h.json}`,
  `core.bootstrap.model_smoke`)
- local champion fixture/bootstrap smoke (`registry/fixtures/champions/tBTCUSD_1h.json`,
  `core.bootstrap.champion_smoke`)
- live evaluate smoke backed by the local champion fixture (`core.bootstrap.evaluate_champion_smoke`)
- fixture-driven bootstrap smoke (`registry/fixtures/runtime_fixture_smoke_minimal.json`,
  `core.bootstrap.fixture_smoke`)
- fixture-driven backtest bootstrap smoke (`core.bootstrap.backtest_smoke`)
- combined runtime smoke suite (`core.bootstrap.smoke_suite`)
- fixture-driven backtest engine smoke (`tests/runtime/test_backtest_engine_fixture_smoke.py`)
- installable console scripts for local API/MCP/pytest and smoke entrypoints

## What is intentionally excluded

- broader future `src/core/io/**` beyond the admitted `src/core/io/bitfinex/**` family
- `src/core/strategy/features.py`
- `scripts/run/run_backtest.py`
- `scripts/optimize/**`
- `scripts/preflight/preflight_optuna_check.py`
- `scripts/validate/validate_optimizer_config.py`
- `scripts/mcp/start_mcp_remote.ps1`
- `scripts/mcp_session_preflight.py`
- `config/runtime.json`
- `config/strategy/champions/backup/**`
- `config/strategy/champions/*candidate*.json`
- `config/strategy/champions/tTEST_1h.json`
- `config/strategy/candidates/**`
- `docs/mcp/**`
- `data/**`
- branch-local research corpora and historical explanation surfaces

## Notes

This seed is intentionally narrower than the source repository.
It is a local starting point, not a claim that all later bootstrap, model, champion,
or wider state-authority decisions are already resolved.
Source `config/models/**` payloads are copied into the seed, while deterministic smoke
paths use fixture-backed model registry payloads under `registry/fixtures/model_registry/**`.
Repo-tracked `config/runtime.seed.json` is copied into the seed as the baseline authority fallback.
Genesis-Core-V2 runs `ri` as the only active strategy family on runtime authority and champion-default surfaces. Any retained legacy material outside those active paths is archival/reference only and is not selected by default, fallback, or incumbent-comparison logic in V2.
Generated V2 still excludes local `config/runtime.json`; if a local runtime override is later created,
`ConfigAuthority` preserves runtime.json-over-seed precedence.
A verified champion subset is admitted: `config/strategy/champions/tBTCUSD_1h.json` and
`config/strategy/champions/tBTCUSD_3h.json`.
`ChampionLoader` falls back to the repo-tracked RI baseline in `config/runtime.seed.json` when a requested champion is missing or invalid.
The admitted API shell is local-only (`account/config/info/status/models/paper/public/strategy/ui`).
Generated `.env` contains local-shell and Bitfinex REST credential placeholders only.
Tracked `.env.example` mirrors the same narrow values for copy-forward bootstrap.
Config runtime-authority semantics are admitted for source/verification purposes only, including the
authority/schema/API surfaces already present in the V2 source closure. Runtime state payloads
(`config/runtime.json`), candidate/test/backup champion artifacts, remote MCP surfaces, and
live-adjacent/promotion surfaces remain deferred and excluded from the seed.
Backtest comparison/diff semantics and associated tmp-path-isolated tests are admitted. Backtest
execution roots, results corpora, non-authoritative champion payloads, local runtime override
payloads, `scripts/run/run_backtest.py`, and remote/live edges remain deferred or excluded.
Genesis-Core-V2 admits constrained remote MCP semantics limited to authorization, safe-mode,
confirm-token, and transport-alias behavior already present in source. Operational launch scripts,
deployment/tunnel/proxy guidance, and other live-adjacent surfaces remain deferred and are not
included in this slice.
Batch E1 admits the public candles endpoint semantics from `src/core/api/public.py` through an injected `core.server.get_exchange_client` seam for offline verification while broader transport remains deferred.
Batch E2 admits only the read-only account endpoint semantics from `src/core/api/account.py` through an injected `core.server.bfx_read` seam for offline verification.
Batch E3 admits the local paper/UI semantics from `src/core/api/{paper,ui}.py` through injected `core.server` helper seams for offline/local verification only.
Batch G1 admits the Bitfinex REST read spine (`src/core/io/bitfinex/{exchange_client,read_helpers}.py`) for direct runtime verification.
Batch G2 binds generated public/account route defaults through `src/core/server.py` to the admitted Bitfinex REST read spine only; websocket, standalone auth, and paper-route transport widening remain deferred.
Batch H1 admits pure runtime decision logic, composable strategy components, intelligence helper packages, and repo-tracked composable strategy configs/tests without widening transport, optimizer, or runtime-authority surfaces.
Batch H2 widens transport family to include the remaining Bitfinex REST/WebSocket modules as dormant package surface only; this slice does not rebind server routes, startup wiring, or paper/live execution.
Batch I1 admits the dormant optimizer package and read-only `config/optimizer/**` research corpus for import/test completeness only. It does not admit optimizer execution roots, startup/server bindings, or runtime-authority payloads.
Batch F admits repo-tracked `config/runtime.seed.json` plus `config/strategy/champions/tBTCUSD_1h.json` and `config/strategy/champions/tBTCUSD_3h.json` while local `config/runtime.json`, candidate/test/backup champions, and `data/**` remain excluded.
Admitted strategy authority helpers keep family classification, run-intent admission, and authority-mode
precedence observable in the seed without admitting runtime/config state authority or promotion surfaces.
Runtime pipeline orchestration is admitted through `src/core/pipeline.py`, while the narrower
`src/core/utils/random_seeds.py` helper preserves deterministic seeding while the dormant optimizer
package reuses the admitted `src/core/utils/optuna_helpers.py` parity surface.
Generated dependency widening for the dormant optimizer slice is limited to `optuna>=3.5,<5` so the
admitted `core.optimizer` and `core.utils.optuna_helpers` imports remain import-safe without opening
execution roots or broader tooling surfaces.
Generated `src/core/utils/diffing/__init__.py` is widened only to the admitted `results_diff`,
`optuna_guard`, and `trial_cache` exports required by the dormant optimizer package.
Local MCP support is admitted for stdio-first workspace usage, while the remote HTTP entrypoint and
remote allowlist variants are admitted only for semantics-level verification.
Repo-local MCP launcher is generated so the local stdio shell can start without depending on
editor-specific config wiring first.
Repo-local API launcher is generated so the local API shell can start without depending on
editor-specific tasks or an editable install first.
Repo-local pytest launcher is generated so the seed can run its test loop without depending on
editor-specific tasks or an editable install first.
Repo-local smoke scripts are generated so the seed can run its core smoke loops without relying on
editor-specific tasks or an editable install first.
Major subsystem folders may include a local `index.md` that explains purpose, boundaries,
invariants, related tests, and lifecycle role. These files are local navigation aids for humans and
agents; they do not override the repository's governance or authority contracts.
Premortem reflection in V2 is deterministic, evidence-based, and fail-closed. If a premortem claim
cannot be tied to a metric, run-intent, threshold, signoff, or another deterministic evidence
surface, it does not belong in V2 premortem.

## Skeleton workflow

- `AGENTS.md` defines the skeleton-first repo contract.
- `.github/copilot-instructions.md` keeps local agent work aligned with the V2 operating model and validated slices.
- `docs/SKELETON_SCOPE.md` records Track A vs Track B and the verification loop.
- `.vscode/mcp.json` wires VS Code to the local `scripts/mcp/mcp_stdio.py` wrapper using `config/mcp_settings.json`.
- `.vscode/tasks.json` and `.vscode/launch.json` route local API/MCP/smoke/test loops through the repo-local wrappers while keeping `PYTHONPATH=${workspaceFolder}/src` available.
- `.vscode/settings.json` aligns Python analysis/test discovery with the `src/` layout and local `.env` placeholder.
- `.vscode/extensions.json` recommends the Python/Pylance/Ruff stack for local skeleton work.
- `.github/ISSUE_TEMPLATE/*.yml` keeps bug/feature intake aligned with the repo's bounded governance workflow.
- `.env.example` keeps the narrow local placeholder values tracked even though `.env` stays ignored.
- `.pre-commit-config.yaml` keeps a narrow local formatting/lint/sanity/secret-scan hook loop tracked in the seed.
- `docs/adr/0000-template.md` provides the repo-local ADR starter for architecture and workflow decisions.
- `pyproject.toml` carries narrow local pytest/ruff/black defaults plus tracked dev-tooling dependencies for the generated V2 workspace.
- `scripts/mcp/mcp_stdio.py` wraps the local MCP stdio shell with repo-root bootstrap and the generated config path.
- `scripts/api/api_shell.py` wraps the local API shell with `src/` bootstrapping for non-installed startup.
- `scripts/validate/pytest_suite.py` wraps `pytest` with local `src/` bootstrapping for non-installed test execution.
- `scripts/audit/pip_audit.py` wraps `pip-audit` with the current repo-local baseline ignore policy for repeatable dependency scans.
- `scripts/data/fetch_historical.py` wraps the admitted Bitfinex REST read spine for local raw JSON + raw-frozen parquet refreshes under excluded `data/**`.
- `scripts/smoke/*.py` wraps the admitted core smoke modules with local `src/` bootstrapping so the seed is runnable before install.

After `uv sync --extra dev --extra mcp`, local module commands:

Local API shell: `python -m uvicorn core.server:app --app-dir src --reload`
Local MCP stdio shell: `python -m mcp_server.server`
Local pytest suite: `python -m pytest -q`

Local model smoke: `python -m core.bootstrap.model_smoke`
Local champion smoke: `python -m core.bootstrap.champion_smoke`
Local champion-backed evaluate smoke: `python -m core.bootstrap.evaluate_champion_smoke`
Local bootstrap smoke: `python -m core.bootstrap.fixture_smoke`
Local backtest bootstrap smoke: `python -m core.bootstrap.backtest_smoke`
Local runtime smoke suite: `python -m core.bootstrap.smoke_suite`

Non-installed local MCP launcher:
`python scripts/mcp/mcp_stdio.py`
`python scripts/mcp/mcp_stdio.py --print-config`

Non-installed local API launcher:
`python scripts/api/api_shell.py`
`python scripts/api/api_shell.py --reload`

Non-installed local pytest launcher:
`python scripts/validate/pytest_suite.py`
`python scripts/validate/pytest_suite.py tests/runtime/test_local_api_shell_script.py -q`

Non-installed local Bitfinex candle fetch script:
`python scripts/data/fetch_historical.py --symbol tBTCUSD --timeframes 1m 5m 15m 30m 1h 3h 6h 12h 1D 7D 14D`
`python scripts/data/fetch_historical.py --from-raw-json --symbol tBTCUSD --timeframes 1h 1D`
`python scripts/data/fetch_historical.py --duckdb-summary --symbol tBTCUSD --timeframes 1h 1D`
`python scripts/data/fetch_historical.py --print-config --symbol tBTCUSD --timeframes 1h 1D`

Non-installed local smoke scripts:
`python scripts/smoke/fixture_smoke.py`
`python scripts/smoke/backtest_smoke.py`
`python scripts/smoke/champion_smoke.py`
`python scripts/smoke/evaluate_champion_smoke.py`
`python scripts/smoke/model_smoke.py`
`python scripts/smoke/smoke_suite.py`

Local VS Code tasks:
`genesis-v2: api shell`, `genesis-v2: mcp stdio`, `genesis-v2: smoke suite`, `genesis-v2: pytest`

Local VS Code debug profiles:
`genesis-v2: api shell`, `genesis-v2: mcp stdio`, `genesis-v2: smoke suite`, `genesis-v2: pytest`

Suggested VS Code extensions:
`ms-python.python`, `ms-python.vscode-pylance`, `charliermarsh.ruff`

Python analysis/test settings:
`.vscode/settings.json`

Console scripts after editable install:
`genesis-v2-api-shell`, `genesis-v2-mcp-stdio`, `genesis-v2-pytest`
`genesis-v2-champion-smoke`, `genesis-v2-evaluate-champion-smoke`
`genesis-v2-fixture-smoke`, `genesis-v2-backtest-smoke`, `genesis-v2-smoke-suite`
`genesis-v2-model-smoke`

Suggested install verification:
`uv sync --extra dev --extra mcp`
then run `uv run pytest tests/runtime/test_installed_console_scripts.py -q`

Optional regression-test loop:
`uv run pytest tests/backtest/test_compare_backtest_results.py -q`

Local pre-commit workflow:
`uv run pre-commit install`
then run `uv run pre-commit run --all-files`

Local dependency audit:
`uv run python scripts/audit/pip_audit.py`

Strict dependency audit (no baseline ignores):
`uv run python scripts/audit/pip_audit.py --strict`

Optional local MCP install:
`uv sync --extra mcp`
then connect the `genesis-core-v2` server from `.vscode/mcp.json`
