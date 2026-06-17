# ADR 0001: External pattern absorption tiers for the solo/agents operating model

- Status: Proposed
- Date: 2026-06-17
- Scope: How Genesis-Core-V2 decides what external patterns to absorb, given its operating model. Strategy/policy only — no runtime or authority change.
- Owners: Saliba (solo dev) + AI agents (Claude + possibly other agents)

## Context

The only actors across these repos are one solo human developer and AI agents. There is no human team and
no external verifier. This flips the *purpose* of the repo's governance layer: it exists to **contain and
audit AI agents, with the human as the sole gate** — not to coordinate humans or satisfy external
compliance. Part of the governance (trace, fail-closed defaults, self-verification) exists to keep the
agents — including Claude itself — honest.

`external-pattern-scan-report.md` (repo root) scanned the wider world for patterns to absorb without
replacing Genesis identity. Its recommendations need a single, durable sorting rule so future absorption
decisions are derived from the repo's identity rather than from taste or popularity.

## Decision

Adopt one driving rule and three tiers.

**Driving rule:** *Patterns that let us see and mechanically catch agent error are absorbed NOW. Patterns
that require a second human or an external verifier are LATER or never. Patterns worth their idea but not
their full system are absorbed in PARTS (take the format/pattern, drop the ceremony).*

Every candidate is sorted through the repo's five identity filters; failing any one demotes it:
deterministic · fail-closed · local-first · authority-separated · no framework inversion.

### Absorbera NU
- Agent-readable run-trace + minimal packet contract (see ADR 0002).
- OOS-validation hardening (design + leakage fixture; optimizer stays dormant).
- Mutation testing of the decision kernel (the missing human reviewer, made mechanical).
- Property/metamorphic tests for `compare_families` / `run_premortem`.
- LLM/agent quarantine policy: agent/LLM output is proposal-evidence, never authority.
- The framework-inversion-guard *principle*; the hermetic-test fix.

### Absorbera DELAR (absorb the part, drop the ceremony half)
- `run_id` + minimal Evidence/Decision/Gate packets wrapping existing decision types — not the full
  six-packet ceremony.
- Manifest/lineage pattern bound to existing canonical hashing — not MLflow/DVC/W&B as systems.
- Tamper-evident hash + structured SignoffReport (manifest hash + the human's override) — not external
  cryptographic signing (Sigstore/KMS), because there is no third party to verify against.
- in-toto/SLSA statement *shape*, OpenTelemetry *semantics*, FMEA/safety-case *doc convention*,
  mission-command *fields* — not their full toolchains/processes.
- Policy-as-code via JSON Schema/table for the config whitelist (parity-tested) — not OPA/Cedar as an
  engine. Not urgent; the current whitelist works.

### Absorbera SENARE (behind explicit triggers; some may be never)
- Full packet protocol + cross-repo standard — after the V2-local contract is proven.
- Full adapter contract + concrete agent-framework adapters — only when V2 grows an authority-bearing agent
  run loop that must delegate to ≥2 external runtimes.
- Durable execution (Temporal/Dapr) — when runs outlive a single local process or become distributed.
- Sigstore service / KMS / required reviewers / separate audit-tee — needs a second human or external
  verifier → **maybe never** in this model.
- schemathesis / Prometheus-Grafana-Jaeger exporters — after the surfaces they observe exist.

## Consequences

- Absorption decisions become derivable from the operating model, not re-litigated per candidate.
- Effort concentrates on what protects a solo+agents workflow (visibility + mechanical self-verification)
  instead of human-coordination ceremony.
- Some industry-standard practices (external signing, required reviewers) are explicitly deprioritized; if
  the operating model ever gains a second human, this ADR must be revisited.

## Alternatives considered

- **Option A — absorb the full agent-framework + durable-execution stack now** (the earlier
  `deep-research-repo-analysis.md` direction). Rejected: the repo has no agent run loop or long-running
  execution; it would invert the architecture and solve problems that do not exist yet.
- **Option B — absorb nothing; keep the current kernel as-is.** Rejected: leaves the real gap (run-level
  traceability) and the real risk (selection bias in validation) unaddressed.

## Validation

- The tiers map every "ABSORB NOW" item to a verified repo gap in `external-pattern-scan-report.md`.
- ADR 0002 instantiates the first NU item with concrete, testable invariants.

## Out of scope

- Any runtime, authority, or promotion behavior change.
- Activation of dormant optimizer/transport surfaces.
- Champion-freeze-sensitive surfaces (freeze active 2026-06-01 → 2026-12-31).
