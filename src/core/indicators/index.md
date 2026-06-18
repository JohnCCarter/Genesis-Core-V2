# `src/core/indicators/`

Status: admitted (Track A) — pure technical-indicator computation helpers.

## Purpose

Owns the technical-indicator family: pure functions that turn price/volume series into derived signals
(ADX, ATR, Bollinger, EMA, RSI, Fibonacci, and the HTF Fibonacci variants). These are computation
primitives consumed by strategies and the backtest engine.

## Scope IN

- core indicators (`adx.py`, `atr.py`, `bollinger.py`, `ema.py`, `rsi.py`, `fibonacci.py`)
- derived/exit features (`derived_features.py`, `exit_fibonacci.py`)
- HTF Fibonacci computation and context (`htf_fibonacci*.py`)

## Scope OUT

- strategy decision logic (lives in `src/core/strategy/`)
- regime/feature intelligence (lives in `src/core/intelligence/`)
- any I/O, transport, or runtime authority

## Inputs

- OHLCV series and indicator parameters

## Outputs

- indicator values / derived feature series, deterministic for a given input

## Invariants

- functions are pure and side-effect-free (no I/O, no global state)
- deterministic output for identical input
- no strategy or authority decisions are made here

## Must Not

- reach into transport, config-authority, or champion surfaces
- carry hidden state across calls

## Related tests

No dedicated unit tests today; indicators are exercised indirectly through the engine fixture smoke
(`tests/runtime/test_backtest_engine_fixture_smoke.py`) and feature-cache determinism
(`tests/utils/test_features_asof_cache_key_deterministic.py`). A dedicated per-indicator test slice is a
reasonable future Validate-lane addition.

## Governance boundaries

- Pure computation surface; no governance-sensitive behavior.

## Lifecycle role / authority level

Computation primitive: feeds Research/Validate work; holds no authority.
