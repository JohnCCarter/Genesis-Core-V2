# Genesis-Core-V2 Scope and Operating Boundaries

This document complements `.github/copilot-instructions.md`.

Use it to answer four questions quickly:

1. What is `Genesis-Core-V2` for?
2. Which surfaces are active authority?
3. Which surfaces are admitted but constrained?
4. Which surfaces are still deferred?

When a more specific contract, test, instruction, or boundary document exists, that more specific surface wins.

## Purpose

`Genesis-Core-V2` is a thin, runnable, RI-first repository optimized for faster research, stronger validation, and safer promotion.

Lifecycle order in this repository is:

Research -> Validate -> Promote

It is intentionally narrower than `Genesis-Core`.

`Genesis-Core` may still be used as:

- historical reference
- migration reference
- audit reference
- seed/regeneration source when a slice explicitly requires it

It does **not** override admitted V2 authority surfaces without an explicit validated slice.

## Current repository shape

Genesis-Core-V2 currently aims to remain:

- minimal in structure
- runnable in local workflows
- evidence-first in how changes are justified
- RI-first on active strategy authority surfaces
- conservative about widening transport, optimizer, and promotion paths

The current shape includes:

- runtime pipeline orchestration via `src/core/pipeline.py`
- local-first API/UI semantics
- local MCP stdio shell
- fixture-backed smoke tests
- repo-tracked runtime seed baseline
- verified BTC champion subset
- admitted but constrained REST read-spine, optimizer package, and remote MCP semantics
- constrained remote MCP HTTP semantics without deployment helpers

## Active authority surfaces

The following are active authority-bearing surfaces in V2:

- `ri` is the sole active strategy family on runtime, config-authority, champion-default, and promotion-facing surfaces
- `config/runtime.seed.json` is the repo-tracked baseline authority fallback
- local `config/runtime.json` remains excluded and non-authoritative
- the verified champion subset is limited to:
  - `config/strategy/champions/tBTCUSD_1h.json`
  - `config/strategy/champions/tBTCUSD_3h.json`
- champion miss-path fallback resolves to `config/runtime.seed.json`

Batch F admits repo-tracked `config/runtime.seed.json` plus `config/strategy/champions/tBTCUSD_1h.json` and `config/strategy/champions/tBTCUSD_3h.json` while local `config/runtime.json`, candidate/test/backup champions, and `data/**` remain excluded.

Legacy may remain in the repository for:

- historical comparison
- replay comparison
- audit purposes
- migration reference

Legacy must not function as:

- runtime authority
- promotion authority
- default admission target
- architectural authority

## Track A — skeleton completeness

The current priority lane remains Track A — skeleton completeness.

In lifecycle terms, Track A is where Research and Validate are primarily executed for admitted V2 surfaces.

## Admitted and constrained scope

### Local workflow and repo hygiene

The following are admitted as part of the normal V2 local workflow surface:

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `.pre-commit-config.yaml`
- tracked `.env.example` plus ignored local `.env`
- `.vscode/mcp.json`
- `.vscode/tasks.json`
- `.vscode/launch.json`
- `.vscode/settings.json`
- `.vscode/extensions.json`
- `pyproject.toml`
- local launchers under:
  - `scripts/api/api_shell.py`
  - `scripts/mcp/mcp_stdio.py`
  - `scripts/validate/pytest_suite.py`
  - `scripts/smoke/*.py`
  - `scripts/data/fetch_historical.py`

runtime determinism guardrails for pipeline fast-hash policy and feature-cache hash stability remain part of the admitted V2 local workflow surface.

### API, runtime, and strategy seams

The following runtime-facing seams are admitted:

- local-only API shell (`account`, `config`, `info`, `status`, `models`, `paper`, `public`, `strategy`, `ui`)
- Batch E1 admits the public candles endpoint semantics from `src/core/api/public.py` through an injected `core.server.get_exchange_client` seam for offline verification while broader transport remains deferred.
- Batch E2 admits only the read-only account endpoint semantics from `src/core/api/account.py` through an injected `core.server.bfx_read` seam for offline verification.
- Batch E3 admits the local paper/UI semantics from `src/core/api/{paper,ui}.py` through injected `core.server` helper seams for offline/local verification only.
- admitted strategy authority helpers:
  - `src/core/config/authority_mode_resolver.py`
  - `src/core/strategy/family_registry.py`
  - `src/core/strategy/family_admission.py`
  - `src/core/strategy/run_intent.py`
- Config runtime-authority semantics are admitted for source/verification purposes only.
- config/runtime authority semantics:
  - `src/core/config/authority.py`
  - `src/core/config/schema.py`
  - `src/core/api/config.py`

These surfaces are admitted for source, runtime, and verification purposes inside the current V2 scope.

### Transport and MCP surfaces

The following transport/MCP surfaces are admitted with explicit boundaries:

- Batch G1 Bitfinex REST read spine:
  - `src/core/io/bitfinex/exchange_client.py`
  - `src/core/io/bitfinex/read_helpers.py`
- Batch G2 binds generated public/account route defaults through `src/core/server.py` to the admitted Bitfinex REST read spine only; websocket, standalone auth, and paper-route transport widening remain deferred.
- the remaining `core.io.bitfinex.*` family may exist as dormant package surface only; it must not be rebound into server routes, startup wiring, or paper/live execution
- Batch H2 widens transport family to include the remaining Bitfinex REST/WebSocket modules as dormant package surface only; this slice does not rebind server routes, startup wiring, or paper/live execution.
- constrained remote MCP semantics are admitted for:
  - authorization
  - safe mode
  - confirm-token behavior
  - transport-alias behavior

Genesis-Core-V2 admits constrained remote MCP semantics limited to authorization, safe-mode, confirm-token, and transport-alias behavior already present in source.

Operational launchers, deployment/tunnel/proxy guidance, and other live-adjacent remote surfaces remain deferred.

### Optimizer, backtest, and comparison surfaces

The following are admitted in a constrained form:

- backtest comparison/diff semantics:
  - `src/core/utils/diffing/results_diff.py`
  - `tools/compare_backtest_results.py`
- Backtest comparison/diff semantics and associated tmp-path-isolated tests are admitted.
- dormant optimizer package:
  - `src/core/optimizer/**`
- supporting diffing/Optuna helpers
- repo-tracked `config/optimizer/**` research corpus

Batch I1 admits the dormant optimizer package and read-only `config/optimizer/**` research corpus for import/test completeness only.

These surfaces are admitted for import/test completeness, bounded research, and comparison workflows only.

They do **not** admit execution-root widening, startup/server bindings, or runtime-authority payload widening.

## Track B — authority migration

Track B covers authority migration and other widening work that must remain deferred until separately validated.

In lifecycle terms, Track B is where Promote-facing authority widening is considered after successful validation.

## Deferred by default

The following remain deferred unless a separate validated slice explicitly admits them:

- activation or rebinding of the dormant Bitfinex transport family into server/startup/paper/live runtime paths
- remote MCP operational launchers, deployment/tunnel/proxy guidance, and other live-adjacent surfaces
- local runtime override payloads and non-authoritative champion payloads
- backtest execution roots, result corpora, and promotion-facing execution surfaces
- optimizer execution roots such as `scripts/run/run_backtest.py`, `scripts/optimize/**`, and preflight/validation CLIs that widen authority or runtime behavior
- freeze-sensitive/runtime-authority widening without explicit validation
- unverified content migration for its own sake

## Verification loop

### Baseline checks

- In `Genesis-Core`: `python -m pytest tests/utils/test_open_v2_runtime_seed.py -q`
- Regenerate seed artifacts from `Genesis-Core` only when an explicit slice requires it: `python scripts/extract/open_v2_runtime_seed.py --clean`
- In `Genesis-Core-V2`: `python -m pytest -q`

### Local interactive workflow

- Use the local VS Code task/debug loop for repeatable API, smoke, MCP, and pytest runs
- Local VS Code tasks: `genesis-v2: api shell`, `genesis-v2: mcp stdio`, `genesis-v2: smoke suite`, `genesis-v2: pytest`
- Local VS Code debug profiles: `genesis-v2: api shell`, `genesis-v2: mcp stdio`, `genesis-v2: smoke suite`, `genesis-v2: pytest`
- Keep local editor settings aligned with `python.analysis.extraPaths`, `python.testing.*`, and `python.envFile`
- Keep editor recommendations aligned with:
  - `ms-python.python`
  - `ms-python.vscode-pylance`
  - `charliermarsh.ruff`
- Use `pre-commit install` followed by `pre-commit run --all-files` for local hygiene

### Non-installed launchers

- MCP stdio: `python scripts/mcp/mcp_stdio.py`
- API shell: `python scripts/api/api_shell.py`
- Pytest wrapper: `python scripts/validate/pytest_suite.py`
- Candle refresh: `python scripts/data/fetch_historical.py --symbol tBTCUSD --timeframes 1m 5m 15m 30m 1h 3h 6h 12h 1D 7D 14D`
- Smoke loops:
  - `python scripts/smoke/fixture_smoke.py`
  - `python scripts/smoke/backtest_smoke.py`
  - `python scripts/smoke/champion_smoke.py`
  - `python scripts/smoke/evaluate_champion_smoke.py`
  - `python scripts/smoke/model_smoke.py`
  - `python scripts/smoke/smoke_suite.py`

### Editable-install and console-script workflow

- Installable console scripts include:
  - `genesis-v2-api-shell`
  - `genesis-v2-mcp-stdio`
  - `genesis-v2-pytest`
  - `genesis-v2-champion-smoke`
  - `genesis-v2-evaluate-champion-smoke`
  - `genesis-v2-fixture-smoke`
  - `genesis-v2-backtest-smoke`
  - `genesis-v2-model-smoke`
  - `genesis-v2-smoke-suite`
- Editable install verification: `python -m pip install -e ".[dev,mcp]"`
- Installed console-script verification: `pytest tests/runtime/test_installed_console_scripts.py -q`
- Editable module loop:
  - `python -m uvicorn core.server:app --app-dir src --reload`
  - `python -m mcp_server.server`
  - `python -m pytest -q`
  - `python -m core.bootstrap.model_smoke`
  - `python -m core.bootstrap.champion_smoke`
  - `python -m core.bootstrap.evaluate_champion_smoke`
  - `python -m core.bootstrap.fixture_smoke`
  - `python -m core.bootstrap.backtest_smoke`
  - `python -m core.bootstrap.smoke_suite`
- Optional local MCP install: `python -m pip install -e ".[mcp]"`
