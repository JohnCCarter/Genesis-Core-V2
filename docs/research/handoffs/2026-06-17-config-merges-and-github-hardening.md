# 2026-06-17 config separation, branch merges, GitHub hardening

> **Boundary note:** this is a short baton-pass note for a future session.
> It preserves continuity, but it does not replace topic pages, logs, or authority surfaces.

Date: 2026-06-17
Working branch: `feature/research-candidate`
Knowledge product links: `../index.md` · `../map.md` · `../log.md`

## Why this handoff exists

A long ops/infra session ended with everything merged to `main` and `feature/research-candidate`
recreated fresh. This note is the durable, git-tracked record of that milestone; per-PR granularity is
recoverable from the `main` history (PRs #9-#45).

## What changed

- **Config separation:** added repo-root `CLAUDE.md`; made `~/.claude` agnostic (machine-only).
- **Branch review:** salvaged seed-admissible work into PRs #9 (optimizer robustness + cost-stress),
  #10 (edge-mechanism register), #11 (forward/backtest reconcile); deleted the redundant `bw9a51`
  and the freeze-violating `phase1-c4lss0` (champion edits never merged).
- **Run-trace foundation** merged (PR #14, merge-commit).
- **CI/security:** PR #13 cleared starlette/cryptography CVEs; all bot-review findings fixed.
- **GitHub hardening:** branch protection on `main` (PR + `lint-test` + `check-champion-freeze`);
  Dependabot security updates + alerts; auto-merge workflow (patch/minor/actions) + auto-delete;
  `copilot-setup-steps.yml` for remote coding-agent work; Dependabot ignores for fastapi,
  websockets, numpy(major), pyarrow(major).
- **Hygiene:** pruned unused keys from `.env` / `.env.example`.

## Current understanding or hypothesis

`main` carries the run-trace substrate + the new research tooling (robustness PSR/DSR/PBO/FDR,
cost-stress sweep, forward/backtest reconcile, edge-mechanism register). `EDGE_MAP=UNRESOLVED`
still holds — no mechanism has reached `CANDIDATE`. The tooling now exists to actually test that.

## Next steps

1. Pick the next research focus on `feature/research-candidate` — natural fit: use the new
   robustness + reconcile tooling to validate a mechanism toward `EXPERIMENTAL → CANDIDATE`.
2. Post-freeze (after 2026-12-31): validate the 1h champion frequency gate — see
   `../queries/2026-06-17-champion-1h-trade-frequency.md` and GitHub Issue #12.

## Blockers or open questions

- Champion freeze active until 2026-12-31 — no champion config changes.
- Deliberate dep migrations deferred (numpy 2, pyarrow 24, fastapi 0.137, websockets 16); fastapi
  needs a version-robust route flattener for the inertness guard, websockets needs a fix at
  `ws_reconnect.py:66`.
- Verify the retained (de-duplicated) `NVIDIA_API_KEY` value in local `.env` is the intended one.
