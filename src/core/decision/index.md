# `src/core/decision/`

## Purpose

Holds deterministic comparison, promotion, and premortem logic for candidate-versus-incumbent
evaluation in V2.

## Scope IN

- metric validation for decision inputs
- incumbent vs candidate comparison rules
- promotion gate semantics
- deterministic premortem reflection over verified evidence

## Scope OUT

- runtime trade execution
- free-form risk narrative
- discretionary market commentary
- mutation of config/champion authority by itself

## Inputs

- `MetricSnapshot` payloads
- run-intent
- lifecycle phase (`validate` / `promote`)
- explicit override and signoff flags

## Outputs

- comparison decisions
- promotion decisions
- deterministic premortem reports
- machine-readable reason codes

## Invariants

- fail-closed on missing required evidence
- no subjective decision claims
- premortem remains post-validation and pre-promotion
- `ri` remains the only active family on authority-facing V2 surfaces

## Must Not

- infer promotion authority from narrative judgment
- speculate about market conditions without deterministic evidence
- rely on `assert` for contract-critical incumbent/candidate completeness
- widen into runtime execution or API authority mutation

## Related tests

- `tests/test_family_decision.py`
- `tests/test_premortem_system.py`

## Governance boundaries

- Validate produces evidence.
- Premortem reflects on verified failure modes only.
- Promote consumes validated evidence plus explicit signoff/override.
- Decision outputs must stay deterministic and evidence-backed.

## Lifecycle role / authority level

Validate / Promote-adjacent decision surface. This folder informs promotion gating but does not
itself create promotion authority.
