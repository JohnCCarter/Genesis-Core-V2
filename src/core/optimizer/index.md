# `src/core/optimizer/`

## Purpose

Contains the admitted dormant optimizer package retained for import/test completeness and bounded
research comparison surfaces in V2.

## Scope IN

- optimizer package imports
- scoring/constraint/helper semantics
- trial/cache/diffing support used by tests and audits
- bounded research completeness for admitted optimizer corpus

## Scope OUT

- optimizer execution-root authority
- startup/server binding
- runtime authority payload mutation
- promotion-facing operational claims

## Inputs

- optimizer configuration payloads
- trial metadata and cached result inputs
- audit/test harnesses

## Outputs

- optimizer helper behavior
- scored trial artifacts and parity surfaces
- deterministic diff/cache semantics used by tests

## Invariants

- package remains dormant in runtime/server authority paths
- admitted optimizer corpus is read-only for seed purposes
- import/test completeness does not imply execution-root admission

## Must Not

- appear in `core.server` as active runtime authority
- imply live optimization workflow admission
- widen into runtime startup hooks without a separate validated slice

## Related tests

- `tests/governance/test_import_smoke_backtest_optuna.py`
- `tests/utils/test_optimizer_runner.py`
- `tests/utils/test_optimizer_duplicate_fixes.py`
- `tests/utils/diffing/test_optuna_diff.py`

## Governance boundaries

- Research completeness is allowed.
- Runtime authority widening is not.
- This folder is admitted for import/test completeness only in the current seed.

## Lifecycle role / authority level

Dormant package surface. Research/verification only; not active runtime or promotion authority.
