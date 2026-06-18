# ADR 0002: Agent-readable run-trace and minimal packet contract (v1)

- Status: Accepted (2026-06-18) — the packet/trace contract is implemented (`src/core/packets/models.py`, `src/core/trace/**`) and validated by `tests/governance/test_packets_contract.py` plus the trace tests; emit-wiring into `pipeline.py`/`decision/*` remains the deferred follow-up noted under Out of scope.
- Date: 2026-06-17
- Scope: A V2-local, contract-clean run-trace substrate and the minimal typed packet set it records. Defines the schema, identity rules, on-disk layout, and read API. No emit wiring or behavior change is decided here beyond the contract itself.
- Owners: Saliba (solo dev) + AI agents

## Context

The repo audits config *state* (`logs/config_audit.jsonl` + drift detection) but does not record individual
*runs and decisions*. In the solo/agents model (ADR 0001) this is the top gap: the human must be able to see
exactly what an agent did, and — load-bearing requirement — **agents must be able to read exactly what
another agent did**. The trace is therefore a shared, agent-readable substrate whose schema is effectively
an inter-agent API.

Build it **V2-local but contract-clean**: a versioned, self-contained module that could be lifted to a
cross-repo standard later, without paying cross-repo complexity now.

## Decision

### Two distinct identities
- **`run_id`** = *which execution* (locator). Timestamp-derived, mirroring
  `optimizer/runner.py::_create_run_id` (`run_YYYYMMDD_HHMMSS`). Non-deterministic by design.
- **`content_hash`** = *what the evidence/decision is* (identity). A deterministic content fingerprint that
  **excludes** every volatile envelope field (run_id, trace_id, parent_run_id, actor, sequence_number,
  created_at). This is what an agent trusts and can reproduce when reading another agent's evidence.

### Packets (minimal set; house style of `intelligence/events/models.py`: frozen `@dataclass(slots=True)`,
`to_payload()/from_payload()`, `validate_*()`, `*_version = "...v1"`)

Common envelope on every packet: `packet_type`, `schema_version`, `run_id`, `trace_id`,
`parent_run_id|None`, `sequence_number` (monotonic per run; deterministic ordering), `actor` (`{type:
human|agent, id}`), `created_at` (ISO-8601 UTC; metadata-only), `content_hash`.

- **EvidencePacket** (body, hashed): `subject_hash`, `kind` (backtest|oos|metrics|comparison), `inputs` or
  `input_refs`, `environment_hash`, `metrics`, `dataset_refs`, `artifact_refs`, `summary` (redacted). The
  reproducible unit other agents consume.
- **DecisionPacket** (body): `decision_kind` (comparison|promotion|premortem), `result` (the `to_dict()` of
  the existing `ComparisonResult`/`PromotionResult`/`PremortemReport`), `input_evidence_refs` (content
  hashes → causal link), `reasons`. **Wraps** existing decision types; does not replace them.
- **GateResult** (body): `stage`, `status` (PASS|FAIL|WAIT|HALT), `criteria_snapshot`,
  `blocking_evidence_refs`, `signoff_ref|None`, `issued_by`. A *recorded* outcome — authority remains in the
  decision/governance code. `signoff_ref` is a forward hook (null in v1).
- **RunRecord** (trace envelope + index entry): `run_id`, `trace_id`, `parent_run_id`, `actor`, `intent`,
  `symbol`, `timeframe`, `started_at`, `ended_at|None`, `outcome`, `event_count`, `dir`.

**Hashing rule:** `content_hash = fingerprint_config(body)` reusing
`utils/diffing/canonical.py::fingerprint_config`, where `body` is the packet-specific fields only. This
guarantees *same inputs → same content_hash* across agents and time.

**Actor identity:** resolved from env `GENESIS_ACTOR_ID` (default `unknown-agent`) and `GENESIS_ACTOR_TYPE`
(default `agent`). Fail-open on *recording* (never blocks a run); fail-closed on *schema* (the field must be
present in the payload).

### On-disk layout (per-run isolation; gitignored under `results/`)
```
results/trace/                  # TRACE_ROOT (gitignored; overridable via GENESIS_TRACE_ROOT)
  index.jsonl                   # append-only, rebuildable cache of RunRecord updates
  <run_id>/
    run.json                    # authoritative RunRecord (atomic tmp+replace)
    events.jsonl                # append-only; one packet payload per line
```
- One writer per run → no cross-run interleaving on `events.jsonl`.
- `run.json` is authoritative (atomic replace). `index.jsonl` is a rebuildable cache (fold to last-per-run_id
  on read); if inconsistent it is rebuilt by scanning `*/run.json`. This sidesteps Windows append-atomicity
  concerns.

### Reader/query API (the inter-agent read surface; deterministic, read-only, fail-closed)
`read_run(run_id)` · `read_events(run_id)` · `latest_run(*, intent, symbol, timeframe, outcome)` ·
`find_runs(**filter)` · `follow_parents(run_id)` · `read_evidence(content_hash)`. Malformed records fail
closed (typed error or `None`); never silently wrong.

### Invariants
Deterministic (content hashes reproducible) · fail-closed (invalid input rejected) · immutable (records are
append-only / content-addressed) · authority-separated (the trace records evidence; it never issues
promotion authority) · local-first (no daemon, no new heavy dependency).

## Consequences

- Provides the foundation every other "Absorb NOW/PARTS" item depends on (evidence manifest, signed
  signoff, OOS evidence).
- Adds a new generated-data root (`results/trace/`) that must remain gitignored.
- A small refactor: `json_dumps_stable` is promoted from `intelligence/events/models.py` to a shared util
  (with a re-export) so `packets/` does not depend on the intelligence domain.
- The contract is intentionally minimal; CommandPacket/CritiquePacket and a cross-repo standard are deferred
  (ADR 0001, SENARE).

## Alternatives considered

- **Single shared append-only log for all runs.** Rejected: multi-writer interleaving corruption risk;
  per-run directory isolation is safer and mirrors the optimizer.
- **content_hash includes run_id/timestamp.** Rejected: would make identical evidence non-reproducible
  across runs, defeating inter-agent trust.
- **Reuse `IntelligenceEvent` as the trace event type.** Rejected: that schema is domain-specific (asset
  intelligence); the trace needs a general, decision/evidence-oriented contract. We reuse its *style*, not
  its type.

## Validation

- Determinism: same fixture body twice → identical `content_hash` (run_id/ts differ).
- Round-trip: `to_payload`/`from_payload` for every packet.
- Fail-closed: malformed payloads rejected by `validate_*`.
- Redaction: an injected fake secret is masked on disk.
- Inter-agent read: write a run, then reconstruct it via `latest_run` + `follow_parents` from a separate
  call (proves the read surface).
- No regression: `tests/governance/` green; existing suite unaffected.

## Out of scope

- Emit wiring into `pipeline.py`/`decision/*` (separate slice; must be parity- and determinism-proven).
- SignoffReport signing, CommandPacket, CritiquePacket.
- Cross-repo standardization.
- Any activation of dormant optimizer/transport surfaces or champion-freeze-sensitive changes.
