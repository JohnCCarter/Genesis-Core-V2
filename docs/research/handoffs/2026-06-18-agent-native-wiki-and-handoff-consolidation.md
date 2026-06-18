# 2026-06-18 agent-native wiki lint + handoff consolidation

> **Boundary note:** this is a short baton-pass note for a future session.
> It preserves continuity, but it does not replace topic pages, logs, or authority surfaces.

Date: 2026-06-18
Working branch: `feature/research-candidate`
Knowledge product links: `../index.md` · `../map.md` · `../log.md`

## Why this handoff exists

A session that started as a review of a colleague's Karpathy-wiki branch turned into two shipped
milestones plus a sharpened operating principle. This note is the durable baton-pass so the next
session resumes without re-deriving the decisions.

## What changed

- **Reviewed** `origin/claude/karpathy-llm-wiki-obsidian-refanw` (the fidelity-review branch). Verified
  faithful to Karpathy's gist (11/11 claims) and to the repo; one minor loose number ("nearly all pages
  06-04/06-08" is really 4/6). **Not merged yet.**
- **Commit `b304f8c` — agent-native lint + framing:** added a referential-integrity check to
  `scripts/audit/research_wiki_lint.py` (unregistered dated pages + dangling registry references,
  warn-only, does not flip structural `ok`); positive + negative tests. It caught real rot — a stale
  "Companion agent workflow" section in `map.md` and `index.md` pointing at a skill that never existed;
  removed from both. Sharpened the agent-native framing in `patterns.md` (Pattern 7), `map.md`,
  `operations.md`.
- **Commit `99c8f96` — handoff consolidation:** `CLAUDE.md` now routes milestone handoffs to
  `docs/research/handoffs/` (was `.claude/handoffs/`, machine-local); removed the duplicate local copy;
  gitignored `.claude/` scratch.

## Current understanding or hypothesis

The research wiki is an **agent-native tool**: faithful to Karpathy in form, deliberately divergent in
motor. Role split is sharper than Karpathy — the agent curates sources, writes, and reads; the human
only asks questions. Its job is millisecond orientation (restore context from the wiki, don't re-scan
the repo). Three knobs turned toward Karpathy (ownership, ergonomics, bookkeeping); authority is held —
load-bearing conclusions still promote out. The lint mechanizes referential integrity only;
contradiction/staleness detection stays agent judgment.

## Next steps

1. **Merge the fidelity-review branch.** Expect a trivial `map.md` conflict: this session removed the
   "Companion agent workflow" section; that branch adds a `queries/2026-06-17-karpathy-wiki-fidelity-review.md`
   row. After merge, `patterns.md` could point Background at that fidelity page (currently points at the
   2026-06-04 page to avoid a dangling ref).
2. Optional: mechanize a semantic-lint slice later (contradictions/staleness) — flagged as fuzzy phase 2,
   not blocking.

## Blockers or open questions

- Champion freeze active until 2026-12-31 — no champion config changes.
- Durable handoffs must now be registered in `handoffs/index.md` or the referential lint goes red — new
  discipline introduced this session, by design.
- Pre-existing env gap (not this work): `tests/runtime/test_local_fetch_historical_script.py` fails to
  collect on `ModuleNotFoundError: pandera` — missing dev dependency locally.
