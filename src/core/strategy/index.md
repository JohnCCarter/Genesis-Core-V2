# `src/core/strategy/`

## Purpose

Owns strategy evaluation, family admission, champion loading, model-driven decision logic, and
runtime strategy helper seams for the admitted V2 runtime kernel.

## Scope IN

- strategy family identity and admission
- run-intent classification
- champion loading and fallback behavior
- deterministic decision/evaluate/proba/confidence helpers
- RI runtime strategy composition already admitted in V2

## Scope OUT

- legacy authority reactivation
- live transport execution wiring
- free-form research notebooks as runtime truth
- optimizer execution-root admission

## Inputs

- runtime/seed/champion config payloads
- model registry payloads
- evaluation inputs from runtime pipeline
- run-intent and family identity metadata

## Outputs

- actions and decision metadata
- champion-backed effective configs
- family admission results
- evaluation signals consumed by runtime pipeline

## Invariants

- `ri` remains the sole active family on authority-facing V2 surfaces
- champion miss-path fallback resolves to `config/runtime.seed.json`
- admitted helpers stay deterministic and test-backed
- family admission must not widen authority by accident

## Must Not

- treat archival legacy material as active authority
- bypass family admission or run-intent rules
- rebind dormant transport or optimizer surfaces into runtime authority
- allow non-authoritative champion artifacts to act as defaults

## Related tests

- `tests/runtime/test_stateful_authority_payloads.py`
- `tests/runtime/test_strategy_authority.py`
- `tests/core/strategy/test_family_admission.py`
- `tests/core/strategy/test_families.py`

## Governance boundaries

- Research may generate strategy hypotheses.
- Validate may verify strategy behavior.
- Active strategy authority remains bounded to admitted RI surfaces only.

## Lifecycle role / authority level

Mixed runtime + authority-adjacent strategy surface. Parts of this folder are active authority
helpers; other parts remain validation/runtime helpers without promotion authority on their own.
