# Research wiki handoff

> **Boundary note:** the single, rolling baton-pass for the next session — overwritten each milestone.
> `patterns.md` Pattern 3 owns the minimum-handoff contract; `log.md` owns the append-only history.

Date: 2026-06-18
Working branch: none (paused on `main`)
Knowledge product links: `index.md` · `map.md` · `log.md`

## Why this handoff exists

Pausing for the day after completing the clean-slate research↔authority sequence (Phase 1–4). The next
session — likely from the home computer — should resume the **Absorb-NOW hardening track** without
reconstructing this chat.

## 1. Current repo status

- `main` at `85e4ef9`; working tree clean; **no active feature branch**.
- CI green through **#57**.
- Phase 1–4 complete and merged. The research↔authority boundary is now **enforced → formalized →
  registered → designed**.

## 2. What changed today (Phase 1–4)

- **Phase 1 (#54)** — candidate-search artifacts are non-authoritative: `find_new_champion_candidate.py`
  forced promotion flags → `False`, output stamped `research_only`, the `--trace` gate de-authorized;
  `tests/governance/test_candidate_search_artifact_guard.py` added.
- **Phase 2 (#55)** — ADR 0003 (research may propose, not approve); ADR 0001/0002 moved → **Accepted**.
- **Phase 3 (#56)** — `seed_manifest.json` `research_tooling_surfaces` registration (visibility, not
  authority); ADR 0003 pointers in `AGENTS.md` / `.github/copilot-instructions.md` /
  `docs/SKELETON_SCOPE.md`; four manifest `output_hashes` refreshed; registration test added.
- **Phase 4 (#57)** — `docs/research/clean-slate-candidate-factory.md` design (mechanism-first lane,
  "reuse the platform, reset the candidate") — **design only, not built**.

## 3. Next track — Absorb-NOW hardening

**Purpose:** implement the open Absorb-NOW points (from `external-pattern-scan-report.md` / ADR 0001)
**before** building the clean-slate runner/model — infrastructure hardening first.

Points to implement:

- mutation testing / mutation-style hardening of the decision kernel
- property/metamorphic tests for `compare_families`
- property/metamorphic tests for `run_premortem`
- OOS leakage hardening
- framework-inversion guard

The clean-slate **candidate prereg-template** (Phase 4 §8a) remains the first clean-slate *lane* artifact,
but Absorb-NOW hardening may go first as infrastructure. **Do not start the prereg-template yet if
Absorb-NOW is prioritized.**

## 4. Home computer resume checklist

```
git checkout main
git pull --ff-only
git log -1 --oneline      # expect 85e4ef9 (or newer)
git status --short        # expect clean
```

Gitignored local state — recreate it; do not expect it in git:

- **`.venv/`** — recreate with the canonical sync: `uv sync --extra dev --extra mcp` (`uv.lock` is
  committed → reproducible). This installs all deps incl. `pandera`/`hypothesis` (a stale local env was
  the only past collection failure).
- **`.env`** — gitignored, machine-local; copy from `.env.example` if needed. **Not required for the
  Absorb-NOW track** (offline tests; no credentials/transport).
- Caches/generated artifacts (`__pycache__`, `.hypothesis`, `results/`, `results/trace/`, `cache/`,
  `data/`, `logs/`) are all gitignored and regenerated — none are needed to resume.

Minimal verification (set `PYTHONDONTWRITEBYTECODE=1` to avoid pycache churn):

```
uv run python scripts/audit/research_wiki_lint.py   # expect ok / referential_ok / semantic_ok = true
uv run pytest -q tests/governance                   # governance + seed-boundary + guard tests
uv run pytest -q                                     # full suite (repo-bounds parity with CI)
```

## 5. Implementation guidance — Absorb-NOW

**Do not create a branch until the next work package is clear.** First step next session: a **read-only
reconnaissance** of the decision kernel + existing test patterns, then **propose a PR breakdown** for review.

Likely breakdown (verify repo structure first — do not finalize before recon):

- **PR A** — decision-kernel mutation-style hardening
- **PR B** — property/metamorphic tests for `compare_families` + `run_premortem`
- **PR C** — OOS leakage hardening
- **PR D** — framework-inversion guard

Rules:

- one PR = one concern
- no runtime / champion / config mutation
- no candidate/model implementation
- no Optuna / tuning / backtest result mining
- no new dependency unless justified and approved
- reuse existing repo test patterns before adding frameworks (Hypothesis is already used in
  `tests/utils/diffing/test_results_diff.py` — precedent, no new dep needed for property tests)
- research should be easy; authority should be hard

Recon anchors:

- kernel: `src/core/decision/{comparison.py,premortem.py,promotion.py,candidate_builder.py,models.py}`
- existing tests: `tests/test_premortem_system.py`, `tests/backtest/test_compare_backtest_results.py`,
  `tests/utils/diffing/test_results_diff.py`
- sources: `external-pattern-scan-report.md` (Absorb-NOW list) + `docs/adr/0001-absorption-tiers-solo-agents.md`

## Current understanding or hypothesis

The research↔authority boundary is structurally closed (enforce → formalize → register → design). The
next risk to retire is **evidence trustworthiness in the decision kernel** — mutation/property tests +
OOS-leakage hardening — so a future clean-slate candidate rests on a *verified* kernel, not an assumed one.

## Blockers or open questions

- Champion freeze active until **2026-12-31** — no champion/config changes.
- `infrastructure-fitness-audit.md` "unregistered research paths" wording is **stale** after Phase 3 (the
  paths are now registered in `research_tooling_surfaces`) — intentionally not updated; fix in a future
  docs slice if desired.
- The clean-slate edge is `EDGE_MAP=UNRESOLVED`; the in-sample edge depends on the evaluate-staleness
  bypass (`stale_threshold_factor=1e9`). The `evaluate.py` ns-vs-ms staleness fix is post-freeze and out of
  the Absorb-NOW scope, but it is a known dependency for any real OOS evidence later.
