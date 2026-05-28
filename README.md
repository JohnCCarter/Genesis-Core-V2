# Genesis-Core-V2

Runtime-first seed with admitted local-only API shell generated from the current
`Genesis-Core` repository.

Source Genesis-Core HEAD: `2fee9429`

## What is included

- runtime kernel roots (`backtest`, `strategy`, `regime`)
- local dependency closure required by those roots
- admitted local-only API shell (`src/core/server.py`,
  `src/core/api/{config,models,status,strategy}.py`)
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
- runtime-only governance guardrails
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
- installable console scripts for the three smoke entrypoints

## What is intentionally excluded

- `src/core/api/{account,info,paper,public,ui}.py`
- `src/core/io/**`
- `src/core/pipeline.py`
- `src/core/optimizer/**`
- `src/core/strategy/features.py`
- `src/core/utils/optuna_helpers.py`
- `src/core/utils/diffing/{optuna_guard,results_diff,trial_cache}.py`
- `config/runtime.json`
- `config/runtime.seed.json`
- `config/strategy/champions/**`
- `mcp_server/remote_server.py`
- `config/mcp_settings.remote_safe.json`
- `config/mcp_settings.remote_git.json`
- `data/**`
- branch-local research corpora and historical explanation surfaces

## Notes

This seed is intentionally narrower than the source repository.
It is a local starting point, not a claim that all later bootstrap, model, champion,
or wider state-authority decisions are already resolved.
Source `config/models/**` payloads are copied into the seed, while deterministic smoke
paths use fixture-backed model registry payloads under `registry/fixtures/model_registry/**`.
Phase 1 intentionally excludes `config/strategy/champions/**`; runtime falls back to
`config/timeframe_configs.py` through `ChampionLoader` when champion payloads are absent.
The admitted API shell is local-only (`config/status/models/strategy`); exchange-facing,
paper, public-data, and UI surfaces remain excluded for a later slice.
Runtime state and champion authority payloads remain excluded; generated `.env` contains only
local-shell placeholders. Tracked `.env.example` mirrors the same narrow values for copy-forward bootstrap.
Unneeded Optuna/optimizer closure is intentionally pruned from the seed until and unless a later
explicit slice admits those higher-sensitivity surfaces.
Local MCP support is admitted for stdio-only workspace usage; remote MCP entrypoints and remote
allowlist variants remain deferred.

## Skeleton workflow

- `AGENTS.md` defines the skeleton-first repo contract.
- `.github/copilot-instructions.md` keeps local agent work aligned with generator-driven slices.
- `docs/SKELETON_SCOPE.md` records Track A vs Track B and the verification loop.
- `.vscode/mcp.json` wires VS Code to the local stdio MCP server using `config/mcp_settings.json`.
- `.vscode/tasks.json` and `.vscode/launch.json` inject `PYTHONPATH=${workspaceFolder}/src` for local non-installed loops.
- `.vscode/settings.json` aligns Python analysis/test discovery with the `src/` layout and local `.env` placeholder.
- `.vscode/extensions.json` recommends the Python/Pylance/Ruff stack for local skeleton work.
- `.env.example` keeps the narrow local placeholder values tracked even though `.env` stays ignored.

After editable install, local module commands:

Local model smoke: `python -m core.bootstrap.model_smoke`
Local champion smoke: `python -m core.bootstrap.champion_smoke`
Local champion-backed evaluate smoke: `python -m core.bootstrap.evaluate_champion_smoke`
Local bootstrap smoke: `python -m core.bootstrap.fixture_smoke`
Local backtest bootstrap smoke: `python -m core.bootstrap.backtest_smoke`
Local runtime smoke suite: `python -m core.bootstrap.smoke_suite`

Local VS Code tasks:
`genesis-v2: api shell`, `genesis-v2: smoke suite`, `genesis-v2: pytest`

Local VS Code debug profiles:
`genesis-v2: api shell`, `genesis-v2: smoke suite`, `genesis-v2: pytest`

Suggested VS Code extensions:
`ms-python.python`, `ms-python.vscode-pylance`, `charliermarsh.ruff`

Python analysis/test settings:
`.vscode/settings.json`

Console scripts after editable install:
`genesis-v2-fixture-smoke`, `genesis-v2-backtest-smoke`, `genesis-v2-smoke-suite`

Suggested install verification:
`python -m pip install -e ".[dev]"`
then run `pytest tests/runtime/test_installed_console_scripts.py -q`

Optional local MCP install:
`python -m pip install -e ".[mcp]"`
then connect the `genesis-core-v2` server from `.vscode/mcp.json`
