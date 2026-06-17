# `core.packets`

## Purpose

The minimal typed packet contract for the agent-readable run-trace (ADR 0002). Packets are pure,
serializable, content-addressed records so that the human — and other agents — can read exactly what an
agent did. The schema is effectively an inter-agent API.

## Scope IN

- `EvidencePacket`, `DecisionPacket`, `GateResult` (content-addressed packets) and `RunRecord`
  (mutable run state / index entry).
- `PacketEnvelope` + `Actor` (shared, metadata-only envelope).
- Deterministic `content_hash` over the packet body only.
- Fail-closed `validate_*` functions.

## Scope OUT

- Disk I/O, the run-event spine, and the reader/query API (separate slices).
- Emit wiring into pipeline/decision boundaries.
- `CommandPacket` / `CritiquePacket`, signed signoff, and any cross-repo standard (deferred, ADR 0001).

## Inputs / Outputs

- Inputs: plain Python values supplied by callers (`run_id`, `created_at`, decision `to_dict()` payloads,
  metrics).
- Outputs: JSON-safe payloads via `to_payload()`; reconstruction via `from_payload()`; a stable
  `content_hash()`.

## Invariants

- **Deterministic identity:** `content_hash` is `fingerprint_config(body)`; it excludes every volatile
  envelope field (`run_id`, `trace_id`, `parent_run_id`, `actor`, `sequence_number`, `created_at`). Same
  body → same hash across agents and time.
- **Fail-closed:** malformed packets are rejected by `validate_*`, never silently accepted.
- **Redacted at rest:** evidence `summary`/`inputs` pass through `logging_redaction` before hashing or
  serialization, so secrets never enter a packet or its hash.
- **Authority-separated:** packets record evidence/decisions; they never issue promotion authority.
- **Pure:** no wall-clock or randomness here; `created_at`/`run_id` are supplied by the caller.

## Must not

- Sample timestamps or run IDs inside the models (keeps the layer deterministic/testable).
- Let `GateResult` become the source of promotion authority.
- Reintroduce a dependency on the intelligence domain (stable JSON lives in `core.utils.json_stable`).

## Related tests

- `tests/governance/test_packets_contract.py` — round-trip, content-hash determinism, fail-closed
  validation, redaction.

## Governance / lifecycle

Research-layer foundation (ADR 0001 "Absorbera NU"). Non-authoritative: it observes runs, it does not
gate them. Reuses `core.utils.diffing.canonical.fingerprint_config` and `core.utils.logging_redaction`.
