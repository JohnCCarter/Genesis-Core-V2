# Research wiki recovery

> **Boundary note:** this is a short baton-pass note for a future session.
> It preserves continuity, but it does not replace topic pages, logs, or authority surfaces.

Date: 2026-06-08
Working branch: `main`
Knowledge product links: `../index.md` → `../map.md` → `../log.md`

## Why this handoff exists

A previously implemented Karpathy-style LLM wiki slice appeared to have been lost during earlier
bounded merge work. This handoff records what was recovered so future sessions do not need to redo
forensic recovery from transcripts, PR metadata, and unreachable commits.

## What changed

- restored `docs/agent-ecosystem-inventory.md` from historical PR #2 content
- restored the repo-tracked research knowledge product under `docs/research/**`
- restored `scripts/audit/research_wiki_lint.py`
- restored `tests/runtime/test_local_research_wiki_lint_script.py`
- removed temporary forensic recovery artifacts after the durable repo files were back in place

## Current understanding or hypothesis

The repo-native research wiki is back as a tracked, derivative, non-authoritative knowledge surface.
The strongest recoverable evidence came from:

- closed PR #2 for `docs/agent-ecosystem-inventory.md`
- local unreachable commit `990df51f88c9aaa9ba5f53c0b62eef5abf2335e5` for the broader `docs/research/**`
  slice and its supporting lint/test surfaces

The recovered wiki should now be treated as the durable Markdown knowledge layer for bounded V2
research, while runtime, promotion, and authority claims remain in their existing authority-bearing
surfaces.

## Next steps

1. Keep repo-level docs aligned so `README.md` and `docs/SKELETON_SCOPE.md` no longer imply that the
   restored research wiki is excluded.
2. If more lost documentation is suspected later, start from the restored wiki/log surfaces before
   doing new transcript archaeology.
3. If the recovered wiki becomes load-bearing in new areas, promote those specific conclusions into
   admitted authority or verification surfaces separately.

## Blockers or open questions

- Some recovered research wiki pages still contain minor encoding artifacts from the historical
  extraction path and may deserve a future cleanup slice.
- It is still possible that other non-admitted historical docs existed on broad branches, but the
  bounded research wiki and agent ecosystem inventory are now back in repo-tracked form.
