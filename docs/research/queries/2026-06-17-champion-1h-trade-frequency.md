# Champion tBTCUSD_1h trade frequency

> **Boundary note:** this is a durable query-answer record.
> It preserves a bounded answer for later sessions, but it does not act as runtime or promotion
> authority.

Date: 2026-06-17
Working branch: `feature/research-candidate`
Knowledge product links: `../index.md` · `../map.md` · `../log.md`

## Question

Does the tracked `tBTCUSD_1h` champion actually trade, or is its entry gate so high that it is
effectively inert — and is the 3h re-tune that was proposed alongside it any better?

## Why this answer should persist

The finding surfaced from an agent research branch (`claude/trading-policy-eval-phase1-c4lss0`,
since deleted) whose champion edits could not merge under the champion freeze. The branch is gone,
so the one durable insight it produced must live somewhere git-tracked, or it is lost. It is also
an actionable post-freeze validation target.

## Consulted surfaces

- `config/strategy/champions/tBTCUSD_1h.json`
- `config/strategy/champions/tBTCUSD_3h.json`
- `scripts/analyze/cost_stress_sweep.py` (the reproducer; landed via PR #9)
- `src/core/optimizer/robustness.py`
- GitHub Issue #12 (post-freeze validation task)

## Answer summary

> Numbers below are the research branch's **own** self-reported cost-stress sweeps
> (baseline 0+5 bps, 30 months), **not** independently re-verified. Reproduce with
> `scripts/analyze/cost_stress_sweep.py` before acting.

- **1h — effectively inert (frequency gate too high).** The current 0.70 entry gate produced
  ~**3 trades / 30 months** (statistically meaningless). A 0.60 gate yielded **183 trades** with
  per-period Sharpe **> 1.0** at low cost — a **real but cost-fragile** edge: PF
  1.42 → 1.30 → 1.03 → 0.71 as slippage rises 5 → 10 → 20 → 40 bps; Sharpe drops below 1.0 by
  ~10 bps total cost.
- **3h — not better.** The proposed re-tune (2x sizing + a new 0.50 tier) **diluted** the edge and
  breached the drawdown budget under realistic slippage; reverting to 1.5x merely restored the
  original PF (1.585) while **raising** max drawdown (3.28% → 4.85%). Net neutral-to-worse.
- Both edges die at >=20 bps slippage; no mechanism reaches `CANDIDATE` (consistent with
  `EDGE_MAP=UNRESOLVED`).

## Durable takeaways

- The current 1h champion barely trades — treat any "1h champion performance" claim as suspect
  until the frequency gate is validated on a meaningful sample.
- A real 1h edge likely exists at a lower gate but only survives at <=10 bps total cost; cost
  sensitivity must be a first-class acceptance criterion, not an afterthought.
- Do not repeat the 3h 2x-sizing re-tune; it added risk without return.
- Champion changes are frozen until 2026-12-31; this is a post-freeze validate-then-promote task.

## Linked log entry

See `../log.md` → `## [2026-06-17] question | champion 1h trade-frequency finding (Issue #12)`.

## Current status

Open — deferred to post-freeze (after 2026-12-31), tracked as GitHub Issue #12.
