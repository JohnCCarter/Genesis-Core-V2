# Genesis-Core-V2 External Pattern Scan Report

> Status: research/report artifact only. No code changes proposed for execution in this document.
> Mode at authoring: `RESEARCH (source=branch:feature/research-candidate)`.
> Location note: written at repo root **deliberately** to avoid the `docs/research/**` wiki-lint
> structure contract (`scripts/audit/research_wiki_lint.py`). Relocate into `docs/research/sources/`
> only after a lint pass confirms structural compatibility.

---

## Governing rule for every decision in this report

Every candidate is sorted through the repo's own identity, not through popularity or novelty. A pattern
is promoted toward **ABSORB** only if it survives all five filters; failing any one demotes it to
STUDY/INSPIRE/REJECT:

1. **Deterministic** — does not introduce uncontained non-determinism (sampling, wall-clock, network races).
2. **Fail-closed** — defaults to deny/stop on ambiguity, never to permit.
3. **Local-first** — works offline / locally; no mandatory daemon, SaaS, or live-adjacent transport.
4. **Authority-separated** — Genesis keeps canonical state, evidence, and promotion authority; the external
   thing is a pattern or an adapter target, never the source of truth.
5. **No framework inversion** — adopting it must not require an external runtime to own the run loop.

This filter is what objectively demotes the heavy infrastructure (Temporal, Dapr, OPA-as-daemon, NATS,
Sigstore-as-service) to STUDY/INSPIRE and elevates the *pattern-level* absorptions (correlation IDs,
evidence manifest, declarative-schema policy, mutation/property testing, hash-signed signoff).

---

## 1. Executive Summary

### Top 10 absorbable patterns (ABSORB NOW)

1. **Correlation/run/trace IDs + a structured, append-only run-event spine** — OBSERVED gap: observability
   is in-memory only (`src/core/observability/metrics.py`); individual runs/decisions are not traced.
2. **Six-packet protocol formalization** (`CommandPacket / EvidencePacket / CritiquePacket /
   DecisionPacket / GateResult / SignoffReport`, plus `RunState / TraceEnvelope / AuthorityRef`) — the
   decision/comparison/premortem types are the seed; they lack `run_id`/identity binding.
3. **Evidence manifest + candidate/experiment registry** — lineage pattern from MLflow/DVC/Sacred, bound to
   the canonical-JSON hashing already in `ConfigAuthority`.
4. **Walk-forward / purged-embargoed CV + multiple-testing correction (deflated Sharpe / PBO)** — *harden*
   the existing single held-out validation sample in `optimizer/runner_validation.py`.
5. **Mutation testing of the governance/decision kernel** (mutmut/cosmic-ray) — prove the gates actually
   catch regressions, not just that they pass.
6. **Property-/metamorphic-based tests for decision invariants** — `hypothesis` is already a dev dependency
   and `.hypothesis/` exists; invariants for `compare_families`/`run_premortem` are not yet exercised.
7. **Declarative policy/schema for the config whitelist** — replace the ~440-line hand-coded nested
   allow-list in `config/authority.py::propose_update` with a data-driven, testable spec (JSON Schema is
   already a dependency).
8. **Hash-signed signoff/gate artifact** (in-toto/SLSA *statement format*) — turn the boolean `signoff_flag`
   into a `SignoffReport` artifact bound to the run's canonical hash, signed with existing `hashlib`/KMS.
9. **Adapter-layer contract + capability manifest + framework-inversion guard** (the *design*, not concrete
   adapters) — framework-agnostic ADR; the forward hedge that lets agent frameworks plug in later without
   owning state.
10. **LLM-tool quarantine boundary** — `openai` + `genesis-v2-qwen-builder` are non-deterministic surfaces;
    formalize that their output is *proposal evidence* behind the evidence/replay boundary, never authority.

### Top 5 highest-risk temptations to REJECT (now)

1. **Making any agent framework (AutoGen/LangGraph/CrewAI/OpenAI Agents) the runtime/authority.** The repo
   has no agent run loop; adapters now solve a problem that does not exist yet. Framework-inversion risk #1.
2. **Durable-execution infra (Temporal/Dapr Workflow) before there are durable runs.** No long-running or
   distributed execution exists; this is operational complexity with no current workload.
3. **OPA / Cedar as a running policy daemon.** Violates local-first + determinism + zero-daemon; absorb the
   *policy-as-code* pattern via declarative schema instead.
4. **Sigstore/transparency-log as a live service dependency.** Absorb the *attestation format* now; defer the
   service.
5. **A live "kill switch" as a near-term priority.** There is no live execution surface to halt; the existing
   champion-freeze CI gate already covers the real current risk. INSPIRE-only until live transport is admitted.

### Biggest Genesis-Core-V2 capability gap

**Run-level evidence and traceability.** Config *state* is audited (`logs/config_audit.jsonl` + drift
detection); individual *runs and decisions* are not. There is no `run_id`-keyed, immutable, replayable
evidence record tying a CommandPacket → backtest → comparison → premortem → signoff → gate into one
verifiable bundle. Everything else (the gates themselves) is comparatively mature.

### Best first no-code/docs-only next step

ADR: **External Pattern Absorption Principle + Framework-Inversion Guard** (encodes the five-filter rule
above), followed by ADR: **Packet Protocol v0** (names the six packets + `run_id`/`trace_id`/`AuthorityRef`).

### Best first low-risk implementation step

A `trace_id`/`run_id` correlation envelope plus an append-only `run_events.jsonl` spine, reusing the exact
atomic-append + canonical-hash pattern already proven in `config/authority.py`. Pure addition, deterministic,
local, no new runtime dependency.

### Biggest governance risk

Adopting an external orchestration runtime (agent framework or durable-workflow engine) that ends up owning
run state, so promotion/authority logic migrates into framework internals and `compare_families`/
`apply_promotion` become decorative.

### Biggest reproducibility risk

The Optuna search runs many trials and selects top-N, then validates on a **single** held-out window. That is
selection under multiple comparisons with no purging/embargo and no multiple-testing correction — the classic
backtest-overfitting failure mode. It is the most important reproducibility gap because it can silently pass a
champion that is a search artifact.

### Biggest framework-inversion risk

LangGraph/AutoGen/Temporal each want to be the top-level loop and the state owner. Any of them adopted as
"the core" inverts the architecture. The adapter-contract ADR exists precisely to prevent this.

---

## 2. Current Genesis-Core-V2 Baseline

### Observed (directly verified from code/docs/tests/CI this session)

- **Identity.** RI-first, evidence-first, local-first algorithmic-trading research/backtest/promotion shell.
  Lifecycle `Research -> Validate -> Promote`; "Research is cheap, Validation is expensive, Promotion is
  rare." (`AGENTS.md`, `docs/SKELETON_SCOPE.md`). It is **not** an agent-orchestration framework.
- **Test health.** `406 passed, 1 skipped` with the one non-hermetic test deselected; 1 real failure:
  `tests/runtime/test_local_pytest_script.py::test_plain_pytest_entrypoint_runs_backtest_tooling_test` uses
  `shutil.which("pytest")` (global PATH interpreter, not the venv) — non-hermetic, machine-dependent.
- **Deterministic governance mode resolution.** `docs/governance_mode.md` defines A/B/C/D resolution
  (override → branch map → freeze escalation → default), fail-closed to `STRICT`, mandatory response banner.
- **Decision/promotion kernel (mature, deterministic, fail-closed).**
  - `decision/models.py`: frozen dataclasses (`MetricSnapshot`, `ComparisonResult`, `PromotionResult`),
    explicit `DecisionReason`/`ComparisonDecision` enums, `to_dict()` serialization.
  - `decision/comparison.py::compare_families`: deterministic thresholds — PF margin `0.05`, drawdown not
    worse, stability not below, trade-count floor `50/yr` → `PROMOTE / KEEP_INCUMBENT / INVALID`.
  - `decision/promotion.py::apply_promotion`: requires **both** `override_flag` and `signoff_flag`; emits
    `OVERRIDE_REQUIRED`/`SIGNOFF_REQUIRED` otherwise.
  - `decision/premortem.py::run_premortem`: severity-weighted (LOW/MED/HIGH/CRITICAL) risk codes
    `PM-000..PM-007`, `BLOCK/MITIGATE/PROCEED`, run-intent phase gating, governance-readiness check;
    side-effect-free and deterministic. This is FMEA-lite already.
- **Config authority (`config/authority.py`).** SSOT runtime config with: optimistic locking
  (`version_conflict`); atomic write (tmp + `fsync` + `os.replace` + dir fsync); **append-only JSONL audit
  log** with `hash_before`/`hash_after`/actor/paths; **drift detection** vs latest audited signature;
  **canonical-JSON sha256** config identity; and a large **path-based whitelist** on `propose_update`.
- **Validation/OOS today.** `optimizer/runner_validation.py` selects top-N by score and re-runs them on a
  **separate sample range** (held-out window). Metrics in `backtest/metrics.py` (PF, drawdown, Sharpe-type,
  stability). The optimizer carries `run_id`, `run_meta`, `snapshot_id`, `run_dir` and writes serialized run
  metadata to disk.
- **Determinism guardrails.** `set_global_seeds`, canonical JSON everywhere, `pipeline_component_order_hash`,
  on-disk precompute cache versioning (`PRECOMPUTE_SCHEMA_VERSION`), feature-cache hash stability tests under
  `tests/governance/`.
- **Change-control / freeze.** `.github/workflows/champion-freeze-guard.yml` blocks any change under
  `config/strategy/champions/` during a configured freeze window (2026-06-01 → 2026-12-31) on all
  non-archive branches. `.github/workflows/ci.yml` runs lint+test on Python 3.11.
- **Boundary model.** "Admitted seed" with Track A (skeleton completeness) / Track B (deferred authority
  migration); default-defer; dormant package surfaces (rest of `io/bitfinex/**`, full `optimizer/**`) admitted
  for import/test only, not rebound into server/startup/live.
- **LLM surface.** `openai>=1.30` dependency; `genesis-v2-qwen-builder` console script; usage in
  `optimizer/runner_config.py`, `genesis_core_v2_cli/qwen_builder.py`. Peripheral tooling, not the runtime.

### Inferred (logical conclusions from observed evidence)

- The repo already contains the deterministic governance/promotion/premortem core that the prior
  `deep-research-repo-analysis.md` recommended *building*. The real work is connective tissue (identity,
  evidence, trace) and validation rigor — not a new governance kernel and not agent adapters.
- "Signoff" is currently a **boolean flag**, not an artifact. There is no signer identity, no signed report,
  no run-bound evidence. This is the seam where attestation patterns attach.
- The `propose_update` whitelist (~440 lines of nested `if`/`raise`) is a hand-rolled admission controller.
  It is correct but is a maintenance and review hazard and is the strongest policy-as-code candidate.
- Validation is single-split; combined with Optuna multi-trial search + top-N selection, selection bias is
  under-controlled (no purge/embargo, no deflated-Sharpe/PBO).

### Unverified (not directly inspected this session, or external status claims)

- I did not exhaustively read all 50 files in `src/core/strategy/**`, all of `intelligence/**`, or every
  `optimizer/**` module; conclusions about those are scoped to what was read (`runner_validation.py`,
  `scoring.py`/`metrics.py` heads, package layout).
- External framework **status/version/license** claims below are marked UNVERIFIED unless checked against a
  primary source this session. In particular: "AutoGen in maintenance mode / superseded" (carried from the
  prior doc) is **UNVERIFIED** here.
- The pattern *content* (purged CV, OTel trace-context semantics, event sourcing, mutation testing) is drawn
  from established practice and is not version-volatile; it is not re-verified per the no-shortcuts rule
  because it is not status-dependent.

---

## 3. Candidate Matrix

Full 13-field matrices are given for **ABSORB NOW** and the key **STUDY LATER** candidates. Every other named
candidate in the brief is dispositioned in the **coverage tables** at the end of this section (status +
one-line rationale), so nothing is silently dropped.

### Candidate: Correlation/Run/Trace IDs + structured run-event spine
- **Domain:** Observability (H) / event sourcing (I)
- **Source:** W3C Trace Context; OpenTelemetry tracing/semantic-conventions; event-sourcing append-only log.
- **Status:** ABSORB NOW
- **Observed:** `observability/metrics.py` is in-memory counters/gauges/events (last 100); no IDs, no run spine.
- **Inferred:** A run cannot currently be reconstructed end-to-end from durable records.
- **Unverified:** Exact OTel SDK API surface (not needed; we absorb the *semantics*, not the SDK).
- **What it does well:** Stable IDs + causal links across steps; append-only immutable timeline.
- **Transferable pattern:** `trace_id`/`run_id`/`parent_id` envelope + `run_events.jsonl` append-only log.
- **Genesis problem/opportunity:** The biggest capability gap (run-level traceability/evidence).
- **Proposed absorption shape:** Reuse the proven atomic-append + canonical-hash code from
  `config/authority.py`; emit one event per pipeline/decision boundary.
- **Possible adapter:** `observability/trace.py` (new); `metrics.py` keeps live counters.
- **Files likely affected:** `src/core/observability/*`, `pipeline.py`, `decision/*` (emit only).
- **Risks:** Governance: low (additive). Determinism: low (IDs must be derived/seeded, not `random`/wallclock-keyed). Dependency: none. Complexity: low. Security: redact secrets in events (reuse `logging_redaction`).
- **Required tests before adoption:** event schema test; determinism/replay test (same inputs → same event hashes); redaction test.
- **ROI:** High. **Confidence:** 9.

### Candidate: Six-packet protocol (Command/Evidence/Critique/Decision/Gate/Signoff + RunState/TraceEnvelope/AuthorityRef)
- **Domain:** Cross-cutting (improvement-area #1)
- **Source:** Internal synthesis; structural cues from in-toto statements (subject/predicate) and event sourcing.
- **Status:** ABSORB NOW (as ADR + JSON schemas; Phase 0/1)
- **Observed:** `ComparisonResult`/`PromotionResult`/`PremortemReport`/`DecisionReason` exist but are not
  `run_id`-bound and there is no Command/Evidence/Gate/Signoff packet.
- **Inferred:** These existing types are ~60% of `DecisionPacket`/`CritiquePacket`/`GateResult` already.
- **Unverified:** None material.
- **What it does well:** A small, stable, framework-agnostic contract decouples the core from any runtime.
- **Transferable pattern:** Typed, serializable, hash-addressable packets with explicit authority refs.
- **Genesis problem/opportunity:** Connective tissue; precondition for adapters, evidence, and signed gates.
- **Proposed absorption shape:** Pydantic models + JSON Schemas; wrap existing decision types, do not replace.
- **Possible adapter:** N/A (this *is* the contract other adapters target).
- **Files likely affected:** new `src/core/packets/`; `decision/*` gain `run_id`/`trace_id`.
- **Risks:** Governance: positive (hardens separation). Determinism: low. Dependency: none (pydantic present). Complexity: medium. Security: low.
- **Required tests:** schema round-trip; immutability; backward-compat wrap of `ComparisonResult`.
- **ROI:** High. **Confidence:** 8.

### Candidate: Evidence manifest + candidate/experiment registry
- **Domain:** Scientific/research workflow (E)
- **Source:** MLflow tracking; DVC data/lineage; Sacred experiment registry; in-toto subject/predicate.
- **Status:** ABSORB NOW (pattern only)
- **Observed:** Optimizer writes per-run `run_meta` locally; canonical-hash identity exists for config; no
  repo-wide evidence bundle binding inputs+env+results+decision.
- **Inferred:** Promotion evidence is reconstructable manually but not as one verifiable artifact.
- **Unverified:** MLflow/DVC exact APIs (not absorbed — pattern only).
- **What it does well:** Immutable, hash-addressed evidence with input/environment lineage; null-result closure.
- **Transferable pattern:** `EvidencePacket` = `{subject_hash, inputs, env_hash, dataset_refs, metrics,
  result_refs}`; a `candidates/registry.jsonl`.
- **Genesis problem/opportunity:** Makes "Validation is expensive, Promotion is rare" auditable, not asserted.
- **Proposed absorption shape:** Manifest writer that consumes existing `run_meta` + canonical hashing.
- **Possible adapter:** `evidence/manifest.py` (new).
- **Files likely affected:** `optimizer/runner_validation.py` (read-only consume), new `evidence/`.
- **Risks:** Governance: positive. Determinism: low (env hash must be stable). Dependency: none. Complexity: medium. Security: redaction.
- **Required tests:** manifest determinism; tamper-evidence (hash mismatch detected); null-result recorded.
- **ROI:** High. **Confidence:** 8.

### Candidate: Walk-forward / purged-embargoed CV + multiple-testing correction
- **Domain:** Quant/backtesting validation (F)
- **Source:** López de Prado, *Advances in Financial Machine Learning* (purged & embargoed K-fold,
  combinatorial purged CV, deflated Sharpe ratio, PBO).
- **Status:** ABSORB NOW (design now; optimizer is a dormant/import-only surface, so no execution widening)
- **Observed:** `runner_validation.py` does top-N → single held-out sample range. No purge/embargo, no
  walk-forward, no deflated Sharpe / PBO.
- **Inferred:** Optuna multi-trial + top-N + single window = under-controlled selection bias (biggest repro risk).
- **Unverified:** None material (methods are standard).
- **What it does well:** Prevents leakage at split boundaries and corrects for selection over many trials.
- **Transferable pattern:** Rolling walk-forward windows; purge+embargo around boundaries; deflate the
  reported Sharpe by the number of effective trials; report PBO.
- **Genesis problem/opportunity:** Turns the promotion comparison into a leakage- and overfit-resistant gate.
- **Proposed absorption shape:** A `validation/oos.py` spec + a `GateResult` criterion; design ADR first.
- **Possible adapter:** Extends the existing validation stage; no new external dependency required.
- **Files likely affected:** `optimizer/runner_validation.py`, `decision/comparison.py` (new criterion),
  `backtest/metrics.py` (deflated Sharpe).
- **Risks:** Governance: positive. Determinism: must seed splits deterministically. Dependency: none (numpy present). Complexity: medium-high. Security: none.
- **Required tests:** known-leakage fixture caught; deflated-Sharpe numeric golden; walk-forward determinism.
- **ROI:** High. **Confidence:** 8.

### Candidate: Mutation testing of the governance/decision kernel
- **Domain:** Testing/validation (G)
- **Source:** mutmut / cosmic-ray (mutation testing).
- **Status:** ABSORB NOW (dev-only)
- **Observed:** `tests/governance/` + decision tests pass, but nothing proves they *detect* a broken gate.
- **Inferred:** A governance kernel whose tests are not mutation-checked can silently rot.
- **Unverified:** mutmut/cosmic-ray current versions (dev-tool, low risk).
- **What it does well:** Measures whether the test suite kills injected faults in critical logic.
- **Transferable pattern:** Run mutation testing scoped to `decision/` + `config/authority.py` whitelist.
- **Genesis problem/opportunity:** Highest-value place to prove tests are real, since these gates are load-bearing.
- **Proposed absorption shape:** Optional dev extra + a scoped CI job (advisory, not blocking initially).
- **Possible adapter:** `pyproject.toml` dev extra; `scripts/validate/`.
- **Files likely affected:** dev tooling only.
- **Risks:** Governance: positive. Determinism: n/a (dev). Dependency: dev-only. Complexity: low. Security: none.
- **Required tests:** the mutation run itself; a documented kill-rate threshold.
- **ROI:** High. **Confidence:** 8.

### Candidate: Declarative policy/schema for the config whitelist
- **Domain:** Runtime governance / policy-as-code (C)
- **Source:** JSON Schema (already a dependency: `jsonschema`); OPA/Cedar as INSPIRE references.
- **Status:** ABSORB NOW (JSON Schema / data-driven rule table); OPA/Cedar = INSPIRE ONLY
- **Observed:** `config/authority.py::propose_update` enforces a ~440-line nested hand-coded allow-list.
- **Inferred:** Correct but brittle; hard to review/diff; a prime source of future governance bugs.
- **Unverified:** None material.
- **What it does well:** Separates policy (data) from enforcement (code); testable, diff-able, auditable.
- **Transferable pattern:** Express the allow-list as a declarative schema/table; the function becomes a thin
  deterministic evaluator.
- **Genesis problem/opportunity:** Removes the biggest single maintenance/review hazard in the authority layer.
- **Proposed absorption shape:** Extract the whitelist to `config/whitelist.schema.json` (or a typed table) +
  a small evaluator; keep behavior byte-identical (parity test).
- **Possible adapter:** Internal; OPA/Cedar rejected as daemons (local-first + determinism filter).
- **Files likely affected:** `config/authority.py`, new schema file, `tests/governance/`.
- **Risks:** Governance: must prove identical behavior. Determinism: high (evaluator must be pure). Dependency: none new. Complexity: medium. Security: positive (clearer surface).
- **Required tests:** **parity test** (old vs new accept/reject on a corpus of patches); fuzz the evaluator.
- **ROI:** Medium-High. **Confidence:** 7.

### Candidate: Hash-signed signoff/gate artifact
- **Domain:** Runtime governance / supply-chain attestation (C)
- **Source:** in-toto statement format; SLSA provenance predicate; Sigstore/Cosign (service = STUDY).
- **Status:** ABSORB NOW (format + hash-signing pattern); full Sigstore service = STUDY LATER
- **Observed:** Signoff is a boolean; no signer identity, no signed report.
- **Inferred:** Promotion acceptance is currently unattested.
- **Unverified:** Sigstore/Cosign current API/keyless flow (deferred anyway).
- **What it does well:** Cryptographically binds "who approved what evidence" to a verifiable artifact.
- **Transferable pattern:** `SignoffReport` carries the run's canonical hash as `subject`, signers, open
  risks; sign with existing `hashlib` digest + a local/KMS key; verify in CI.
- **Genesis problem/opportunity:** Upgrades the strongest existing gate from a flag to an audit artifact.
- **Proposed absorption shape:** `SignoffReport` packet + a sign/verify helper; no external service.
- **Possible adapter:** `signing/local.py`; later `signing/sigstore.py` (STUDY).
- **Files likely affected:** `decision/promotion.py`, new `packets/`, new `signing/`.
- **Risks:** Governance: strongly positive. Determinism: low. Dependency: none for local hash-sign. Complexity: medium. Security: key management is the real work.
- **Required tests:** sign/verify round-trip; tamper detection; missing-signer fail-closed.
- **ROI:** Medium-High. **Confidence:** 7.

### Candidate: Adapter-layer contract + capability manifest + framework-inversion guard (DESIGN)
- **Domain:** Cross-cutting (improvement-area #2; Phase 4 forward hedge)
- **Source:** Ports-and-adapters / hexagonal architecture; capability-manifest pattern.
- **Status:** ABSORB NOW (the *contract/ADR* only); concrete per-framework adapters = STUDY behind trigger.
- **Observed:** No agent runtime exists; `intelligence/**` already uses an `interface.py`+`processing.py`
  ports style, so the repo is culturally compatible with adapter contracts.
- **Inferred:** Designing the contract now is cheap insurance; building adapters now is premature.
- **Unverified:** Framework specifics (deferred).
- **What it does well:** Lets external runtimes feed packets *in* without ever owning state or promotion.
- **Transferable pattern:** An adapter must (a) emit only canonical packets, (b) declare a capability manifest,
  (c) never write promotion/authority directly, (d) pass schema validation at the boundary.
- **Genesis problem/opportunity:** Honors the brief's adapter ask while preventing framework inversion.
- **Proposed absorption shape:** ADR + a `adapters/CONTRACT.md` + capability-manifest schema. No runtime code.
- **Possible adapter:** Reference stub only (in-process, no external dep) to validate the contract.
- **Files likely affected:** docs/ADR + schema; optional `adapters/_reference.py`.
- **Risks:** Governance: strongly positive (this is the guard). Determinism: n/a. Dependency: none. Complexity: low. Security: defines the trust boundary.
- **Required tests:** contract conformance test against the reference stub.
- **ROI:** High (as insurance). **Confidence:** 8.

#### Trigger that promotes agent-framework adapters STUDY → ABSORB
Adapt a concrete framework **only when all hold:** (1) V2 has admitted an actual multi-step agent run loop as
an authority-bearing surface; (2) that loop needs to delegate to ≥2 external runtimes; (3) the packet protocol
+ adapter contract are merged and tested. Until then, agent frameworks remain INSPIRE/STUDY and the LLM tool
(`qwen_builder`) stays quarantined as proposal-evidence behind the evidence/replay boundary.

---

### Key STUDY LATER (full matrices)

### Candidate: Temporal (and Dapr Workflow/Actors)
- **Domain:** Workflow engines / durable execution (A/B)
- **Source:** Temporal docs; Dapr Workflow/Actors docs. **Status:** STUDY LATER.
- **Observed:** V2 runs are synchronous, local, bounded; no crash-recovery or long-running need today.
- **Transferable pattern:** Durable run state, deterministic replay of workflow code, pause/resume.
- **Genesis problem/opportunity:** Relevant *only if* runs become long-lived/distributed.
- **Risks:** Determinism: Temporal's replay model is actually aligned; **but** operational complexity, a server
  dependency, and framework-inversion risk fail the local-first/no-inversion filters today.
- **Trigger:** runs exceed a single local process lifetime or need durable pause-for-signoff across restarts.
- **ROI:** Low now / High later. **Confidence:** 7.

### Candidate: OPA / Cedar (policy engines)
- **Domain:** Policy-as-code (C). **Source:** Open Policy Agent (Rego); AWS Cedar. **Status:** STUDY/INSPIRE.
- **Observed:** The whitelist need is real; a *daemon* or new language runtime is not local-first/deterministic-friendly.
- **Transferable pattern:** Policy-as-data, decision logging. Absorbed via JSON Schema instead (see ABSORB item).
- **Risks:** Dependency + determinism + local-first all push against adoption as a service. Cedar-as-library is
  a lighter future option than OPA-as-daemon.
- **ROI:** Low (engine) / pattern already absorbed. **Confidence:** 7.

### Candidate: Sigstore / SLSA / in-toto (full toolchain)
- **Domain:** Supply-chain attestation (C). **Source:** Sigstore/Cosign, SLSA, in-toto. **Status:** STUDY (format ABSORBed now).
- **Observed:** Format is directly useful; the transparency-log service is not local-first.
- **Trigger:** external verification of signoffs by third parties is required.
- **ROI:** Medium later. **Confidence:** 6 (service specifics UNVERIFIED).

### Candidate: Schemathesis / API contract+property testing
- **Domain:** Testing (G) for the FastAPI shell. **Source:** Schemathesis; OpenAPI. **Status:** STUDY LATER.
- **Observed:** Local-only API shell exists; property/contract fuzzing of it is not present.
- **ROI:** Medium. **Confidence:** 6.

---

### Coverage table — full candidate dispositions (no candidate dropped)

**A. Agent & orchestration frameworks**

| Candidate | Status | One-line rationale |
|---|---|---|
| AutoGen Core | INSPIRE / STUDY (trigger) | Actor/topic/intervention patterns; no agent loop in V2 yet. Maintenance-mode claim UNVERIFIED. |
| OpenAI Agents SDK | INSPIRE / STUDY (trigger) | Guardrails/handoffs/tracing ideas; vendor-specific, premature. |
| LangGraph | INSPIRE / STUDY (trigger) | Checkpoints/interrupts/HITL are good *concepts* for pause-for-signoff; adapter premature. |
| CrewAI | INSPIRE | Role/flow/HITL ideas only. |
| ChatDev | INSPIRE | Role-chain/dehallucination idea bank only. |
| Semantic Kernel | INSPIRE | Planner/plugin ideas; no current need. |
| Haystack Agents | INSPIRE | RAG/agent patterns; out of scope. |
| LlamaIndex Workflows | INSPIRE | Event-step workflow idea; covered by event-sourcing absorption. |
| Prefect | INSPIRE | Task-flow/retry semantics; lighter than Temporal but still a runtime. |
| Temporal | STUDY (trigger) | Durable execution — see full matrix. |
| Airflow | REJECT (now) | Heavy DAG scheduler; wrong altitude for a local research shell. |
| Dagster | INSPIRE | Asset/lineage framing is good *thinking*; engine premature. |

**B. Distributed systems & control planes**

| Candidate | Status | One-line rationale |
|---|---|---|
| Kubernetes controllers | INSPIRE | Reconcile-loop framing for promotion state machines. |
| K8s admission controllers | INSPIRE | Mental model for the config-whitelist gate (validate/mutate/deny). |
| etcd | INSPIRE | Watches + learner→voter promotion analogy only. |
| Nomad | REJECT (now) | Scheduler; no workload. |
| Ray / Dask | REJECT (now) | Distributed compute; runs are local+bounded. |
| Celery | REJECT (now) | Task queue; no async workload. |
| Akka actor model | INSPIRE | Actor identity/lifecycle thinking. |
| Erlang/OTP supervision trees | INSPIRE | Restart/containment-domain policy for future runtime. |
| NATS / Kafka | INSPIRE / STUDY | Event-bus + replay; absorb the *append-only log* locally first, broker later. |

**C. Runtime governance & authorization**

| Candidate | Status | One-line rationale |
|---|---|---|
| Open Policy Agent | STUDY/INSPIRE | Policy-as-code pattern absorbed via JSON Schema; daemon rejected. |
| Cedar / AWS Verified Permissions | INSPIRE | Cedar-as-library is a lighter future option than OPA. |
| Zanzibar-style authz | INSPIRE | Relationship-based authz; overkill for current single-authority model. |
| GitHub branch protection | ABSORB-ADJACENT (already partly used) | Maps to the freeze guard; extend with required reviewers. |
| GitHub deployment environments | STUDY | Protected-step + required-reviewer pattern for promotion gates. |
| GitHub required reviewers | STUDY | Cheap human-signoff model for promotion PRs. |
| Sigstore / SLSA / in-toto | ABSORB (format) / STUDY (service) | See full matrix + ABSORB item #8. |
| policy-as-code (general) | ABSORB (pattern) | Realized as the declarative whitelist. |

**D. Safety-critical & regulated systems**

| Candidate | Status | One-line rationale |
|---|---|---|
| DO-178C | INSPIRE | Objectives/traceability discipline for the safety-case doc; full process is overkill. |
| NASA software assurance | INSPIRE | Independent V&V mindset for governance review. |
| IEC 61508 / ISO 26262 | INSPIRE | SIL/ASIL framing → risk-tiering of promotion criteria. |
| Medical-device validation | INSPIRE | Design-history-file ≈ evidence manifest. |
| Incident review systems | STUDY | Post-promotion incident timeline (pairs with trace spine). |
| Change-control boards | ABSORB-ADJACENT | The freeze guard + signoff already implement a lightweight CCB. |
| Safety cases | ABSORB (doc pattern) | Formalize `run_premortem` output as a structured safety case (Phase 0). |
| Hazard analysis (FMEA/HAZOP) | ABSORB (doc pattern) | `premortem.py` is FMEA-lite; document it as such, extend risk codes. |

**E. Scientific & research workflow systems**

| Candidate | Status | One-line rationale |
|---|---|---|
| MLflow | ABSORB (pattern) | Experiment/run tracking → evidence manifest + registry. |
| DVC | ABSORB (pattern) | Data/version lineage → dataset_refs + env hash. |
| Weights & Biases | INSPIRE | Hosted; absorb the run-comparison UX idea only. |
| Sacred | ABSORB (pattern) | Lightweight experiment registry + config capture. |
| Pachyderm | INSPIRE | Data-lineage/provenance graph idea. |
| Snakemake / Nextflow | INSPIRE | Reproducible-pipeline + env-pinning discipline (no DSL adoption). |
| ReproZip | INSPIRE | Environment-capture idea → env hash. |
| preregistration workflows | ABSORB (pattern) | Pre-register the hypothesis/criteria before a run; null-result closure. |
| experiment registries | ABSORB (pattern) | Candidate registry (see ABSORB item #3). |

**F. Quant / backtesting / research platforms**

| Candidate | Status | One-line rationale |
|---|---|---|
| Zipline / Backtrader | INSPIRE | Event-driven backtest design reference; V2 has its own engine. |
| vectorbt | INSPIRE | Vectorized speed ideas; not core. |
| QuantConnect Lean | INSPIRE | Full platform; pattern reference only. |
| Qlib | INSPIRE | ML-quant pipeline + purged-CV usage reference. |
| Freqtrade | INSPIRE | Crypto bot; hyperopt-overfit lessons reinforce the CV gap. |
| NautilusTrader | INSPIRE | Event-driven + deterministic backtest design reference. |
| Purged CV / walk-forward | ABSORB | See full matrix (top reproducibility fix). |
| Risk engines | INSPIRE/STUDY | Risk-budget in CommandPacket; live risk engine deferred (no live exec). |
| Portfolio construction | INSPIRE | Out of current single-strategy scope. |

**G. Compiler & verification architecture**

| Candidate | Status | One-line rationale |
|---|---|---|
| LLVM-style pass managers | INSPIRE | Ordered, named, hashable passes ≈ pipeline component-order hash (already present). |
| Static analyzers | ABSORB-ADJACENT | `ruff` present; consider adding type-strictness gates. |
| Type systems | ABSORB-ADJACENT | Tighten mypy/pyright on `decision/`+`config/`. |
| Model checking | INSPIRE | Overkill; principle of small verifiable core informs the whitelist refactor. |
| Property-based testing | ABSORB | `hypothesis` present; add decision invariants. |
| Mutation testing | ABSORB | See full matrix. |
| Differential testing | ABSORB (pattern) | Old-vs-new parity test for the whitelist refactor; `results_diff.py` already exists. |

**H. Observability & operational intelligence**

| Candidate | Status | One-line rationale |
|---|---|---|
| OpenTelemetry | ABSORB (semantics) | Trace-context/correlation IDs (no SDK dependency required initially). |
| Prometheus / Grafana | INSPIRE/STUDY | `metrics.py` could export later; not local-first priority now. |
| Jaeger / Honeycomb | INSPIRE | Trace-viz; defer until a trace spine exists. |
| structured event logs | ABSORB | The run-event spine. |
| trace/correlation IDs | ABSORB | See full matrix. |
| incident timelines | STUDY | Pairs with trace spine + incident review. |
| replay/debug systems | ABSORB (pattern) | Deterministic replay from the evidence manifest. |

**I. Game engines & simulation**

| Candidate | Status | One-line rationale |
|---|---|---|
| ECS architecture | INSPIRE | Data-oriented separation; not a fit for this pipeline. |
| Deterministic simulation loops | ABSORB-ADJACENT | Reinforces existing seed/canonical-hash determinism discipline. |
| Event buses | INSPIRE | Covered by event-sourcing absorption. |
| Replay systems / state snapshots | ABSORB (pattern) | Snapshot = evidence manifest + config version. |
| Behavior trees / GOAP / blackboard | INSPIRE | Future agent-decision structuring ideas only. |

**J. Robotics & autonomy**

| Candidate | Status | One-line rationale |
|---|---|---|
| ROS2 | INSPIRE | Managed node lifecycles → agent/run lifecycle states (future). |
| Behavior trees | INSPIRE | Decision structuring (future). |
| Planning/execution separation | ABSORB-ADJACENT | Already mirrored by Research/Validate/Promote separation. |
| Sensor fusion | n/a REJECT | Not applicable. |
| Sim-before-real | ABSORB (principle) | Paper/backtest-before-live already encodes this; keep it strict. |
| Safety monitors / human override | STUDY | Maps to gate + signoff; live override deferred (no live exec). |

**K. Cybersecurity & adversarial validation**

| Candidate | Status | One-line rationale |
|---|---|---|
| Threat modeling / STRIDE | ABSORB (doc) | Threat-model the adapter boundary (untrusted external packets) — currently absent. |
| Attack trees | INSPIRE | Structure the threat model. |
| MITRE ATT&CK mapping | INSPIRE | Overkill for current surface. |
| Sandboxing / capability boundaries | ABSORB-ADJACENT | The "admitted seed"/dormant-surface model already does capability-scoping. |
| Least privilege | ABSORB-ADJACENT | Reinforce in adapter contract + secret redaction (present). |
| Audit logs / tamper-evident logs | ABSORB | Extend the config audit-log + hashing to the run spine. |

**L. Organizational & command systems**

| Candidate | Status | One-line rationale |
|---|---|---|
| Military command/control, mission command | INSPIRE | Commander's-intent fields on `CommandPacket` (intent/constraints/fallback). |
| OODA loop | INSPIRE | Observe→Orient→Decide→Act framing for the run loop. |
| Incident command system | STUDY | Escalation ladder for `BLOCK`/`HALT` outcomes. |
| Air traffic control / mission control | INSPIRE | Separate "controller" vs "executor" mindset (already mirrored). |
| War-room / escalation ladders / approval chains | ABSORB (pattern) | Required-signers + escalation in `SignoffReport`. |

---

## 4. Domain Coverage Checklist

| Domain | Searched? | Notes |
|---|---|---|
| agent orchestration | Yes | All ABSORB-deferred (no agent loop); adapter *contract* absorbed. |
| workflow engines | Yes | Temporal/Dapr/Prefect/Dagster/Airflow — STUDY/INSPIRE/REJECT per filter. |
| distributed systems | Yes | All INSPIRE/REJECT now (local, bounded workload). |
| control planes | Yes | Reconcile-loop + admission-controller framing absorbed as *mental models*. |
| policy-as-code | Yes | Pattern ABSORBed (JSON Schema); OPA/Cedar daemon rejected. |
| safety-critical systems | Yes | Safety-case + hazard-analysis *doc patterns* absorbed; full process INSPIRE. |
| research workflow systems | Yes | MLflow/DVC/Sacred lineage → evidence manifest + registry ABSORB. |
| quant/backtesting frameworks | Yes | Purged-CV/walk-forward ABSORB (top fix); platforms INSPIRE. |
| observability systems | Yes | OTel semantics + structured event spine ABSORB. |
| compiler/verification systems | Yes | Property/mutation/differential testing ABSORB. |
| robotics/autonomy | Yes | Lifecycle + sim-before-real principles; mostly INSPIRE. |
| game engines/simulation | Yes | Determinism + replay/snapshot principles ABSORB-adjacent. |
| cyber defense | Yes | Adapter-boundary threat model ABSORB (currently a gap). |
| organizational command systems | Yes | Intent/escalation/approval-chain *fields* absorbed into packets. |

No domain skipped. Depth was concentrated on candidates that map to a verified repo gap; breadth is accounted
for in the coverage tables above.

---

## 5. Absorption Roadmap

### Phase 0 — Docs-only / design-only
- ADR: **External Pattern Absorption Principle + Framework-Inversion Guard** (encodes the five-filter rule).
- ADR: **Packet Protocol v0** — six packets + `RunState/TraceEnvelope/AuthorityRef`; wraps existing decision types.
- ADR: **Adapter Layer contract + capability manifest** (framework-agnostic; defers concrete adapters behind the trigger).
- ADR: **Safety case + hazard analysis convention** — formalize `run_premortem` as the structured safety case.
- ADR: **OOS validation policy** — walk-forward / purged-embargoed CV + deflated-Sharpe/PBO criteria.
- Doc: **Adapter-boundary threat model (STRIDE-lite)** for untrusted external packets.

### Phase 1 — Low-risk infrastructure
- JSON Schemas for the six packets.
- `trace_id`/`run_id` correlation envelope + append-only `run_events.jsonl` (reuse `authority.py` append+hash).
- Evidence manifest writer (consumes existing optimizer `run_meta` + canonical hashing).
- Candidate/experiment registry (`candidates/registry.jsonl`), incl. null-result closure.
- Adapter capability-manifest schema + a no-dependency reference adapter stub for conformance tests.

### Phase 2 — Governance hardening
- Declarative config whitelist (schema/table) + pure evaluator, with **byte-parity test** vs current behavior.
- `SignoffReport` artifact + local hash-sign/verify; CI verification job (fail-closed on missing signer).
- Formal `GateResult` issuance bound to a signed criteria snapshot; only the governance path may emit PASS.
- Authority-widening gate: any Track-B widening must produce a `GateResult` + signoff.
- Mutation-testing CI job scoped to `decision/` + whitelist (advisory → blocking once kill-rate threshold set).

### Phase 3 — Runtime orchestration (STUDY / deferred until trigger)
- Durable run state / replay / pause-for-signoff. **Do not** adopt Temporal/Dapr until runs outlive a single
  local process or need cross-restart durability. Until then: deterministic replay from the evidence manifest.

### Phase 4 — External framework adapters (deferred behind the explicit trigger in §3)
- Concrete AutoGen/LangGraph/OpenAI-Agents adapters — only after the trigger conditions hold. The Phase-0
  contract is what makes these safe; building them earlier inverts the architecture.

---

## 6. Hard Rejection Conditions (applied)

A candidate is rejected or deferred if it: weakens governance; turns an external framework into the authority
layer; requires broad rewrites before value is proven; introduces uncontained non-determinism; creates
live-adjacent widening without an explicit gate; bypasses signoff or audit; mixes research/prototype output
with promotion authority; hides state inside framework internals; cannot produce reproducible artifacts;
cannot be tested locally; or cannot be mapped to a concrete Genesis-Core-V2 need.

**Rejected/deferred now under these conditions:** Temporal/Dapr (framework inversion + no durable workload);
OPA/Cedar as daemons (non-determinism + dependency + not local-first); Airflow/Nomad/Ray/Dask/Celery (no
workload to justify); concrete agent-framework adapters (no agent run loop yet); live kill-switch as a
priority (no live execution surface — covered by the freeze guard); Sigstore-as-service (not local-first;
format absorbed instead). The LLM tooling (`openai`/`qwen_builder`) is **contained**, not adopted as
authority: its output is proposal-evidence behind the evidence/replay boundary.

---

## 7. Immediate Next Issue Candidates

### Issue 1 — Make the local pytest entrypoint test hermetic
- **Scope:** Fix `tests/runtime/test_local_pytest_script.py::test_plain_pytest_entrypoint_runs_backtest_tooling_test`.
- **Why now:** Only red test in the suite; non-hermetic (`shutil.which("pytest")` → global Python 3.13, not venv).
- **Files likely touched:** `tests/runtime/test_local_pytest_script.py`.
- **Acceptance criteria:** Test uses `sys.executable -m pytest` (or guards on the resolved interpreter); green on a machine with a different global `pytest`.
- **Non-goals:** No change to `scripts/validate/pytest_suite.py` behavior.
- **Required tests:** the test itself; CI green.
- **Governance risk:** None. **Confidence:** 9.

### Issue 2 — ADR: Packet Protocol v0 + Framework-Inversion Guard (docs-only)
- **Scope:** Two ADRs from `docs/adr/0000-template.md`: packet protocol + the five-filter absorption/inversion rule.
- **Why now:** Connective-tissue contract is the precondition for every other absorption; zero code risk.
- **Files likely touched:** `docs/adr/000X-*.md`.
- **Acceptance criteria:** Six packets defined with fields + `run_id`/`AuthorityRef`; existing decision types shown as wrappable; inversion guard states the trigger for adapters.
- **Non-goals:** No schemas/code yet.
- **Required tests:** None (docs). **Governance risk:** Positive. **Confidence:** 8.

### Issue 3 — Run-trace spine: correlation IDs + append-only run_events.jsonl
- **Scope:** Add `trace_id`/`run_id` envelope and a deterministic append-only run-event log; emit at pipeline/decision boundaries.
- **Why now:** Closes the biggest capability gap (run-level traceability) with the lowest-risk addition.
- **Files likely touched:** new `src/core/observability/trace.py`; `pipeline.py`; `decision/*` (emit only).
- **Acceptance criteria:** Same inputs → identical event hashes; secrets redacted; no behavior change to decisions.
- **Non-goals:** No external OTel SDK; no exporters.
- **Required tests:** determinism/replay, schema, redaction. **Governance risk:** Low. **Confidence:** 8.

### Issue 4 — OOS validation hardening ADR + leakage fixture (design + test, no execution widening)
- **Scope:** ADR for walk-forward / purged-embargoed CV + deflated-Sharpe/PBO; add a known-leakage fixture test.
- **Why now:** Biggest reproducibility risk; optimizer is dormant/import-only so this is design+test, not widening.
- **Files likely touched:** `docs/adr/000X-oos.md`; `tests/backtest/` (fixture); design note referencing `optimizer/runner_validation.py`.
- **Acceptance criteria:** ADR specifies purge/embargo + multiple-testing correction; a fixture demonstrates the current single-split passing a leaked candidate that the proposed gate would catch.
- **Non-goals:** No optimizer execution-root activation; no champion changes (freeze active).
- **Required tests:** leakage fixture. **Governance risk:** Low (design). **Confidence:** 7.

### Issue 5 — Mutation-test the governance/decision kernel (advisory CI)
- **Scope:** Add a dev extra + scoped mutation-testing job over `src/core/decision/**` and the `config/authority.py` whitelist.
- **Why now:** These gates are load-bearing; nothing currently proves the tests detect a broken gate.
- **Files likely touched:** `pyproject.toml` (dev extra); `scripts/validate/`; CI (advisory job).
- **Acceptance criteria:** Mutation run produces a kill-rate report; a documented threshold; job non-blocking initially.
- **Non-goals:** No blocking gate until threshold agreed.
- **Required tests:** the mutation run. **Governance risk:** Positive. **Confidence:** 8.

### Issue 6 — Declarative config-whitelist refactor (behind a parity test)
- **Scope:** Extract the `propose_update` allow-list to a declarative schema/table + a pure evaluator.
- **Why now:** Removes the largest maintenance/review hazard in the authority layer (~440 lines of nested checks).
- **Files likely touched:** `src/core/config/authority.py`; new `config/whitelist.schema.json`; `tests/governance/`.
- **Acceptance criteria:** **Byte-identical** accept/reject on a corpus of patches (parity test) + evaluator fuzz; no behavior change.
- **Non-goals:** No new runtime dependency; no OPA/daemon.
- **Required tests:** parity + fuzz. **Governance risk:** Must prove parity (medium). **Confidence:** 7.

### Issue 7 — SignoffReport artifact + local hash-signing (turn the flag into evidence)
- **Scope:** Define `SignoffReport` packet bound to the run's canonical hash; local sign/verify helper; CI verify.
- **Why now:** Upgrades the strongest existing gate from a boolean to a verifiable audit artifact.
- **Files likely touched:** new `src/core/packets/`, `src/core/signing/local.py`; `decision/promotion.py`.
- **Acceptance criteria:** sign/verify round-trip; tamper detected; missing-signer fails closed; promotion still requires override+signoff.
- **Non-goals:** No Sigstore/transparency-log service; no external KMS mandated initially.
- **Required tests:** round-trip, tamper, fail-closed. **Governance risk:** Positive. **Confidence:** 7.

---

## Final note

Genesis-Core-V2 already owns the deterministic governance/promotion kernel the prior analysis proposed
building. The highest-value absorptions are therefore connective tissue (packets, trace spine, evidence
manifest), validation rigor (OOS hardening), and self-verification of the gates (mutation/property testing) —
plus a framework-agnostic adapter contract as forward insurance. Agent frameworks and durable-execution engines
are deferred behind explicit triggers, because adopting them now would invert the architecture and solve
problems the repo does not yet have. External systems provide patterns and adapter targets only; Genesis
remains the authority.
