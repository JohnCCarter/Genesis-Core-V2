# `core.trace`

## Purpose

The append-only, per-run filesystem substrate for the agent-readable run-trace (ADR 0002). The writer
records what an agent did so the human — and other agents — can read it back later.

## Scope IN

- `TraceWriter`: owns one run; stamps run context + monotonic `sequence_number` onto each emitted
  packet; writes `run.json`, `events.jsonl`, and the `index.jsonl` cache. Convenience recorders
  (`record_evidence`, `record_decision`, `record_gate`) let callers emit without building an envelope.
- `rebuild_index`: rebuilds the index cache from the authoritative `run.json` files.
- Reader/query API (`read_run`, `read_events`, `latest_run`, `find_runs`, `follow_parents`,
  `read_evidence`): the read-only, fail-closed inter-agent surface.
- `recorder` (`record_candidate_build`, `record_backtest_run`, `resolve_actor_from_env`,
  `new_run_id`): external, fail-open helpers that emit a trace from a returned result —
  `record_candidate_build` from a `CandidateBuildPacket` (+ inputs); `record_backtest_run` from a
  `BacktestEngine.run()` dict (`kind="backtest"` evidence). They never edit or import authority from
  `decision/*`, never mutate their input, and their `GateResult`s only mirror an outcome (issue no
  promotion authority). Both deep-redact recorded results / gate criteria (free-text leaves via
  `redact_text`, sensitive keys masked) because the packet layer redacts only `EvidencePacket`
  bodies — so no input `metadata` secret reaches disk. Both honor the same ownership rule: a
  caller-provided `writer` gets evidence only (no gate/close), so multiple records can share one run.
  - **Live emitters:** `scripts/audit/build_candidate_packet.py` and `find_new_champion_candidate.py`
    under `--trace` (the latter also records `kind="backtest"` evidence per backtest). The
    `pipeline.run_backtest(trace=True)` hook is trace-capable but has **no production caller yet** —
    "backtest-trace exists" does not mean every backtest is traced.
- `paths`: TRACE_ROOT resolution (`results/trace/`, overridable via `GENESIS_TRACE_ROOT`).

## Scope OUT

- Emit wiring into pipeline/decision boundaries (Slice 4).
- Packet schemas (live in `core.packets`).

## Inputs / Outputs

- Inputs: packets from `core.packets` plus run context (`run_id`, `actor`, `intent`, ...).
- Outputs on disk under `<TRACE_ROOT>/`:
  - `<run_id>/run.json` — authoritative `RunRecord` (atomic replace).
  - `<run_id>/events.jsonl` — append-only, one packet payload per line.
  - `index.jsonl` — append-only, rebuildable cache (one line per `run.json` update).

## Invariants

- **Single writer per run** → no cross-run interleaving on `events.jsonl`.
- **`run.json` is authoritative; `index.jsonl` is a rebuildable cache.** If the index is ever
  inconsistent, `rebuild_index` regenerates it by scanning `*/run.json`. This is the cross-platform
  safety net (notably for Windows append atomicity).
- **Identity is preserved:** stamping the envelope changes locator/ordering fields only;
  `content_hash` (body-only) is unchanged.
- **Deterministic-friendly:** the clock is injectable so tests assert reproducible output.
- **Authority-separated:** writing a trace never issues promotion authority.

## Must not

- Couple to `config/authority.py` or `optimizer/**` (the atomic helpers are kept local).
- Treat `index.jsonl` as a source of truth.
- Write under a tracked path (TRACE_ROOT stays gitignored under `results/`).

## Related tests

- `tests/governance/test_trace_writer.py` — run.json/atomicity, append-only events, index
  fold-to-latest, index rebuild, two-run isolation, deterministic sequence/identity.

## Governance / lifecycle

Research-layer foundation (ADR 0001 "Absorbera NU"). Non-authoritative observation surface. Reuses
`core.packets` and `core.utils.json_stable`.
