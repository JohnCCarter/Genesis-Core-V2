# `src/core/config/`

## Purpose

Defines V2 runtime config authority semantics, schema enforcement, validation boundaries, and
authority-mode normalization.

## Scope IN

- runtime config schema
- runtime authority load/validate/propose semantics
- authority-mode normalization and guardrails
- config validation contracts used by API and tests

## Scope OUT

- discretionary strategy evaluation
- promotion decisions
- live transport behavior
- non-authoritative runtime payload archives

## Inputs

- repo-tracked `config/runtime.seed.json`
- validated runtime patches
- bearer-guarded propose requests through admitted API seams

## Outputs

- validated runtime config snapshots
- canonicalized authority-mode payloads
- deterministic config hashes and audit records

## Invariants

- repo-tracked seed remains the baseline fallback
- local `config/runtime.json` stays excluded from seed authority
- authority-mode resolution is deterministic and fail-closed
- runtime authority remains RI-only on active V2 surfaces

## Must Not

- silently widen authority to legacy/default fallbacks outside admitted rules
- bypass validation or whitelist checks
- turn docs/examples into runtime authority
- mutate authority state without explicit guarded path

## Related tests

- `tests/runtime/test_config_authority_semantics.py`
- `tests/governance/test_authority_mode_resolver.py`
- `tests/integration/test_config_endpoints.py`

## Governance boundaries

- Source/verification semantics are admitted.
- Runtime state mutation remains guarded and narrow.
- Active authority is RI-first and fail-closed on ambiguity.

## Lifecycle role / authority level

Runtime authority surface. This folder defines authoritative config semantics but remains bounded by
repo-tracked seed rules and guarded propose paths.
