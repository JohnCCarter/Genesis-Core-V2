# `src/core/backtest/`

Status: admitted (Track A) — engine, metrics, exit strategies, and comparison/diff semantics.

## Purpose

Owns the offline backtest engine and its supporting surfaces: the candle-driven engine and precompute,
per-trade position/cost tracking, metrics, and the HTF exit-strategy family. This is where a strategy's
historical behavior is simulated and scored.

## Scope IN

- backtest engine and precompute (`engine.py`, `engine_precompute.py`, `engine_results.py`)
- position/cost tracking and trade logging (`position_tracker.py`, `trade_logger.py`)
- metrics computation (`metrics.py`)
- exit-strategy logic, including the HTF exit family (`exit_strategies.py`, `htf_exit_*.py`)

## Scope OUT

- execution roots / run launchers (`scripts/run/run_backtest.py`, `scripts/optimize/**`) — deferred (Track B)
- champion-config changes (frozen through 2026-12-31)
- live/paper execution or order routing
- order-book / VWAP slippage derivation (planned, deferred — see the research wiki methodology page)

## Inputs

- OHLCV candle data and strategy configs
- commission / slippage cost inputs (independent, per-trade)

## Outputs

- simulated trades, equity, and per-trade cost application
- backtest metrics and results objects for comparison/diff

## Invariants

- commission and slippage are independent inputs (fee ≠ slippage)
- slippage is applied as a flat symmetric proxy against candle price today (no order-book depth exists)
- comparison/diff semantics stay tmp-path-isolated, carrying no execution roots or results corpora

## Must Not

- introduce execution roots or server/startup wiring for backtest runs
- rebind dormant transport (`core.io.bitfinex.ws_public`) to source live depth
- alter frozen champion config

## Related tests

- `tests/runtime/test_backtest_engine_fixture_smoke.py`
- `tests/runtime/test_pipeline_defaults.py`
- `tests/backtest/test_reconcile_forward_backtest.py`
- `tests/backtest/test_compare_backtest_results.py`
- `tests/governance/test_dead_code_tripwires.py`

## Governance boundaries

- Admitted as offline simulation + comparison/diff semantics only.
- Execution-root and runtime-authority widening remain deferred (Track B); cost-fragility validation is
  post-freeze (GitHub Issue #12).

## Lifecycle role / authority level

Research/Validate evidence surface: produces backtest evidence; holds no promotion authority by itself.
