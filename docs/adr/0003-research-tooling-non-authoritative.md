# ADR 0003: Research and audit tooling paths are non-authoritative

- Status: Accepted (2026-06-18)
- Date: 2026-06-18
- Scope: Governance/boundary only. Classifies the repo's research/audit tooling as research-only paths and reaffirms that promotion/champion authority requires the explicit authority path + human signoff. No runtime, authority, config, champion, strategy, optimizer, backtest, or transport change.
- Owners: Saliba (solo dev) + AI agents

## Context

After the V2 seed was generated, the repository accumulated genuinely useful research/audit tooling — the
"unregistered research paths" named in `docs/research/infrastructure-fitness-audit.md`. These tools search,
score, stress, and reconcile; they write evidence under `results/`; they mutate no authority surface. They
are **not wrong** — they are legitimate research infrastructure. The only risk is interpretive: a later
reader (human or agent) could mistake their output for promotion / champion / signoff **authority**.

ADR 0001 already sets the rule (*agent/LLM/research output is proposal-evidence, never authority*), and
ADR 0002 makes the run-trace *record* evidence while authority stays in the decision/governance code. This
ADR makes that boundary concrete for the candidate-search / decision tooling and records the guard that now
enforces it (PR #54).

Operating principle: **Research should be easy. Authority should be hard.**

## Decision

The following paths are covered by the research↔authority boundary. Most are research/evidence-only paths
that may *propose* but may not *approve*. `build_candidate_packet.py` is **boundary-spanning**: by default
it produces proposal/evidence packets, while real promotion-readiness is reachable only through the explicit
human override + signoff authority path.

- `scripts/audit/find_new_champion_candidate.py` — candidate search. Proposes candidates from a
  runtime-seed grid; writes only under `results/evaluation/candidate_search/`; reads the seed read-only.
  Its artifacts are stamped `authority: {status: "research_only", non_authoritative: true,
  requires_human_signoff: true}` and hold `ready_for_promotion` structurally False.
- `scripts/audit/build_candidate_packet.py` — decision-packet CLI; **boundary-spanning**. Its default /
  no-signoff output is non-authoritative (a proposal/evidence packet). The explicit human override + signoff
  path (`--promotion-override --promotion-signoff`, which `apply_promotion` requires) is the **authority
  path** that can reach real promotion-readiness. It must not be confused with the research-only
  candidate-search output of `find_new_champion_candidate.py`.
- `scripts/analyze/cost_stress_sweep.py` — cost-stress research probe.
- `tools/reconcile_forward_backtest.py` — forward/backtest reconciliation evidence.
- the run-trace + packet substrate (ADR 0002) — records evidence; it never issues promotion authority.

**Invariant:** a research artifact may propose; it may not approve. `ready_for_promotion` / promotion /
champion status is never true merely because a research script ran or forced flags. The only path to real
promotion-readiness is the explicit authority path — a human asserting override **and** signoff — enforced
by `apply_promotion` (`src/core/decision/promotion.py`) and gated by `build_candidate_packet`
(`src/core/decision/candidate_builder.py`).

Registration of these paths in `seed_manifest.json` is a separate follow-up (visibility/auditability, not
authority). **Registration grants visibility; it never grants authority.**

## Consequences

- Research stays easy: these tools run freely and write evidence. Authority stays hard: explicit human
  signoff remains the sole route to promotion-readiness.
- A later reader or agent can trust the boundary from the artifact's own stamp plus this ADR, without
  re-deriving intent from the script.
- The obsolete qwen/glm/nvidia LLM-builder tooling was removed (PR #53) and is not part of this boundary.
- Concrete pointers to this ADR from the manifest-hashed governance docs (`AGENTS.md`,
  `.github/copilot-instructions.md`, `docs/SKELETON_SCOPE.md`) are deferred to the manifest-registration
  slice, where their seed-manifest hashes are refreshed in the same change.

## Validation

- PR #54 merged the candidate-search guard: artifacts stamped non-authoritative, forced
  `promotion_override/signoff` removed, the opt-in `--trace` gate de-authorized
  (`issued_by` `"governance-kernel"` → `"candidate-search"`), proven by
  `tests/governance/test_candidate_search_artifact_guard.py`.
- `apply_promotion` returns `PROMOTE` only with both override and signoff true
  (`src/core/decision/promotion.py`); `ready_for_promotion` gates on that
  (`src/core/decision/candidate_builder.py`). CLI smoke: default flags → not ready; explicit human
  override + signoff → ready.
- Consistent with ADR 0001 (proposal-evidence, never authority) and ADR 0002 (the trace records evidence,
  never issues authority).

## Out of scope

- `seed_manifest.json` registration of these paths and the AGENTS/copilot/SKELETON_SCOPE pointers (separate
  manifest-registration slice).
- Any runtime / authority / champion / config / strategy / optimizer / backtest / transport / VWAP change.
- Clean-slate candidate factory design (separate slice).
