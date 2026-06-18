# Research log

> **Boundary note:** this file is an append-only chronology for `docs/research/`.
> It records research-layer updates and source-ingest moments.
> It is not a runtime-authority surface.

## Entry format

Use:

`## [YYYY-MM-DD] kind | short title`

Suggested kinds:

- `bootstrap`
- `ingest`
- `update`
- `lint`
- `question`
- `close`

## [2026-06-04] bootstrap | initialize research knowledge layer

- Created `docs/research/index.md` as the bounded research knowledge-layer contract.
- Created `docs/research/champion-results-review.md` as the first active topic page.
- Seeded the page with current evidence links for:
  - `config/strategy/champions/tBTCUSD_1h.json`
  - `config/strategy/champions/tBTCUSD_3h.json`
  - `config/optimizer/3h/phased_v3/PHASED_V3_RESULTS.md`
  - `artifacts/diagnostics/v2_gap_audit_2026-06-01.md`
- Intent: keep champion-results review durable, repo-tracked, and non-load-bearing for future
  agent sessions.

## [2026-06-04] ingest | verify champion loader fallback semantics

- Read and linked the current loader implementation in `src/core/strategy/champion_loader.py`.
- Confirmed via `tests/runtime/test_stateful_authority_payloads.py` that both tracked champion
  files currently resolve to `baseline:runtime_seed` at runtime.
- Confirmed via `tests/governance/test_v2_seed_boundaries.py` that the repo contract explicitly
  treats the tracked subset as demoted while seed fallback remains active.
- Updated `docs/research/champion-results-review.md` with a source-backed finding so future
  sessions do not need to rediscover this seam from scratch.

## [2026-06-04] update | reconcile current champion authority wording

- Reconciled `README.md` and `docs/SKELETON_SCOPE.md` around the current champion/runtime
  authority contract.
- Added one compact statement clarifying that the tracked champion subset is admitted and
  evidence-bearing, but demoted for runtime authority.
- Kept the existing Batch F wording intact while making the runtime-active fallback behavior more
  explicit for human readers and future agents.
- Updated `docs/research/champion-results-review.md` so the research layer reflects the new repo
  wording.

## [2026-06-04] update | productize research knowledge layer

- Elevated `docs/research/**` from a minimal knowledge layer to a first-class, repo-tracked
  knowledge product for V2 growth.
- Added `docs/research/map.md` as the navigation/registry surface and
  `docs/research/templates/topic-template.md` as the canonical topic-page template.
- Anchored the product in `README.md`, `docs/SKELETON_SCOPE.md`, `seed_manifest.json`, and
  `tests/governance/test_v2_seed_boundaries.py`.
- Kept the product plain-Markdown, Obsidian-friendly, and explicitly non-authoritative.

## [2026-06-04] update | admit research patterns fully

- Added explicit product surfaces for three admitted research patterns:
  - atomic runnable artifacts
  - black-box experiments
  - agent handoff/log continuity
- Added new templates for experiment and handoff notes plus an artifact contract surface.
- Updated `index.md`, `map.md`, `seed_manifest.json`, and governance coverage so these patterns
  are now first-class within the research knowledge product.

## [2026-06-04] update | align product to full karpathy llm-wiki shape

- Clarified the Karpathy-style three-layer mapping inside `docs/research/index.md`:
  raw sources, wiki, and schema.
- Added explicit source, query, and lint surfaces plus `operations.md` for the ingest/query/lint
  loop.
- Added durable query and lint templates plus a structural lint script entrypoint for the research
  wiki.
- Extended manifest/test coverage so the fuller schema/index/log/operations shape is now tracked in
  repo contract surfaces.

## [2026-06-04] question | file back karpathy agent discipline answer

- Added `docs/research/queries/2026-06-04-karpathy-agent-discipline.md` as the first durable
  query-answer page in the product.
- Captured the repo-facing implication of Karpathy-style agent discipline:
  schema/index/log structure, durable artifacts, and explicit ingest/query/lint workflow.
- Registered the query page in `map.md` so later sessions can reuse it without depending on chat
  history.

## [2026-06-04] lint | run first research wiki structure health check

- Ran `python scripts/audit/research_wiki_lint.py` after the fuller Karpathy-style wiki alignment.
- Confirmed zero missing paths and zero missing markers across the current schema/index/log and
  support surfaces.
- Recorded the first lint pass in `docs/research/lint/2026-06-04-structure-health-check.md`.

## [2026-06-04] question | file back NVIDIA skills cherry-pick review

- Reviewed `NVIDIA/skills` against the current V2 research-wiki and scope boundaries.
- Captured the conclusion that V2 should cherry-pick lightweight governance, evaluation,
  performance, and security patterns before considering any RAG/AI-Q deployment slice.
- Added `docs/research/queries/2026-06-04-nvidia-skills-cherry-pick-review.md` so later
  sessions can reuse the decision without relying on chat history.

## [2026-06-04] update | add V2 capability card template

- Added `docs/research/templates/capability-card-template.md` as the first V2-native adaptation
  from the NVIDIA skills audit.
- Registered capability cards as a research-only pattern for describing bounded agent, tool,
  endpoint, workflow, or checklist capabilities.
- Kept the card explicitly non-authoritative: it documents scope, risks, boundaries, validation,
  and promotion path without importing external runtime stacks.

## [2026-06-04] update | add V2 eval and endpoint security templates

- Added `docs/research/templates/evaluation-record-template.md` to capture eval/perf/security
  evidence with candidate, baseline, signals, result, interpretation, and promotion decision.
- Added `docs/research/templates/endpoint-security-checklist-template.md` to capture endpoint,
  MCP, hosted-model, and agent-tool trust boundaries with deny-by-default safety assumptions.
- Registered both as V2-native adaptations of NVIDIA skill patterns without adding RAG, AI-Q,
  NeMo, deployment, or runtime dependencies.

## [2026-06-04] update | add repo-local V2 research review skill

- Added `.github/skills/v2-research-review/SKILL.md` as a project-local agent skill for bounded
  research-wiki reviews.
- The skill points agents toward capability cards, evaluation records, endpoint security
  checklists, and existing wiki templates while preserving Research -> Validate -> Promote order.
- Kept the skill as guidance only; it does not create runtime, config, transport, deployment, or
  promotion authority.

## [2026-06-04] update | tighten NVIDIA pattern adaptations

- Added `docs/research/templates/evidence-pipeline-template.md` for scan -> review -> evidence
  records without NVIDIA signing or external attestation.
- Tightened capability cards with owner, purpose, risks, outputs, version/provenance, evidence,
  limitations, and scan/review/evidence state.
- Tightened eval/perf records with artifact layout, summary table, and failure table.
- Tightened endpoint security checklists with endpoint trust confirmation, no-secrets-in-prompts,
  deny-by-default egress, and path/method scoped external calls.
- Split `.github/skills/v2-research-review` into small `SKILL.md`, detailed `references/**`,
  explicit `scripts/**` boundary, and compatibility notes.

## [2026-06-08] update | restore research wiki and ecosystem inventory docs

- Restored `docs/agent-ecosystem-inventory.md` into the repo from the recoverable historical PR #2
  content.
- Restored the broader Karpathy-style research wiki under `docs/research/**` from local
  unreachable commit evidence.
- Restored `scripts/audit/research_wiki_lint.py` and
  `tests/runtime/test_local_research_wiki_lint_script.py` so the recovered wiki has a repo-local
  structural verification loop again.
- Ran the recovered wiki lint and focused test successfully before removing temporary forensic
  recovery artifacts.
- Added a dated handoff note so future sessions can start from the restored wiki rather than repeat
  transcript/PR archaeology.

## [2026-06-17] update | record external-pattern absorption decision and trace foundation

- Added `docs/adr/0001-absorption-tiers-solo-agents.md` and `docs/adr/0002-run-trace-packet-contract.md`
  to canonize WHY and HOW V2 absorbs external patterns. The operating model (one solo human + AI agents)
  means governance exists to contain and audit agents, with the human as sole gate; external systems are
  pattern sources only, never V2 authority.
- Captured the full external scan in `external-pattern-scan-report.md` (repo root): NU/DELAR/SENARE
  absorption tiers sorted by the repo's five identity filters (deterministic, fail-closed, local-first,
  authority-separated, no framework inversion).
- First NU slice in progress: an agent-readable run-trace + minimal packet contract so future agents can
  read exactly what a prior agent did (`run_id` locator vs reproducible `content_hash` identity).
- Recorded the absorption rationale as `Pattern 7` in `docs/research/patterns.md` so later sessions meet
  the why before touching external-pattern work.

## [2026-06-17] question | champion 1h trade-frequency finding (Issue #12)

- Filed `queries/2026-06-17-champion-1h-trade-frequency.md`: the tracked `tBTCUSD_1h` champion is
  effectively inert (0.70 entry gate -> ~3 trades / 30 months); a 0.60 gate reveals a real but
  cost-fragile edge (183 trades, Sharpe > 1.0 at low cost, dies by ~10 bps). The proposed 3h 2x-sizing
  re-tune was neutral-to-worse.
- Source numbers are the (now-deleted) research branch's own self-reported cost-stress sweeps;
  reproduce via `scripts/analyze/cost_stress_sweep.py` before acting. Deferred to post-freeze
  (after 2026-12-31), tracked as GitHub Issue #12.

## [2026-06-17] update | run-trace foundation merged; research tooling + GitHub hardening

- Merged the run-trace foundation (`core.packets` + `core.trace`) and the salvaged research tooling to
  `main`: optimizer robustness (PSR/DSR/PBO-CSCV/FDR), cost-stress sweep, forward/backtest reconcile,
  and the edge-mechanism register (`mechanism_registry.py` + `docs/strategies/MECHANISMS.md`).
- `EDGE_MAP=UNRESOLVED` still holds; the tooling to test mechanisms toward `CANDIDATE` now exists.
- Hardened the repo (branch protection, Dependabot security + auto-merge, deliberate dep-major holds).
  Baton-pass in `handoffs/2026-06-17-config-merges-and-github-hardening.md`.

## [2026-06-17] question | file back karpathy wiki fidelity review

- Added `docs/research/queries/2026-06-17-karpathy-wiki-fidelity-review.md`
  comparing the V2 research wiki to Karpathy's `llm-wiki` gist.
- Conclusion: faithful in form (raw→wiki→schema layers, ingest/query/lint loop,
  content-oriented map, prefixed append-only log) but deliberately divergent in
  motor (LLM-owned/low-friction/wiki-as-truth → human-gated/high-friction/
  derivative-non-authority).
- Recorded the largest open gap vs the gist: `research_wiki_lint.py` is a
  structural presence check, not a semantic lint (no contradiction/orphan/
  broken-link detection).
- Registered the page in `map.md` and `queries/index.md`.

## [2026-06-18] update | agent-native lint + framing for the research wiki

- Extended `scripts/audit/research_wiki_lint.py` with a referential-integrity check (unregistered
  dated pages + dangling registry references). Warn-only: it does not flip the structural `ok`. Added
  positive and negative tests in `tests/runtime/test_local_research_wiki_lint_script.py`.
- Lint caught real rot: `map.md` and `index.md` both pointed at `.github/skills/v2-research-review/`
  which never existed (carried since admission). Removed the stale "Companion agent workflow" section
  from both; `log.md` history left intact.
- Sharpened the agent-native framing in `patterns.md` (Pattern 7), `map.md`, and `operations.md`:
  the wiki is an agent-native tool (agent curates sources + writes + reads; human only asks questions)
  whose job is millisecond orientation — context restore without re-scanning the repo. Authority is
  still promoted out; referential lint mechanizes integrity only, not semantic consistency.

## [2026-06-18] question | slippage/cost methodology filed

- Filed `slippage-backtest-methodology.md`: Bitfinex publishes no general slippage figure, so slippage
  must be derived from order-book depth (VWAP walk vs a reference price, mid recommended) when data
  exists, and otherwise run as labeled stress-scenario *assumptions* — never as Bitfinex facts. Fee ≠
  slippage, and `position_tracker.py` already keeps them separate (not a gap).
- Recorded the current reality: no `book` channel exists (`ws_public.py` is ticker-only), so the engine
  always runs the stress branch via `cost_stress_sweep.py` with a flat candle-close slippage proxy. The
  order-book VWAP slice is scoped but deferred behind the champion freeze (ends 2026-12-31, Issue #12);
  no trading-claim until the edge survives fee + slippage sensitivity.

## [2026-06-18] update | wiki-lint semantic slice + agent-substrate docs

- Mechanized the fidelity-review's largest gap: `research_wiki_lint.py` now runs `run_semantic_checks()`
  — `orphan_pages` (pages reachable from nowhere) and `broken_links` — on a warn-only `semantic_ok`,
  decoupled from `referential_ok`/`ok` so a false positive can never flip the structural gate. Added a
  positive and negative test in `tests/runtime/test_local_research_wiki_lint_script.py`. Live repo: clean
  (no orphans, no broken links).
- **Scope decision (diverged from the approved plan, deliberately):** the plan scoped broken-link
  detection to backtick `.md` refs across all pages. Running it live showed that is all prose-noise —
  external citations (NVIDIA clone paths), historical chronology, and a `<date>` placeholder. The wiki's
  backtick navigation is load-bearing *only* in the registries, which the referential check already
  validates. So broken-link detection now targets markdown `[text](target.md)` link syntax (the actual
  link convention); orphan reachability stays broad (any backtick OR markdown mention counts). Opposite
  directions, both "stay green unless real."
- Hardened the agent substrate (freeze-safe docs, no `src/` logic / config / champion touch): added
  `docs/glossary.md` (repo terms → SSOT links, not restated), `mcp_server/index.md` (verification-only
  MCP boundary), and rolled the `index.md` convention out to `src/core/backtest/`, `indicators/`, and
  `intelligence/`. Marked the fidelity review's semantic-lint next-step done.

## [2026-06-18] ingest | Bitfinex zero-fee change folded into slippage methodology

- External fact verified across sources: Bitfinex scrapped the maker/taker model effective **2025-12-17**
  — zero maker and taker fees, permanent, no volume/tier/LEO condition, across spot/margin/derivatives/
  securities/OTC. Funding/margin-lending and deposit/withdrawal fees are unchanged.
- Folded into `slippage-backtest-methodology.md`: `commission: 0.0` is now documented exchange reality for
  spot (not an assumption); the `position_tracker.py` `commission_rate=0.002` default is now historical
  (harmless, config overrides to 0.0); funding/margin-lending recorded as the separate remaining exchange
  cost (applies to margin/leverage only — tracked champions are spot `tBTCUSD`).
- Consequence recorded: with the spot fee axis at ~0, slippage now carries essentially all executable
  cost — vindicating fee ≠ slippage and raising the relative priority of the deferred order-book VWAP
  slice. Docs-only; no runtime/config/champion change.

## [2026-06-18] update | slippage methodology: official fee wording + VWAP slice prep

- **Wording correction (supersedes the "permanent" framing above).** Verified against Bitfinex's own
  sources (`bitfinex.com/zero-fee-trading`, `blog.bitfinex.com` zero-fees Q&A): they call it *"the new
  standard"*, *"not a short term promotion"*, with *"no fixed end date"* — and reserve the right to alter
  fees later with notice. The page now says **current documented Bitfinex standard / no fixed end date**,
  not "permanent". `commission: 0.0` framed as the *correct current baseline* for spot, not a convenience.
- **Funding verified, not assumed.** Confirmed the tracked champions (`tBTCUSD_1h/3h.json`) are spot RI
  configs with fraction-of-capital sizing and no leverage/margin/funding parameters, and `position_tracker.py`
  models no funding/borrow cost — so funding does not apply to them as configured today (would apply under
  real funding exposure).
- **Cost-stress reframed:** commission axis = fee-return / robustness probe (realistic baseline is the zero
  column); slippage axis stays a realistic conservative proxy until order-book depth is modeled.
- **Added an "Implication" section:** zero fees ≠ zero execution cost; the burden shifts onto spread,
  order-book depth, order-size-aware VWAP slippage, and latency/adverse selection as separate stresses.
- **Prepared the deferred VWAP slice (docs-only, still not built):** a pure deterministic
  `orderbook_vwap_bps()` helper, fixtures first — inputs `side/order_size/bids/asks/reference_price`,
  outputs `vwap/filled_size/slippage_bps/spread_bps/depth_exhausted`, no live transport / depth-pipeline /
  engine wiring / champion use before a validation gate. Docs-only; no runtime/config/champion/strategy/
  transport change.

## [2026-06-18] question | edge / mechanism map review (under unresolved VWAP)

- Filed `queries/2026-06-18-edge-mechanism-map-review.md`: a non-authoritative map of the two registered
  mechanisms (`ml_confidence_v1`, `regime_intelligence_v1`) and the two committed champions
  (`tBTCUSD_1h/3h`) under the rule that current results = mechanism mapping + fee-adjusted baseline +
  slippage-stress proxy, NOT order-book-VWAP-adjusted and NOT execution-final.
- Result: **both champions and both mechanisms = `UNRESOLVED`; `EDGE_MAP = UNRESOLVED`.** The only real
  OOS number is negative (`candidate_search_tBTCUSD_1h`: Sharpe −0.22, PF 0.53, best candidate fails
  pf<1.0); the in-sample edge (PF 1.24/1.585) is contingent on the `stale_threshold_factor=1e9` bug bypass
  (0 trades without it) and comes from a deleted, unreproduced branch; Optuna/parity artifacts are test
  fixtures (`dummy.json`, synthetic `tTESTBTC`). 1h is *closest to REJECTED* but held at UNRESOLVED because
  falsification needs a reproduced run (out of scope). Neither mechanism has a counterparty/persistence story.
- VWAP is necessary-but-not-sufficient: neither result is *blocked* by VWAP (1h fails on negative OOS; 3h on
  Sharpe<1.0 at zero cost). Next step = a falsifiable OOS reproduction without the bypass (needs-experiment,
  post-freeze / Issue #12). Docs-first; no runtime/strategy/champion/optimizer/transport change.

## [2026-06-18] audit | infrastructure-fitness audit (pre clean-slate candidate lane)

- Filed `infrastructure-fitness-audit.md` (topic page): an evidence-backed fitness map of V2 infra across 8
  areas, classifying each component KEEP / KEEP_WITH_GUARDS / REPLACE / DEPRECATE / DELETE_CANDIDATE /
  QUARANTINE_LEGACY / BASELINE_ONLY / UNKNOWN_NEEDS_EVIDENCE. Principle: *Reuse is not preservation* +
  *Research should be easy, authority should be hard* — a fitness audit, not a policing audit.
- Headline (own-verified, not just Explore sweeps): **no live V1 imports** anywhere. `find_new_champion_candidate.py`
  is candidate-generation-adjacent research that writes only to `results/evaluation/`, mutates no authority,
  reads seed read-only — but builds packets with **forced** `promotion_override/signoff` flags → *authority
  risk if reused without guards* (not a violation). Five research tools/scripts (`find_new_champion_candidate`,
  `build_candidate_packet`, `cost_stress_sweep`, `reconcile_forward_backtest`, `qwen_builder`) are
  **unregistered research paths** (absent from `seed_manifest.json`); `openai`+`optuna` sit in main deps.
- DELETE_CANDIDATE: test fixtures committed under `results/hparam_search/**` + a synthetic-symbol parity
  artifact (flag for a separate removal PR, not deleted now). DEPRECATE: legacy backtest exit-engine family
  (mid-migration), `agent-ecosystem-inventory.md` (superseded). KEEP: REST read spine, backtest core,
  strategy/governance spine, wiki substrate.
- Pre-clean-slate must-resolve: a research↔authority boundary contract; the candidate-script boundaries
  (needs governance decision); the `evaluate.py` staleness bug; exit-engine consolidation; funding-cost
  handling. Docs-first, audit-only; no code/dep/champion/results change. Page is non-authoritative.

## [2026-06-18] change | remove obsolete qwen/glm/nvidia LLM-builder surface

- Removed the `genesis-v2-qwen-builder` console tool and its entire surface as **obsolete**: deleted
  `src/genesis_core_v2_cli/qwen_builder.py`, `scripts/ai/qwen_builder.py`, and
  `tests/runtime/test_local_qwen_builder_script.py`; dropped the `genesis-v2-qwen-builder` console script
  and the `qwen_builder_main` shim from `pyproject.toml` + `console_scripts.py`; pruned the qwen/NVIDIA
  assertions from the console-script and env-template tests.
- Dropped the now-orphaned `openai` dependency (qwen_builder was its only consumer; flagged
  quarantine-only in the external-pattern scan) and regenerated `uv.lock` (also removed transitive
  `distro`/`jiter`/`sniffio`). Cleared the `LLM_API_KEY`/`GLM_API_KEY`/`NVIDIA_*` block from `.env.example`
  and local `.env`; refreshed the three affected `seed_manifest.json` file hashes.
- Supersedes the `qwen_builder.py` row in `infrastructure-fitness-audit.md` (was KEEP_WITH_GUARDS → now
  removed). No runtime/strategy/champion/optimizer/transport behavior changed; clean-slate cleanup only.

## [2026-06-18] governance | research↔authority boundary sync (ADR 0001/0002 Accepted, ADR 0003)

- Filed `docs/adr/0003-research-tooling-non-authoritative.md`: makes the research↔authority boundary a
  durable decision. It covers the research/evidence-only paths (`find_new_champion_candidate.py`,
  `cost_stress_sweep.py`, `tools/reconcile_forward_backtest.py`, and the trace/packets substrate) that may
  *propose* but never *approve*, plus the boundary-spanning decision-packet CLI (`build_candidate_packet.py`)
  whose default output is non-authoritative and whose approval mode requires the explicit human override +
  signoff authority path. Records the Phase 1 guard (PR #54) as the enforcement.
- Moved ADR 0001 (absorption tiers) and ADR 0002 (run-trace/packet contract) from Proposed → **Accepted**:
  0002's contract is implemented (`core/packets`, `core/trace`) and validated by green governance tests;
  0001's tiers are in active use (0002 instantiated the first "Absorbera NU" item; the LLM-quarantine tier
  is realized by the candidate-search guard).
- Docs-only governance sync. No code/config/champion/runtime/seed_manifest change. The AGENTS/copilot/
  SKELETON_SCOPE pointers and manifest registration of these research paths are deferred to the next slice
  (those docs are manifest-hashed; their hashes are refreshed there).
