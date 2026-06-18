# Research wiki handoff

> **Boundary note:** the single, rolling baton-pass for the next session — overwritten each milestone.
> `patterns.md` Pattern 3 owns the minimum-handoff contract; `log.md` owns the append-only history.

Date: 2026-06-18
Working branch: `feature/research-candidate`

## Why this handoff exists

This session reviewed a colleague's Karpathy fidelity branch, shipped the agent-native lint + framing,
consolidated handoffs into the wiki, then restructured handoffs into this single rolling file.

## What changed

- Agent-native referential-integrity lint + tests (`b304f8c`); stale "Companion agent workflow" section
  removed from `map.md`/`index.md`; agent-native framing sharpened (Pattern 7, `map.md`, `operations.md`).
- Handoff consolidation: `CLAUDE.md` routes handoffs to the wiki, not `.claude/` (`99c8f96`).
- Karpathy fidelity review merged to `main` via PR #47 (squash, branch deleted, all checks green).
- Handoffs restructured: this single rolling `handoff.md` replaces the dated `handoffs/**` directory;
  the stale repo-root `handoff.md` was removed.

## Current understanding or hypothesis

The research wiki is an agent-native tool: faithful to Karpathy in form, divergent in motor (the agent
curates sources, writes, and reads; the human only asks questions; authority is promoted out). The lint
mechanizes referential integrity only — semantic consistency stays agent judgment.

## Next steps

1. Merge `feature/research-candidate -> main` when ready. Expect a `map.md` reconciliation: this branch
   removed the Companion section and added the agent-native lint, while `main` now carries the fidelity
   row from #47. Afterwards, `patterns.md` Background can point at the merged fidelity page.

## Blockers or open questions

- Champion freeze active until 2026-12-31 — no champion config changes.
- Pre-existing env gap (not this work): `tests/runtime/test_local_fetch_historical_script.py` fails to
  collect on `ModuleNotFoundError: pandera` (missing local dev dependency).
