# `src/core/intelligence/`

Status: admitted (Track A) — feature/regime intelligence helpers.

## Purpose

Owns the intelligence layer that turns raw market data into structured features and regime context for
strategies: collection, evaluation, events, features, normalization, parameter handling, and regime
classification. It sits between raw indicators and strategy decisions.

## Scope IN

- feature construction and as-of caching (`features/`)
- regime classification and clarity/authority semantics (`regime/`)
- normalization, parameter, evaluation, events, and collection subsurfaces

## Scope OUT

- raw indicator math (lives in `src/core/indicators/`)
- strategy decision/authority logic (lives in `src/core/strategy/`)
- transport, runtime, or champion authority

## Inputs

- market data series and indicator outputs
- run/regime context parameters

## Outputs

- structured feature sets (deterministic, cache-keyed)
- regime context consumed by strategy logic

## Invariants

- feature as-of cache keys are deterministic for identical inputs
- no legacy feature import paths (enforced by a governance tripwire)
- regime authority/clarity semantics stay contract-bound and testable

## Must Not

- reintroduce legacy feature import paths
- make strategy/promotion decisions here
- reach into transport or champion-config surfaces

## Related tests

- `tests/core/intelligence/regime/test_authority.py`
- `tests/core/intelligence/regime/test_clarity.py`
- `tests/core/intelligence/regime/test_contracts.py`
- `tests/core/intelligence/regime/test_htf.py`
- `tests/governance/test_no_legacy_feature_imports.py`
- `tests/utils/test_features_asof_cache_key_deterministic.py`

## Governance boundaries

- Admitted as deterministic feature/regime computation; the legacy-import tripwire guards drift.

## Lifecycle role / authority level

Feature/context layer: produces inputs for Research/Validate; holds no promotion authority.
