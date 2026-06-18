# Infrastructure fitness audit (pre clean-slate candidate lane)

> **Boundary note:** this is a derivative, **non-authoritative** research page. It maps the fitness of
> existing V2 infrastructure for reuse in a future clean-slate candidate lane. It issues no runtime,
> promotion, or removal authority — every label is a recommendation, not an action. Nothing here deletes,
> refactors, or changes code.

Status: active
Opened: 2026-06-18
Working branch: `feature/research-infrastructure-audit`
Knowledge product links: `index.md` · `map.md` · `log.md`

## Guiding principles

- **Reuse is not preservation. Clean slate requires cleanup.** Existing infra is not reused by default
  just because it exists; each piece earns reuse on evidence.
- **Research should be easy. Authority should be hard.** This is a *fitness* audit, not a *policing*
  audit. Research may freely search, test, and write artifacts. The boundary we protect is the one where
  research output silently becomes candidate / champion / promotion authority. Where a repo contract is
  unclear, this page says **needs governance decision** — never "violation".

## 1. Executive summary

V2 infrastructure is overwhelmingly **V2-native** — no live Genesis-V1 imports were found; every "v1"/
"legacy" marker is an internal version label or an explicitly guarded test-only surface. The core
backtest / strategy / governance spine is clean, tested, and reusable. The real fitness gaps are not
contamination but **boundary clarity**: several genuinely useful research/candidate-generation tools were
added after the seed was generated and are **unregistered research paths** (absent from
`seed_manifest.json` and the governance docs). They are not wrong — they just lack the guards that keep
their output from being mistaken for authority. The other recurring themes are **test fixtures committed
into `results/`** (cleanup, not danger), a **dual exit-engine migration** mid-flight, and a known
**staleness bug** in `evaluate.py` that distorts cost-stress honesty. None of this blocks a clean-slate
lane; it defines the guards that lane must carry.

## 2. Scope and non-goals

Docs-first, audit-only. **No** deletion, refactor, replacement, dependency change, model/candidate
implementation, optimizer/tuning, or any change to runtime / config / champion / strategy / transport /
VWAP / depth / backtest-engine / tests / `results/`. Everything that should change later is flagged as a
recommendation + a proposed future PR. "Fix while scanning" is out of scope. Only files written by this
track: this page + `map.md` + `log.md`.

## 3. Consulted files / areas

Eight areas: (1) Data/IO, (2) Backtest infra, (3) Eval/research tooling, (4) Strategy/candidate surfaces,
(5) Optimizer/hparam artifacts, (6) Governance/authority, (7) Agent/research-wiki infra, (8) Overlap/
duplication. Evidence base: three parallel read-only Explore sweeps (callers, tests, grep, artifacts) plus
**own verification** of every headline finding below — `find_new_champion_candidate.py` read in full;
`seed_manifest.json`, `pyproject.toml`, `tests/**`, and `src/**` imports searched directly. Methods notes:
labels are adjudicated here (not copied from the sweeps); claims of "unused"/"safe" require a repo search /
tests / callers, else `UNKNOWN_NEEDS_EVIDENCE`.

## 4. Infrastructure inventory

Detailed per-component reasoning lives in the per-label sections (5–12). Confidence: H = own-verified or
test/caller-backed, M = sweep evidence with file refs, L = partial/inferred.

| Component | Area | Origin | Use evidence | Tests | Label | Action type | Conf |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `io/bitfinex/exchange_client.py` | IO | V2 | server + all IO callers | yes | KEEP | none | H |
| `io/bitfinex/read_helpers.py` | IO | V2 | account API | yes | KEEP | none | H |
| `io/bitfinex/historical_candles.py` | IO | V2 | fetch script | partial | KEEP_WITH_GUARDS | test PR | M |
| dormant transport (`ws_public/ws_auth/ws_reconnect/rest_auth`) | IO | V2 | no prod callers; admitted dormant (Batch H2) | import-only | KEEP_WITH_GUARDS | code PR (future) | H |
| `io/bitfinex/rest_public.py` | IO | V2 | test-only, 1 fn | yes | BASELINE_ONLY | none | M |
| `symbols/symbols.py` (`SymbolMapper`) | IO | V2 | active; hardcoded map | partial | KEEP_WITH_GUARDS | code PR (future) | M |
| `utils/__init__.py` data-path helpers | IO | V2 | active; legacy fallback path | partial | KEEP_WITH_GUARDS | docs/test | M |
| `frozen_first` / `data_source_policy` | IO | V2 | engine load path | none direct | KEEP_WITH_GUARDS | test PR | M |
| `features_asof*` (as-of + precompute remap) | IO/BT | V2 | engine | partial | KEEP_WITH_GUARDS | test PR | M |
| HTF 1D as-of alignment | IO/BT | V2 | engine | unread | UNKNOWN_NEEDS_EVIDENCE | needs evidence | L |
| `backtest/engine.py` (`BacktestEngine`) | BT | V2 | pipeline + scripts | yes | KEEP | none (resolve dual-engine) | H |
| `backtest/engine_precompute.py` | BT | V2 | engine only | none direct | KEEP_WITH_GUARDS | test PR | M |
| `backtest/engine_results.py` | BT | V2 | engine | indirect | KEEP | none | M |
| `backtest/position_tracker.py` | BT | V2 | engine | partial | KEEP_WITH_GUARDS | docs + test | H |
| `backtest/metrics.py` | BT | V2 | optimizer scoring | none direct | KEEP_WITH_GUARDS | docs/test | M |
| `backtest/trade_logger.py` | BT | V2 | scripts | none | KEEP | none | M |
| legacy exit engine + `htf_exit_*`, `exit_strategies.py` | BT | V2 | engine fallback | tripwire only | DEPRECATE | code PR (future) | M |
| `strategy/htf_exit_engine.py` (new) | BT | V2 | engine (preferred) | tripwire only | KEEP_WITH_GUARDS | test PR | M |
| `strategy/champion_loader.py` | STRAT | V2 | all exec paths | yes | KEEP | none | H |
| `config/strategy/champions/tBTCUSD_1h/3h.json` | STRAT | V2 | runtime seed | indirect | KEEP_WITH_GUARDS | docs | H |
| `strategy/family_registry.py` | STRAT | V2 | 17 callers | yes | KEEP | none | H |
| `strategy/family_admission.py` | STRAT | V2 | governance guard | yes | KEEP | none | H |
| `strategy/run_intent.py` | STRAT | V2 | pipeline-wide | yes | KEEP | none | H |
| `strategy/evaluate.py` | STRAT | V2 (+legacy regime call) | runtime authority | yes | KEEP_WITH_GUARDS | code PR (post-freeze) | H |
| `strategy/mechanism_registry.py` + `MECHANISMS.md` | STRAT | V2 | research record | yes | KEEP | none | H |
| `detect_authoritative_regime_legacy` (regime authority) | STRAT | unclear | live call in evaluate | partial | UNKNOWN_NEEDS_EVIDENCE | needs evidence | L |
| `optimizer/**` (12 modules) | OPT | V2 | import/test-only; dormant (Batch I1) | yes | KEEP_WITH_GUARDS | docs | H |
| `config/optimizer/**` legacy-family YAML | OPT | V2 (pre-RI-cutover) | research corpus | n/a | QUARANTINE_LEGACY | docs | M |
| `optuna` dependency | OPT | dep | optimizer + tests | via tests | KEEP_WITH_GUARDS | docs | H |
| `results/hparam_search/{run_optuna*,run_test,run_validate*,test_narrow}` | OPT | test fixtures | none | n/a | DELETE_CANDIDATE | removal PR | H |
| `results/evaluation/ri_p1_off_parity_v1_*.json` | OPT | synthetic (`tTESTBTC`) | none | n/a | DELETE_CANDIDATE | removal PR | H |
| `results/evaluation/candidate_search/**` | EVAL | real, point-in-time | research evidence | n/a | BASELINE_ONLY | none | H |
| `scripts/analyze/cost_stress_sweep.py` | EVAL | V2 | wiki-referenced instrument | none direct | KEEP_WITH_GUARDS | register + test | H |
| `tools/reconcile_forward_backtest.py` | EVAL | V2 | tested; no live data yet | yes | KEEP_WITH_GUARDS | register | H |
| `tools/compare_backtest_results.py` | EVAL | V2 | admitted; tested | yes | KEEP | none | H |
| `scripts/audit/find_new_champion_candidate.py` | EVAL | V2 | candidate-generation adjacent | none direct | KEEP_WITH_GUARDS | needs governance decision | H |
| `scripts/audit/build_candidate_packet.py` | EVAL | V2 | core builder tested | indirect | KEEP_WITH_GUARDS | register + test | M |
| `scripts/ai/qwen_builder.py` + `openai` dep | TOOL | V2 | tested; console-locked | yes | KEEP_WITH_GUARDS | docs + dep PR | H |
| `governance_mode.md` / freeze-guard / family+config authority | GOV | V2 (config V1-derived) | CI + tests | yes | KEEP | none | H |
| `seed_manifest.json` | GOV | V2 | 57+ assertions | yes | KEEP_WITH_GUARDS | docs (mode field) | H |
| `config/authority.py` (`ConfigAuthority`) | GOV | V1-derived (admitted) | config API | yes | KEEP_WITH_GUARDS | REPLACE whitelist (future) | M |
| `config/validator.py` legacy schema | GOV | V2 (legacy/test-only) | test-only; tripwire-guarded | yes | QUARANTINE_LEGACY | docs | M |
| governance docs (`AGENTS.md`/`copilot-instructions.md`/`SKELETON_SCOPE.md`) | GOV | V2 | drift vs repo | text-asserted | KEEP_WITH_GUARDS | docs sync PR | H |
| research wiki (`map/index/log/queries/templates/patterns/operations`) | WIKI | V2 | active | lint | KEEP | none | H |
| `scripts/audit/research_wiki_lint.py` | WIKI | V2 | local audit | yes | KEEP_WITH_GUARDS | CI-wire (future) | H |
| `trace/**` + `packets/**` (ADR 0001/0002) | WIKI | V2 | opt-in emitters; tested | yes | KEEP_WITH_GUARDS | manifest + ADR status | H |
| subsystem `index.md` + `glossary.md` | WIKI | V2 | guidance | n/a | KEEP | none | H |
| `docs/agent-ecosystem-inventory.md` | WIKI | V2 | superseded; stale branch ref | none | DEPRECATE | mark superseded | M |
| `external-pattern-scan-report.md` | WIKI | V2 | ADR-referenced | none | KEEP | relocate (future) | M |

## 5. KEEP

Clean, active, V2-native, tested, reusable as-is for the clean-slate lane:

- **REST read spine** — `io/bitfinex/exchange_client.py` (SSOT for signing/public), `read_helpers.py`.
- **Backtest core** — `backtest/engine.py` (central; resolve the dual exit-engine duality eventually but
  it is not a blocker), `engine_results.py`, `trade_logger.py`.
- **Strategy governance spine** — `champion_loader.py`, `family_registry.py`, `family_admission.py`,
  `run_intent.py`, `mechanism_registry.py` (+ `docs/strategies/MECHANISMS.md`; consistent and tested).
- **Governance SSOT** — `docs/governance_mode.md`, `champion-freeze-guard.yml`, `authority_mode_resolver.py`,
  and the governance test suite (`test_v2_seed_boundaries.py`, `test_no_legacy_feature_imports.py`,
  `test_dead_code_tripwires.py`, `test_pipeline_fast_hash_guard.py`).
- **Result-comparison gate** — `tools/compare_backtest_results.py` (admitted, tested).
- **Agent/wiki substrate** — research wiki surfaces, subsystem `index.md`, `docs/glossary.md`.

## 6. KEEP_WITH_GUARDS

Useful but reuse needs explicit guards / scope / anti-leakage. The dominant theme is *unregistered
research paths* and *output that could be misread as authority*.

- **`find_new_champion_candidate.py`** — the boundary case, examined closely. Verified: it is
  candidate-generation-adjacent research infra. It **writes only** to `results/evaluation/candidate_search/`
  (+ opt-in trace), **mutates no authority surface** (never touches `champions/` or `runtime.json`), reads
  `runtime.seed.json` **read-only** as a baseline with `skip_champion_merge=True`, and has **no V1 import**.
  The genuine guard gap: its candidate packet is built with **hardcoded** `promotion_override_flag=True,
  promotion_signoff_flag=True`, so the artifact's `ready_for_promotion` reflects *forced* flags, not real
  signoff — an **authority risk if reused without guards** (a reader could mistake the artifact for a
  promotion green-light). It is also an **unregistered research path** (absent from `seed_manifest.json`,
  no direct test) and uses `optimizer.scoring` (Batch I1 dormant surface). Recommended guards: stamp the
  artifact non-authoritative; stop forcing promotion flags (or rename them in the artifact); register +
  test the path. Whether calling `optimizer.scoring` from a research script sits inside Batch I1's
  import/test admission is a **needs governance decision**, not a violation. *Research may search — we just
  keep its output from silently becoming authority.*
- **`cost_stress_sweep.py`** — the wiki's primary cost instrument; active and depended-on, but an
  unregistered research path with no direct test and a known staleness bypass (`stale_threshold_factor=1e9`).
  Guards: register in the manifest as a research script; add a smoke test; carry the staleness caveat.
- **`tools/reconcile_forward_backtest.py`** — well-tested Phase-3 reconciliation tool, but unregistered in
  the manifest and not yet fed real forward data. Guard: register; mark "ready, awaiting forward rows".
- **`build_candidate_packet.py`** — its core (`core.decision.candidate_builder`) is tested; the script
  wrapper is unregistered/untested. Guard: register + wrapper test.
- **`qwen_builder.py` + `openai` dependency** — tested, console-script-locked, never writes authority.
  But `openai>=2.43.0` is a **main** `[project.dependencies]` entry (not an optional extra) for a
  non-deterministic research helper that the governance docs do not mention. Guards: move to an optional
  `ai` extra; document the LLM-output-is-proposal-evidence quarantine.
- **`seed_manifest.json`** — essential machine contract; its top-level `mode: "RESEARCH"` is a
  generation-time label, not a live mode signal. Guard: note/test that live mode resolves via
  `governance_mode.md`.
- **`config/authority.py` (`ConfigAuthority`)** — V1-derived, admitted; its ~440-line hand-coded
  `propose_update` whitelist is a correctness/maintenance risk (see REPLACE).
- **Governance docs** — `AGENTS.md` / `copilot-instructions.md` / `SKELETON_SCOPE.md` predate the
  trace/packets foundation, `qwen_builder`, and the analysis/audit scripts. Guard: one synchronized
  docs-only pass to describe these as admitted research paths and their boundaries.
- **Dormant Bitfinex transport family** (`ws_public/ws_auth/ws_reconnect/rest_auth`) — admitted dormant
  (Batch H2), zero prod callers (own-verified). Guard already exists (`test_v2_seed_boundaries` asserts
  absence from server); flag nonce-logic drift (`ws_reconnect` vs `NonceManager`) to reconcile before any
  future validated rebind. **Must not rebind without a separate validated slice.**
- **`trace/**` + `packets/**`** — clean, tested, fail-open, authority-separated; ADRs are "Proposed" and
  the addition is not yet in `seed_manifest.json`. Guard: admit to manifest; move ADR status to Accepted.
- **Backtest accounting honesty** — `position_tracker.py` (no funding cost; flat symmetric slippage proxy;
  `commission_rate` default mismatch 0.2% vs engine 0.1%), `metrics.py` (non-standard per-trade Sharpe /
  drawdown). Guards: document limitations; add unit tests before any head-to-head candidate comparison.
- **Data load integrity** — `historical_candles.py` (pandera on write but no schema check on read in
  `engine.load_data()`), `frozen_first` policy (no end-to-end test), `features_asof` precompute remap
  (complex; a regression could reintroduce lookahead). Guards: read-side column check; policy test; an
  as-of/`pre_idx` lookahead regression test.
- **`SymbolMapper`** (hardcoded `DEFAULT_MAP` requires code change per new symbol), `optimizer/**`
  (correctly dormant; `trace/recorder.py` imports `run_optimizer` — annotate to prevent accidental
  widening), `optuna` dep (heavy, dormant-only — document as research/test-only), `research_wiki_lint.py`
  (not CI-wired — wiki regressions not auto-caught), `strategy/evaluate.py` (active staleness bug; calls a
  legacy-named regime function — see UNKNOWN).

## 7. REPLACE candidates

- **`ConfigAuthority.propose_update` whitelist** — ~440 lines of hand-coded nested allow-list. A
  declarative JSON-Schema replacement would shrink the surface and remove a silent-misconfig risk. Future
  hardening slice (post-freeze); not urgent, not a blocker.

(No other component had strong enough evidence to recommend replacement over guarded reuse.)

## 8. DEPRECATE candidates

Phase out, but keep temporarily:

- **Legacy backtest exit engine** — `backtest/htf_exit_engine.py` + `htf_exit_partials.py` /
  `htf_exit_structure.py` / `htf_exit_swing_updates.py` / `htf_exit_trailing.py` + `exit_strategies.py`.
  Mid-migration to `strategy/htf_exit_engine.py`; keep as fallback until the new engine is proven
  equivalent, then remove in a dedicated PR.
- **`docs/agent-ecosystem-inventory.md`** — strategic content superseded by `external-pattern-scan-report.md`
  + ADR 0001; references a deleted branch. Mark `superseded` in `map.md` and archive in a later cleanup.

## 9. DELETE_CANDIDATE

Appear to be committed test fixtures / leaked test artifacts. **Do not delete now** — flag for a separate
removal PR after independent confirmation:

- `results/hparam_search/run_optuna/`, `run_optuna_patch_surface/`, `run_test/`, `run_validate_only/`,
  `run_validate_patch_surface/` — fixtures (markers `abc123`, `tTEST`, `dummy.json`).
- `results/hparam_search/test_narrow/` — a pytest run artifact (config_path is a `pytest-of-*` temp dir).
- `results/evaluation/ri_p1_off_parity_v1_ri-20260303-003.json` — synthetic symbol `tTESTBTC:TESTUSD`.

These are cleanup, not danger; the recommended home is `tests/fixtures/` or dynamic generation.

## 10. QUARANTINE_LEGACY

Keep for history / reproduction / baselines; must not be used as authority or template:

- **`config/optimizer/**` legacy-family YAML corpus** — predates the RI-only cutover; admitted as dormant
  research corpus (Batch I1); never an active optimizer input.
- **`config/validator.py` legacy schema** — explicitly legacy/test-only, tripwire-guarded against runtime
  import; retained for the schema-v1 surface only.

## 11. BASELINE_ONLY

Usable as comparison/control, not as the basis for a new candidate:

- **`results/evaluation/candidate_search/**`** — real point-in-time evidence (2026-06-02); the 1h window
  is the negative-OOS control referenced by the edge-mechanism map. Treat as baseline/control, never as
  candidate authority (consistent with `queries/2026-06-18-edge-mechanism-map-review.md`).
- **`io/bitfinex/rest_public.py`** — single public-status function, test-only; infrastructure baseline.

## 12. UNKNOWN_NEEDS_EVIDENCE

Insufficient evidence — do not guess:

- **HTF 1D Fibonacci as-of alignment** (`compute_htf_fibonacci_mapping`) — not fully traced; confirm it
  uses only past 1D closes as-of each LTF bar before trusting HTF-exit results (lookahead risk if wrong).
- **`detect_authoritative_regime_legacy`** — a legacy-named function called live in the RI `evaluate.py`
  path; its scope within RI authority was not traced. Needs a clear read of
  `intelligence/regime/authority.py` before labeling. **Needs clearer research boundary.**
- **`optimizer.scoring` use from `find_new_champion_candidate.py`** — whether this sits inside Batch I1's
  import/test admission or beyond it is a **needs governance decision**, not a missing-evidence item.

## 13. Highest-risk overlaps / obsolete areas

1. **Authority-risk-if-reused (not violation): `find_new_champion_candidate.py` forced promotion flags.**
   The single most important guard for the clean-slate lane — research output must carry a
   non-authoritative marker and must not pre-force override/signoff.
2. **Governance / manifest drift** — the gap between "what the docs/manifest admit" and "what is in the
   repo" (trace/packets, `qwen_builder`+`openai`, the analysis/audit scripts). Low-risk, high-confusion;
   a docs-only sync closes it.
3. **Parallel candidate-review paths** — formal (`compare_backtest_results.py`, admitted/tested) vs
   informal (`build_candidate_packet.py` + `find_new_champion_candidate.py`, unregistered). Not redundant,
   but the informal path is the one needing boundary clarity.
4. **Dual exit-engine** — two HTF exit engines selected by env/config; resolve before the new lane depends
   on exit behavior.
5. **Honesty bug** — `evaluate.py` staleness (ns vs ms → 0 trades without bypass) distorts every
   cost-stress reading; the clean-slate lane should not inherit a bypass-dependent measurement.

## 14. What must be resolved before a clean-slate candidate factory

- A **research↔authority boundary contract**: research may search/score/write artifacts freely; promotion
  authority requires explicit, un-forced signoff. Encode it so candidate-search output cannot be read as
  promotion-ready (fixes finding #1).
- Decide the **boundary of the candidate-generation scripts** (`find_new_champion_candidate.py`,
  `build_candidate_packet.py`): admit as scoped research paths in the manifest + docs, or relocate.
- Fix or quarantine the **staleness bug** so the new lane measures cost honestly (post-freeze; champion-
  adjacent).
- Pick the **exit-engine** of record and retire the other.
- Establish **funding-cost** handling (or an explicit "spot-only, no funding" contract) in the accounting
  layer.

## 15. Proposed next PRs (ordered by risk/ROI)

1. **Docs-only governance sync** (lowest risk, high clarity): describe trace/packets, `qwen_builder`,
   `cost_stress_sweep.py`, `find_new_champion_candidate.py`, `build_candidate_packet.py`,
   `reconcile_forward_backtest.py` as admitted research paths + their boundaries; note `seed_manifest`
   `mode` is generation-time; move ADR 0001/0002 to Accepted. **docs-only.**
2. **Manifest registration** of the unregistered-but-kept research scripts/tools. **docs/config-only.**
3. **Non-authoritative artifact guard** for candidate-search output (stop forcing promotion flags; stamp
   artifacts). **code PR (small, post-review).**
4. **`results/` fixture cleanup** — move the test fixtures out of `results/` to `tests/fixtures/`.
   **removal PR.**
5. **`openai` → optional `ai` extra** + LLM-quarantine doc. **dependency PR.**
6. **Accounting honesty** — staleness-bug fix + funding-cost decision + slippage/funding docs.
   **code PR (post-freeze).**
7. **Exit-engine consolidation** — prove equivalence, retire legacy. **code PR (later).**

## 16. Observed / Inferred / Unverified split

- **Observed (own-verified or test/caller-backed):** no V1 imports; `find_new_champion_candidate.py`
  writes only to `results/evaluation/`, mutates no authority, forces promotion flags; the five tools absent
  from `seed_manifest.json`; `openai` + `optuna` in main deps; no prod importers of the WS family; champions
  are RI spot with `score=0`/`trial_id=null`; results/ fixtures carry test markers.
- **Inferred (reasoned from evidence):** candidate-search artifacts could be misread as authority because of
  the forced flags; governance-doc drift creates confusion risk; the dual exit-engine and staleness bug are
  reuse hazards; `agent-ecosystem-inventory.md` is superseded.
- **Unverified (needs evidence):** HTF 1D as-of alignment; `detect_authoritative_regime_legacy` scope;
  whether `optimizer.scoring` use is inside Batch I1 admission (governance decision); funding-cost materiality
  for current hold horizons.

## 17. Lint result

Recorded at write time in `log.md`; `research_wiki_lint.py` → `ok` / `referential_ok` / `semantic_ok` all
True (this topic page is registered in `map.md`).

## 18. Final verdict

**PASS** — an evidence-backed fitness map produced docs-first, audit-only, with research-friendly framing:
the core spine is reusable; the work before a clean-slate lane is *boundary clarity and guards*, not
demolition. No code, deps, champions, or `results/` were touched; every change-worthy item is a flagged
recommendation, not an action.

## Current status

Open. The map is recorded; the next concrete step is the docs-only governance sync (PR #1 above), not any
build. This page is non-authoritative and should be updated as the clean-slate lane design consumes it.
