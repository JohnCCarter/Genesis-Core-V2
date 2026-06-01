# Governance Mode (V2 SSOT)

This document is the V2 source of truth for governance mode resolution and operating expectations.

## Allowed modes

- STRICT
- RESEARCH
- SANDBOX

Default: STRICT

Explicit override: `GENESIS_GOV_MODE`

## Deterministic resolution (A/B/C/D)

Resolution is deterministic and must be evaluated in this exact order.

### A) Explicit override

If `GENESIS_GOV_MODE` is set:

- Accept only `STRICT`, `RESEARCH`, `SANDBOX`.
- Invalid value must fail-closed to `STRICT`.

### B) Branch mapping (exact)

- `master -> STRICT`
- `release/* -> STRICT`
- `champion/* -> STRICT`
- `feature/* -> RESEARCH`
- `research/* -> RESEARCH`
- `sandbox/* -> SANDBOX`
- `spike/* -> SANDBOX`

### C) Freeze escalation

Force `STRICT` if either condition is true:

- a touched path is under `config/strategy/champions/`, OR
- `.github/workflows/champion-freeze-guard.yml` is modified.

### D) Default fallback

If no prior rule resolves a mode, use `STRICT`.

## Fail-closed policy

- Invalid override values always resolve to `STRICT`.
- Unresolved or ambiguous states always resolve to `STRICT`.
- Governance mode resolution must remain deterministic and fail-closed.

## Mandatory mode banner

Every response must begin with this exact format:

`Mode: <MODE> (source=<resolution reason>)`

Examples:

- `Mode: STRICT (source=branch:master)`
- `Mode: RESEARCH (source=branch:feature/composable-v2)`
- `Mode: STRICT (source=freeze-signal)`
- `Mode: SANDBOX (source=branch:spike/idea-x)`

## Operational expectations per mode

### STRICT

- Packet-first for non-trivial work.
- Require explicit authority before entering behavior/config/runtime/comparison/champion surfaces.
- Fail closed on ambiguity.

### RESEARCH

- Prefer the smallest admissible research step.
- Prefer the minimum artifacts/docs needed for traceability.
- Do not add STRICT-style process unless a strict-only surface is touched or mode re-resolves to `STRICT`.
- Avoid unnecessary packet proliferation when authority is already clear.

Controlled dirty research is allowed only for isolated evidence-surface work inside `RESEARCH`; it is not a separate governance mode.

### SANDBOX

- Prefer fast exploration, sketches, and disposable work.
- No production-near, merge-ready, or `införd` claims.
- Keep experimentation separated from tracked governed artifacts.

## Policy by mode

### STRICT

- Full gates required for non-trivial slices.
- No behavior change by default.
- Behavior changes require explicit exception.

### RESEARCH

- Determinism replay required when runtime/comparison semantics are touched.
- Pipeline invariants required when the slice touches pipeline/runtime authority surfaces.
- Behavior change is allowed only if behind a flag/version.
- Default behavior must remain unchanged.
- A parity test should prove identical default behavior when defaults are in scope.

### SANDBOX

- Rapid experimentation is allowed.
- Determinism replay is optional.
- Must not modify champion freeze-sensitive surfaces.

## Strict-only surfaces

This list is an operational stop/escalate list and does not change deterministic mode resolution.

- `config/strategy/champions/`
- `.github/workflows/champion-freeze-guard.yml`
- strategy-family rule surfaces
- runtime-default authority surfaces
- comparison, readiness, and promotion surfaces

## Constraints

- Do not weaken freeze protection.
- Do not allow SANDBOX to override freeze escalation.
- Keep mode resolution deterministic and fail-closed.
