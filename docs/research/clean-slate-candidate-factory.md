# Clean-slate candidate factory (design)

> **Boundary note:** this is a derivative, **non-authoritative** design/research page. It proposes the
> *shape* of a future candidate lane; it issues no implementation, runtime, promotion, or champion
> authority. Nothing here builds a candidate, mutates a champion, runs a backtest, or tunes anything.
> Per ADR 0003, a research artifact may *propose*; it may not *approve*.

Status: active
Opened: 2026-06-18
Working branch: `feature/clean-slate-candidate-factory-design`
Knowledge product links: `index.md` · `map.md` · `log.md`

**Principle: Reuse the platform. Reset the candidate.**

## Purpose

Define a durable, V2-native design for a **clean-slate candidate lane**: one that reuses the clean,
tested platform spine but *resets* candidate logic so a new candidate starts from a **mechanism**, not
from threshold mining on an unresolved edge. This page answers *how the lane should be shaped* before any
implementation, so the first build slice inherits a clear boundary instead of inventing one under pressure.

It builds directly on three already-merged foundations:

- **Phase 1 guard** (PR #54) — research/candidate-search artifacts are non-authoritative by construction.
- **ADR 0003** (Accepted) — research/audit tooling may propose/evidence, not approve;
  `build_candidate_packet.py` is boundary-spanning (authority only via explicit human override + signoff).
- **Phase 3 manifest registration** — `seed_manifest.json` `research_tooling_surfaces`: visibility, not
  authority.

## 1. Boundary

- This is a **design page**, not a build. It carries **no implementation authority** and **no promotion
  authority**.
- It is exploratory *inside research* and strict *only at the authority/promotion edge* — the same posture
  as the rest of the lane.
- Building anything described here requires a **separate, scoped slice** with its own PRE/POST gates and a
  human gate. Reuse is not preservation; nothing is reused by default just because it is described here.

## 2. Why clean-slate

- The edge is honestly **unresolved**. `queries/2026-06-18-edge-mechanism-map-review.md` holds
  `EDGE_MAP = UNRESOLVED`: both tracked champions and both registered mechanisms are `UNRESOLVED`, the only
  real out-of-sample number is **negative** (`candidate_search_tBTCUSD_1h`: Sharpe −0.22, PF 0.53), and the
  in-sample edge is contingent on a staleness bypass.
- Existing V1/legacy candidates are **baseline/control only** (`infrastructure-fitness-audit.md`). They are
  kept for comparison, replay, and audit — never as a thing to rescue.
- **Do not rescue old candidates with more tuning.** Re-tuning thresholds on an unresolved edge is
  convenience over validity: it mines a result rather than testing a hypothesis. (3h re-tune was already
  neutral-to-worse; 1h is inert at the documented gate.)
- A clean lane therefore starts from a **mechanism hypothesis**, not from a config grid searched for a
  number that looks good in-sample.

## 3. What we reuse (the platform)

These are V2-native surfaces the new lane consumes as-is (read/evidence only). Most are clean and directly
tested; a few carry **guards** (flagged below, per the infrastructure audit) the lane must respect before
leaning on them — reuse is not a clean bill of health:

- **Data / read spine** — Bitfinex REST read spine (Batch G1/G2) and repo-tracked candle fixtures.
- **Backtest core** — `core.backtest.engine.BacktestEngine`; `position_tracker` is `KEEP_WITH_GUARDS`
  (zero-fee baseline, but models no funding cost and uses a flat slippage proxy).
- **Research wiki** — `docs/research/**` for hypotheses, prereg, evidence, and handoffs.
- **Trace / packets** — ADR 0002 substrate (`core/packets`, `core/trace`): records evidence; never issues
  authority.
- **Cost-stress tooling** — `scripts/analyze/cost_stress_sweep.py` (`research_only`). **Guard:** it injects
  the staleness bypass (`stale_threshold_factor=1e9`); its numbers are not valid edge until the `evaluate.py`
  ns-vs-ms staleness bug is fixed (post-freeze). The lane must not inherit bypass-dependent measurement —
  the bypass lives in the reused *platform*, and §6 rejects evidence that depends on it.
- **Candidate-packet tooling** — `scripts/audit/build_candidate_packet.py` (boundary-spanning; default
  output non-authoritative) over the tested `core.decision` comparison/premortem/promotion checks. The
  script *wrapper* itself has no direct test; its core (`candidate_builder`) does.
- **Governance / manifest boundary** — `seed_manifest.json` `research_tooling_surfaces` + ADR 0003.
- **Tests / gates where useful** — premortem (fail-closed), comparison, and the candidate-search guard test
  as a model for "research output cannot read as authority".

## 4. What we reset (the candidate)

The platform stays; the candidate's *logic and evidence chain* are rebuilt from scratch:

- **Candidate hypothesis** — a stated edge with a reason, not a parameter set.
- **Mechanism** — the economic/structural cause of the edge.
- **Feature selection** — causal, known-at-time-t inputs only.
- **Thresholds** — derived from the mechanism, not mined to fit history.
- **Training / eval doctrine** — OOS / walk-forward, placebo/null comparison, cost-stress.
- **Promotion evidence** — produced only along the explicit authority path; never inferred from a research
  artifact.

## 5. Candidate doctrine

Every new candidate must define, **before any run**, all of:

1. **Mechanism hypothesis** — what edge, and why it exists.
2. **Counterparty + persistence story** — who is structurally forced to pay, and why the edge does not
   arbitrage away. (The edge-map flagged that *neither* current mechanism has this.)
3. **Causal known-at-time-t feature contract** — every input available at decision time `t`; no lookahead.
4. **Null / placebo baseline** — a control the candidate must beat to be interesting.
5. **OOS / walk-forward plan** — the out-of-sample protocol, declared up front.
6. **Cost / slippage stress plan** — zero-fee baseline + slippage stress now; order-book VWAP later
   (`slippage-backtest-methodology.md`).
7. **Falsification rule** — the concrete result that *kills* the candidate.
8. **Classification rule** — what evidence would make it `REJECTED` / `UNRESOLVED` / `WATCH` / `CANDIDATE`
   (the edge-map vocabulary), so the verdict is decided by pre-declared criteria, not after seeing results.

## 6. Forbidden patterns

Not policing — these keep the *evidence valid*. A candidate built any of these ways cannot be trusted:

- **No Optuna-first candidate creation** — tuning is not a mechanism.
- **No threshold mining as mechanism** — a number that fits history is not an explanation.
- **No staleness-bypass-dependent evidence** — evidence that only appears with the evaluate-staleness
  bypass (`stale_threshold_factor=1e9`) is not real edge.
- **No in-sample-only claim** — in-sample success is a hypothesis, not a result.
- **No future leakage** — any feature not known at `t` invalidates the run.
- **No artifact → authority shortcut** — a research packet never becomes promotion evidence by itself
  (Phase 1 guard / ADR 0003).
- **No champion mutation** — champions are frozen (freeze active through 2026-12-31); the lane writes only
  to `results/`.

## 7. Research lane lifecycle (suggested)

A fail-closed pipeline where each stage leaves an artifact the next consumes. Research is cheap and fast up
front; rigor concentrates at the authority edge.

1. **Hypothesis / prereg** — declare mechanism, features, baseline, OOS plan, falsification, and
   classification criteria *before* running.
2. **Feature contract** — pin the causal, known-at-`t` inputs.
3. **Dummy fixture / leakage test** — fixtures-first; prove no lookahead before any real data.
4. **Minimal research runner** — produces evidence under `results/`, stamped non-authoritative.
5. **OOS evaluation** — walk-forward against the pre-declared protocol.
6. **Placebo / null comparison** — must beat the declared control.
7. **Cost-stress** — zero-fee baseline + slippage stress.
8. **Packet / report** — `build_candidate_packet` (default non-authoritative) + a trace/packet record.
9. **Human review** — the gate the lane cannot self-pass.
10. **Only later: authority gate** — explicit human override + signoff is the *sole* route to
    promotion-readiness.

## 8. First minimal future implementation slice (define only — do not build now)

Three plausible first steps were considered:

- **(a) Candidate prereg template** — `docs/research/templates/candidate-prereg-template.md` encoding the
  §5 doctrine (mechanism, counterparty/persistence, feature contract, baseline, OOS plan, falsification,
  classification).
- **(b) Tiny fixture-based candidate-contract test** — a leakage/known-at-`t` fixture check.
- **(c) Research-only candidate-factory skeleton** — a runner stub writing non-authoritative evidence.

**Recommendation: start with (a), the prereg template.** Rationale: it is the lowest-risk, docs-only step;
it forces mechanism-first discipline before any code exists; it matches the repo's template-driven research
convention; and it makes (b) and (c) cheap to add once at least one mechanism is preregistered. Building (c)
before a single preregistered mechanism would be a runner in search of a hypothesis — the exact inversion
this lane rejects.

## 9. Stop rules

Stop before implementation and report if any of these hold:

- the design requires **new authority semantics**;
- the design requires **champion / config mutation**;
- the design **cannot separate research output from authority**;
- the **mechanism is undefined** (no hypothesis = nothing to test);
- evaluation **depends on old V1 candidate outputs** as truth (they are baseline/control only);
- **cost / slippage assumptions are unclear** or unstated.

## Current status

**Open** — design only; no implementation authorized. The recommended first slice (§8a, prereg template) is
a separate future docs-only slice pending review. The open "absorb-NOW" testing-hardening items
(mutation/property tests for the decision kernel, OOS-leakage hardening) are tracked separately and are
natural dependencies this lane will lean on.
