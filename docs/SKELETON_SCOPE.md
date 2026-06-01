# Genesis-Core-V2 Skeleton Scope

## Current target

`Genesis-Core-V2` is intentionally a thin, runnable shell:

- minimal repo structure
- runtime pipeline orchestration via `src/core/pipeline.py`
- local-only API
- Batch E1 public candles endpoint semantics with injected exchange-client verification
- Batch E2 read-only account endpoint semantics with injected read-helper verification
- Batch E3 local paper and UI semantics with injected helper verification
- Batch G1 Bitfinex REST read spine with direct runtime verification
- Batch G2 public/account route defaults bound through generated `src/core/server.py` to the admitted REST read spine only
- Batch H1 pure runtime decision/component/intelligence helpers plus repo-tracked composable strategy configs/tests
- Batch H2 dormant Bitfinex transport family admission without server/startup/paper-live rebinding
- Batch I1 dormant optimizer package/diffing utility admission plus repo-tracked `config/optimizer/**` research corpus without execution-root or runtime-authority widening
- Batch F repo-tracked runtime seed baseline plus the verified BTC champion subset
- local MCP stdio shell
- constrained remote MCP HTTP semantics without deployment helpers
- generated workflow guidance for agent-driven work
- fixture-backed smoke tests
- dormant admission of the remaining Bitfinex transport family only; no server rebinding or live-ready/private runtime edges

`Genesis-Core` remains the source of truth until each slice is proven.

## Track A — skeleton completeness

Included in the current priority lane:

- README and local workflow docs
- `AGENTS.md`, `.github/copilot-instructions.md`, and `.pre-commit-config.yaml`
- `.vscode/mcp.json`, `.vscode/tasks.json`, `.vscode/launch.json`, `.vscode/settings.json`, and `.vscode/extensions.json` for local editor workflow
- tracked local env bootstrap template (`.env.example`) plus ignored local placeholder `.env`
- narrow local pytest/ruff/black defaults in `pyproject.toml`
- repo-local MCP launcher (`scripts/mcp/mcp_stdio.py`) for non-installed stdio startup
- repo-local API launcher (`scripts/api/api_shell.py`) for non-installed startup
- repo-local pytest launcher (`scripts/validate/pytest_suite.py`) for non-installed test execution
- repo-local Bitfinex candle fetch script (`scripts/data/fetch_historical.py`) for local raw JSON + raw-frozen parquet refreshes under excluded `data/**`
- repo-local smoke scripts (`scripts/smoke/*.py`) for non-installed execution
- `config/mcp_settings.json` and `mcp_server/**` for local MCP use
- local-only API shell (`account`, `config`, `info`, `status`, `models`, `paper`, `public`, `strategy`, `ui`)
- admitted strategy authority helpers (`src/core/config/authority_mode_resolver.py`, `src/core/strategy/{family_registry,family_admission,run_intent}.py`)
- admitted config/runtime authority semantics (`src/core/config/{authority,authority_mode_resolver,schema}.py`, `src/core/api/config.py`) with repo-tracked `config/runtime.seed.json` while local runtime override remains excluded
- admitted verified champion subset (`config/strategy/champions/tBTCUSD_1h.json`, `config/strategy/champions/tBTCUSD_3h.json`) while candidate/test/backup champion payloads remain excluded
- admitted backtest comparison/diff semantics (`src/core/utils/diffing/results_diff.py`, `tools/compare_backtest_results.py`) while execution roots and corpora remain excluded
- admitted constrained remote MCP semantics (`mcp_server/remote_server.py`, `config/mcp_settings.remote_{safe,git}.json`) while launchers and deployment guidance remain excluded
- Batch G1 direct Bitfinex REST read-spine verification (`src/core/io/bitfinex/{exchange_client,read_helpers}.py`, `tests/runtime/test_transport_read_spine.py`)
- Batch G2 binds generated public/account route defaults through `src/core/server.py` to the admitted Bitfinex REST read spine only; websocket, standalone auth, and paper-route transport widening remain deferred.
- Batch H1 admits pure runtime decision logic, composable strategy components, intelligence helper packages, and repo-tracked composable strategy configs/tests without widening transport, optimizer, or runtime-authority surfaces.
- Batch H2 widens transport family to include the remaining Bitfinex REST/WebSocket modules as dormant package surface only; this slice does not rebind server routes, startup wiring, or paper/live execution.
- Batch I1 admits the dormant optimizer package (`src/core/optimizer/**`), supporting diffing/Optuna helpers, and repo-tracked `config/optimizer/**` research corpus for import/test completeness only; optimizer execution roots, runtime-authority payloads, and server/startup bindings remain deferred.
- `src/core/pipeline.py` plus narrow deterministic seeding helper `src/core/utils/random_seeds.py`
- runtime determinism guardrails for pipeline fast-hash policy and feature-cache hash stability
- fixture-backed smoke tests and console scripts
- explicitly admitted non-sensitive config/model artifacts already carried into the seed

Config runtime-authority semantics are admitted for source/verification purposes only, including the
authority/schema/API surfaces already present in the V2 source closure. Repo-tracked
`config/runtime.seed.json` is carried as the baseline authority fallback while local
`config/runtime.json`, non-authoritative champion artifacts, and live-adjacent/promotion surfaces
remain deferred and excluded from the seed.
Backtest comparison/diff semantics and associated tmp-path-isolated tests are admitted. Backtest
execution roots, results corpora, non-authoritative champion payloads, local runtime override
payloads, `scripts/run/run_backtest.py`, and remote/live edges remain deferred or excluded.
Batch I1 admits the dormant optimizer package and read-only `config/optimizer/**` research corpus
for import/test completeness only. Optimizer execution roots (`scripts/run/run_backtest.py`,
`scripts/optimize/**`, preflight/validation CLIs), runtime-authority payload widening, and any
server/startup activation remain deferred and excluded from this seed.
Genesis-Core-V2 admits constrained remote MCP semantics limited to authorization, safe-mode,
confirm-token, and transport-alias behavior already present in source. Operational launch scripts,
deployment/tunnel/proxy guidance, and other live-adjacent surfaces remain deferred and are not
included in this slice.
Batch E1 admits the public candles endpoint semantics from `src/core/api/public.py` through an injected `core.server.get_exchange_client` seam for offline verification while broader transport remains deferred.
Batch E2 admits only the read-only account endpoint semantics from `src/core/api/account.py` through an injected `core.server.bfx_read` seam for offline verification.
Batch E3 admits the local paper/UI semantics from `src/core/api/{paper,ui}.py` through injected `core.server` helper seams for offline/local verification only.
Batch G1 admits the Bitfinex REST read spine (`src/core/io/bitfinex/{exchange_client,read_helpers}.py`) for direct runtime verification.
Batch G2 binds generated public/account route defaults through `src/core/server.py` to the admitted Bitfinex REST read spine only; websocket, standalone auth, and paper-route transport widening remain deferred.
Batch F admits repo-tracked `config/runtime.seed.json` plus `config/strategy/champions/tBTCUSD_1h.json` and `config/strategy/champions/tBTCUSD_3h.json` while local `config/runtime.json`, candidate/test/backup champions, and `data/**` remain excluded.
Batch I1 admits the dormant optimizer package and read-only `config/optimizer/**` research corpus for import/test completeness only. It does not admit optimizer execution roots, startup/server bindings, or runtime-authority payloads.
`ChampionLoader` still falls back to `config/timeframe_configs.py` when a requested champion is missing or invalid.

## Track B — authority migration

Deferred to separate verified slices:

- remote MCP operational launchers and deployment/tunnel/proxy guidance remain deferred
- activation/rebinding of the dormant Bitfinex transport family and other live-adjacent/private execution edges
- freeze-sensitive surfaces

## Verification loop

- In `Genesis-Core`: `python -m pytest tests/utils/test_open_v2_runtime_seed.py -q`
- Regenerate the seed: `python scripts/extract/open_v2_runtime_seed.py --clean`
- In `Genesis-Core-V2`: `python -m pytest -q`
- Local task loop: `genesis-v2: api shell`, `genesis-v2: mcp stdio`, `genesis-v2: smoke suite`, `genesis-v2: pytest`
- Local debug loop: `genesis-v2: api shell`, `genesis-v2: mcp stdio`, `genesis-v2: smoke suite`, `genesis-v2: pytest`
- Local editor settings: `python.analysis.extraPaths`, `python.testing.*`, `python.envFile`
- Local editor recommendations: `ms-python.python`, `ms-python.vscode-pylance`, `charliermarsh.ruff`
- Local pre-commit workflow: `pre-commit install`, then `pre-commit run --all-files`
- Local QA defaults: `pytest` recursion guards plus narrow `ruff`/`black` excludes in `pyproject.toml`
- Non-installed local MCP launcher: `python scripts/mcp/mcp_stdio.py`, optional config probe via `python scripts/mcp/mcp_stdio.py --print-config`
- Non-installed local API launcher: `python scripts/api/api_shell.py`, optional reload via `python scripts/api/api_shell.py --reload`
- Non-installed local pytest launcher: `python scripts/validate/pytest_suite.py`, optional focused run via `python scripts/validate/pytest_suite.py tests/runtime/test_local_api_shell_script.py -q`
- Non-installed local Bitfinex candle fetch script: `python scripts/data/fetch_historical.py --symbol tBTCUSD --timeframes 1m 5m 15m 30m 1h 3h 6h 12h 1D 7D 14D`, optional raw-json conversion via `python scripts/data/fetch_historical.py --from-raw-json --symbol tBTCUSD --timeframes 1h 1D`
- Non-installed local smoke scripts: `python scripts/smoke/fixture_smoke.py`, `python scripts/smoke/backtest_smoke.py`, `python scripts/smoke/champion_smoke.py`, `python scripts/smoke/evaluate_champion_smoke.py`, `python scripts/smoke/model_smoke.py`, `python scripts/smoke/smoke_suite.py`
- Installable local console scripts: `genesis-v2-api-shell`, `genesis-v2-mcp-stdio`, `genesis-v2-pytest`, `genesis-v2-champion-smoke`, `genesis-v2-evaluate-champion-smoke`, `genesis-v2-fixture-smoke`, `genesis-v2-backtest-smoke`, `genesis-v2-model-smoke`, `genesis-v2-smoke-suite`
- Installable console-script verification: `python -m pip install -e ".[dev,mcp]"`, then `pytest tests/runtime/test_installed_console_scripts.py -q`
- Editable-install module loop: `python -m uvicorn core.server:app --app-dir src --reload`, `python -m mcp_server.server`, `python -m pytest -q`
- Editable-install smoke module loop: `python -m core.bootstrap.model_smoke`, `python -m core.bootstrap.champion_smoke`, `python -m core.bootstrap.evaluate_champion_smoke`, `python -m core.bootstrap.fixture_smoke`, `python -m core.bootstrap.backtest_smoke`, `python -m core.bootstrap.smoke_suite`
- Optional local MCP install: `python -m pip install -e ".[mcp]"`
