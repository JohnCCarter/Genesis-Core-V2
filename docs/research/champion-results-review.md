# Champion results review

> **Boundary note:** this is a derivative research page.
> It compiles current evidence and open questions, but it does not act as runtime or promotion
> authority by itself.

Status: active
Opened: 2026-06-04
Working branch: `feature/champion-results-review`
Knowledge product links: `index.md` ┬À `map.md` ┬À `log.md`

## Purpose

Compile the current V2 understanding of admitted champion payloads, seed fallback behavior, and
artifact-backed evidence so future review work can start from a stable markdown page instead of
reconstructing the same context from chat or raw file scans.

## Review question

How should the current admitted champion payloads be interpreted in V2, what evidence backs them,
and which statements in repo docs still need reconciliation before any stronger authority claim is
made?

## Source surfaces

- `README.md`
- `docs/SKELETON_SCOPE.md`
- `config/runtime.seed.json`
- `config/strategy/champions/tBTCUSD_1h.json`
- `config/strategy/champions/tBTCUSD_3h.json`
- `config/optimizer/3h/phased_v3/PHASED_V3_RESULTS.md`
- `artifacts/diagnostics/v2_gap_audit_2026-06-01.md`

## Current compiled understanding

- V2 is currently framed as RI-first on active family semantics in the repo-level docs.
- The admitted tracked champion subset is limited to `tBTCUSD_1h.json` and `tBTCUSD_3h.json`.
- Both tracked champion payloads keep `strategy_family: "ri"` at top level and inside
  `merged_config`.
- `ChampionLoader` currently fail-closes demoted champion payloads to runtime-seed fallback.
  This is not just a miss-path policy: the current loader implementation treats demoted payloads as
  non-authoritative and returns `None` from `_validate_champion(...)`, which in turn falls back to
  `config/runtime.seed.json`.
- `tBTCUSD_1h.json` currently presents as:
  - `authority_class: demoted_baseline_carried_ri`
  - `optimizer_backed: false`
  - metadata marking it as a demoted historical payload retained from seed-derived context
- `tBTCUSD_3h.json` currently presents as:
  - `authority_class: demoted_artifact_backed_ri`
  - `optimizer_backed: true`
  - metadata linking it to
    `config/optimizer/3h/phased_v3/best_trials/phaseB_v3_best_trial.json`
- The 3h optimizer evidence page records a post-fix Phase B v3 result (`trial_082`) with positive
  score / PF / Sharpe and notes that it reflects corrected RI config-key lookups.
- `artifacts/diagnostics/v2_gap_audit_2026-06-01.md` is now partly historical: it records a
  pre-cutover state where Legacy was active, then documents the user-directed target architecture
  moving V2 toward RI. It should not be treated as current family-authority truth without
  cross-checking newer docs and configs.

## Verified loader behavior

- Source implementation:
  - `src/core/strategy/champion_loader.py`
- Source-backed tests:
  - `tests/runtime/test_stateful_authority_payloads.py`
  - `tests/governance/test_v2_seed_boundaries.py`

Current verified behavior:

- exact load of `tBTCUSD` / `1h` returns `baseline:runtime_seed`
- exact load of `tBTCUSD` / `3h` returns `baseline:runtime_seed`
- missing champion load (for example `tTEST` / `1h`) returns `baseline:runtime_seed`
- demoted payloads are intentionally retained for audit/reference but rejected as runtime
  authority by `_validate_champion(...)`

Practical implication:

- the currently tracked champion subset is repo-tracked and evidence-bearing,
  but under the present loader semantics it is not runtime-active champion authority
- the strongest current runtime truth is therefore still the RI baseline in
  `config/runtime.seed.json`

## Docs reconciliation

- `README.md` and `docs/SKELETON_SCOPE.md` now share one compact current-authority statement:
  - the tracked champion subset is admitted and evidence-bearing
  - it remains demoted for runtime authority
  - current runtime-active champion/default behavior resolves to `config/runtime.seed.json`
    under the loader/test contract

## Tensions to resolve

- The loader/test seam and the repo-level docs are now aligned on the current runtime contract.
- The tracked champion filenames still look more runtime-active than the current demotion/fallback
  semantics actually allow.
- The exact current relationship between:
  - `config/runtime.seed.json` as baseline fallback
  - tracked champion JSON payloads
  - future runtime-active champion authority, if it is ever re-admitted
    still needs one longer-term end-state statement.
- If these champion files are retained mainly as historical/evidence carriers, their review and
  naming should make that obvious to future agents.

## Immediate next checks

1. Decide whether the compact current-authority statement should also be mirrored in
   `seed_manifest.json` or another machine-readable contract surface.
2. Decide whether tracked demoted champion filenames need stronger historical/evidence labeling.
3. Decide whether this page should later split into:
   - authority semantics
   - artifact evidence
   - open review questions

## Durable notes

- Prefer linking to raw source surfaces instead of copying large payload blocks into this page.
- When a new review finding is confirmed, update this page briefly and append a dated line to
  `docs/research/log.md`.
- Keep the page Obsidian-friendly: plain Markdown, stable headings, and narrow topic scope.

## Current status

Open. Initial loader semantics are now reconciled against repo-level docs; longer-term artifact and
authority-shape questions remain.
