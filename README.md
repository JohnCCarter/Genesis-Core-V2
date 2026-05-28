# Genesis-Core-V2

Runtime-only Phase-1 seed generated from the current `Genesis-Core` repository.

Source Genesis-Core HEAD: `c9e42b21`

## What is included

- runtime kernel roots (`pipeline`, `backtest`, `strategy`, `regime`)
- local dependency closure required by those roots
- narrow config bootstrap (`config/__init__.py`, `config/timeframe_configs.py`,
    `config/backtest_defaults.yaml`)
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

- `src/core/server.py`
- `src/core/api/**`
- `src/core/strategy/features.py`
- `src/core/config/validator.py`
- `config/runtime.json`
- `config/runtime.seed.json`
- `config/strategy/champions/**`
- `data/**`
- branch-local research corpora and historical explanation surfaces

## Notes

This seed is intentionally narrower than the source repository.
It is a local starting point, not a claim that all later bootstrap, model, champion,
or API/service decisions are already resolved.
Source `config/models/**` payloads are copied into the seed, while deterministic smoke
paths use fixture-backed model registry payloads under `registry/fixtures/model_registry/**`.
Phase 1 intentionally excludes `config/strategy/champions/**`; runtime falls back to
`config/timeframe_configs.py` through `ChampionLoader` when champion payloads are absent.

Local model smoke: `python -m core.bootstrap.model_smoke`
Local champion smoke: `python -m core.bootstrap.champion_smoke`
Local champion-backed evaluate smoke: `python -m core.bootstrap.evaluate_champion_smoke`
Local bootstrap smoke: `python -m core.bootstrap.fixture_smoke`
Local backtest bootstrap smoke: `python -m core.bootstrap.backtest_smoke`
Local runtime smoke suite: `python -m core.bootstrap.smoke_suite`

Console scripts after editable install:
`genesis-v2-fixture-smoke`, `genesis-v2-backtest-smoke`, `genesis-v2-smoke-suite`

Suggested install verification:
`python -m pip install -e ".[dev]"`
then run `pytest tests/runtime/test_installed_console_scripts.py -q`
