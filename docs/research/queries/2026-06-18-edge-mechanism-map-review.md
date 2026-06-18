# Edge / mechanism map review (under unresolved VWAP)

> **Boundary note:** this is a durable, **non-authoritative** query-answer record. It maps mechanism /
> edge status from existing evidence; it does **not** issue runtime, promotion, or readiness authority,
> and it is **not** a profitability or promotion review. No conclusion here is "production-grade",
> "live-ready", "promote-ready", or "net profitable under real execution".

Date: 2026-06-18
Working branch: `feature/research-candidate`
Knowledge product links: `../index.md` · `../map.md` · `../log.md`

## Question

What is the honest status of the edge mechanisms the V2 system bets on, given that order-book-VWAP
slippage is still unsolved? For each mechanism/champion: is there a real mechanism, standalone OOS/forward
evidence, and survival under the current cost proxy — and what is the right status
(`REJECTED` / `UNRESOLVED` / `WATCH` / `CANDIDATE`)?

## Interpretation frame (how current results may be read)

Current results may be interpreted **only** as:

- mechanism / edge-candidate mapping
- **+** fee-adjusted baseline (Bitfinex spot trading fee is now a documented zero — see
  `../slippage-backtest-methodology.md`)
- **+** slippage-stress proxy (flat `slippage_rate`, a conservative assumption)
- **−** not order-book-VWAP adjusted
- **−** not execution-final

Zero trading fees sharpen the commission baseline but resolve none of spread / order-book depth / VWAP /
latency. No result may be called execution-final without VWAP/depth evidence.

## Consulted surfaces

- `../slippage-backtest-methodology.md` — cost taxonomy (fact vs assumption), deferred VWAP slice
- `docs/strategies/MECHANISMS.md` + `src/core/strategy/mechanism_registry.py` — the two registered mechanisms
- `config/strategy/champions/tBTCUSD_1h.json`, `config/strategy/champions/tBTCUSD_3h.json` — committed champions
- `scripts/analyze/cost_stress_sweep.py` — the cost-stress reproducer (read only; not re-run here)
- `2026-06-17-champion-1h-trade-frequency.md` — prior trade-frequency / cost-fragility finding
- `tools/reconcile_forward_backtest.py` — forward-vs-backtest reconciliation **tool** (no committed champion run)
- `results/evaluation/candidate_search/candidate_search_tBTCUSD_1h_*.json` — a real OOS-style evaluation (evidence only)
- `results/evaluation/ri_p1_off_parity_v1_*.json`, `results/hparam_search/run_optuna/*` — parity / Optuna artifacts (evidence only)

## Observed findings (facts from the surfaces)

- **Two registered mechanisms only.** `ml_confidence_v1` (status `UNVERIFIED`) and `regime_intelligence_v1`
  (status `EXPERIMENTAL`). `has_verified_edge()` is False → `EDGE_MAP = UNRESOLVED`. No mechanism is `CANDIDATE`.
- **The only real OOS-style number is negative.** `candidate_search_tBTCUSD_1h` (run 2026-06-02, ~6-week
  window 2026-04-20 → 2026-06-01): incumbent **Sharpe −0.221, PF 0.532**, winrate 45%; the **best** searched
  candidate carries `hard_failures: ['pf<1.0']` (Sharpe −0.192). All five evaluations are negative. The
  searched gate (`entry_conf_overall ≈ 0.26`) is close to the committed champion's `0.25`.
- **The in-sample edge depends on a bug bypass.** `cost_stress_sweep.py` injects
  `stale_threshold_factor=1e9` to bypass a nanosecond-vs-millisecond staleness bug in `evaluate.py`;
  **without the bypass, confidence is halved → 0 trades**. The PF 1.24 (1h) / 1.585 (3h) figures exist only
  with that bypass active.
- **The cost-fragility numbers are unreproduced.** The 30-month sweep figures (`conf≥0.60`: PF 1.24,
  Sharpe 0.72, 183 trades; 3h PF 1.585 collapsing to ~1.11 by 40 bps) originate from a since-deleted branch
  and are explicitly **not** independently re-verified (see `2026-06-17-champion-1h-trade-frequency.md`).
- **Optuna / parity artifacts are test fixtures, not champion evidence.** `run_optuna/run_meta.json` is a
  `test-study` (snapshot `tTEST_1h`, `n_trials=1`, `best_value=1.0`); `best_trial.json` points at
  `dummy.json` with empty metrics. The parity artifact `ri_p1_off_parity_v1_*` is `parity_verdict: FAIL` on
  a synthetic `tTESTBTC:TESTUSD` symbol — tooling status, not a champion forward run.
- **No committed positive OOS/forward evidence exists** for either champion.

## Inferred findings (reasoning from the facts)

- The committed `tBTCUSD_1h` champion sits at the gate (~0.25) whose real OOS evaluation is **negative**.
  The "edge" discussed in prior findings lives at a *different* gate (0.60) that was only ever measured
  in-sample, under the bug bypass, with Sharpe (0.72) below the 1.0 death line even at low cost.
- `regime_intelligence_v1` (3h) has **Sharpe < 1.0 at zero cost** — an in-sample quality floor that is
  independent of execution cost. Its PF 1.585 is in-sample, bypass-dependent, and cost-fragile.
- **Neither mechanism has a counterparty / persistence story.** `ml_confidence_v1` is a pure statistical
  confidence bet with no stated reason a counterparty is "forced to pay us"; `regime_intelligence_v1` has a
  *plausible* persistence rationale (trend/regime momentum) but it is unconfirmed. Absent a persistence
  argument, neither can reach `CANDIDATE` regardless of cost modeling.

## Unverified gaps

- **Gate conflation.** Committed gate `0.25` vs swept-edge `0.60` vs inert `0.70` are three different
  configs; the cost-stress narrative may not describe the committed champion at all. We do not have a clean
  read of the committed champion's own edge curve.
- **Reproduction missing.** The in-sample sweep has not been independently re-run here (scope: no new runs),
  and it is contingent on the staleness-bug bypass rather than a real fix.
- **OOS sample is thin.** The one negative OOS window is ~6 weeks / one regime — strong as disconfirming
  evidence, weak as a generalization.
- **No forward reconciliation.** `tools/reconcile_forward_backtest.py` exists but no committed champion
  forward-vs-backtest run does; the only parity artifact FAILs on a synthetic test symbol.

## Mechanism table

| Mechanism | Causal claim | Counterparty / persistence | Standalone OOS/forward | Survives proxy cost? | VWAP-dependent to decide? | Status (this review) |
| --- | --- | --- | --- | --- | --- | --- |
| `ml_confidence_v1` (1h) | confidence > tuned threshold marks positive-expectancy bars | **none stated** (pure statistical) | **negative** (Sharpe −0.22, PF 0.53, ~6 wk) | no — in-sample edge dies by ~10 bps, and that is unreproduced/bypass-dependent | **no** — fails before VWAP subtlety matters | **UNRESOLVED** (closest to REJECTED, pending one reproduction) |
| `regime_intelligence_v1` (3h) | conditioning on regime persistence avoids low-edge regimes | plausible but **unconfirmed** | **none** | weak — Sharpe < 1.0 at *zero* cost; PF collapses by ~40 bps | partial (necessary, not sufficient) | **UNRESOLVED** |

Registry mirror for reference: `ml_confidence_v1` = `UNVERIFIED`, `regime_intelligence_v1` = `EXPERIMENTAL`
(code statuses are not flipped by this review).

## Status per champion / policy

- **`tBTCUSD_1h` → UNRESOLVED** (dominant disconfirming evidence: negative real OOS). It is **not** marked
  `REJECTED`: a falsification claim requires a reproduced run, which is out of scope here. The committed
  champion is effectively inert at its high gate, and the lower-gate "edge" is in-sample-only,
  bypass-dependent, and cost-fragile. Honest framing: *closest to REJECTED, pending one reproduction.*
- **`tBTCUSD_3h` → UNRESOLVED.** Backtest-only PF 1.585 but Sharpe < 1.0 everywhere (in-sample floor), no
  OOS/forward, cost-fragile; the prior 2x-sizing re-tune was neutral-to-worse. Not `WATCH`: zero-cost
  Sharpe < 1.0 is a quality problem, not merely a VWAP/cost question.
- **Global `EDGE_MAP` → UNRESOLVED.** Consistent with the registry; no mechanism is `CANDIDATE`.

## VWAP dependency per result

Neither result is **blocked** by VWAP:

- **1h:** fails on negative OOS + non-reproducible, bypass-dependent in-sample numbers — *before* execution
  cost subtlety matters. VWAP is irrelevant to its current status.
- **3h:** fails on Sharpe < 1.0 at zero cost (in-sample) plus missing OOS. VWAP/depth is **necessary but not
  sufficient** to ever decide it — required downstream, but not the binding constraint today.

So "unresolved VWAP" must not absorb blame that belongs to missing OOS + in-sample weakness.

## Next smallest falsifiable experiment (needs-experiment — not built here)

**Reproduce the committed 1h champion's cost-stress curve on an out-of-sample split, without the staleness
bypass.** Concretely: confirm whether the `conf≥0.60` 1h edge reproduces OOS at ≤10 bps cost once the
nanosecond-staleness bug is *fixed* (not bypassed). If it does not reproduce → the 1h moves to `REJECTED`;
if it does → it is a genuine `WATCH` candidate pending VWAP/depth.

This requires a new run (and a code fix to `evaluate.py`), so it is flagged **needs-experiment** and not
executed under this docs-first scope. It is post-freeze work (champion-adjacent), aligned with GitHub
Issue #12.

## Durable takeaways

- The bot still has **no verified edge**; the only real OOS number is negative, and the in-sample edge is
  contingent on a bug bypass. Treat every "champion performance" figure as in-sample and unreproduced until
  an OOS run without the bypass exists.
- Zero trading fees clarify the commission baseline but change none of the mechanism verdicts.
- A mechanism cannot reach `CANDIDATE` on cost modeling alone — it needs a counterparty/persistence story,
  standalone OOS/forward evidence, and survival under proxy cost. None of the three is met today.

## Linked log entry

See `../log.md` → `## [2026-06-18] question | edge / mechanism map review (under unresolved VWAP)`.

## Current status

Open — both champions and both mechanisms `UNRESOLVED`; `EDGE_MAP = UNRESOLVED`. Next step is a falsifiable
OOS reproduction (needs-experiment, post-freeze / Issue #12), not any build under this scope.
