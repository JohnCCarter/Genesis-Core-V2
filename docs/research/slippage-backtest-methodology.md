# Slippage and cost methodology for backtest

> **Boundary note:** this is a derivative research page.
> It compiles current evidence and open questions, but it does not act as runtime or promotion
> authority by itself.

Status: active
Opened: 2026-06-18
Working branch: `feature/research-candidate`
Knowledge product links: `index.md` · `map.md` · `log.md`

## Purpose

Record how transaction cost is modeled in the V2 backtest — specifically how slippage should be
derived, what holds when no order book is available, and why the current cost numbers are assumptions
rather than exchange facts. This exists so future sessions reason about cost from a stable page instead
of re-deriving the methodology from chat or raw code scans.

## Review question

How should slippage be modeled in the V2 backtest, what is the correct order-book-derived computation,
and what conservative fallback holds when order-book depth is not available?

## Source surfaces

- `src/core/backtest/position_tracker.py` — where cost is actually applied per trade
- `src/core/backtest/engine.py` — passes `commission_rate` / `slippage_rate` into the tracker
- `config/backtest_defaults.yaml` — default cost values loaded by the pipeline
- `scripts/analyze/cost_stress_sweep.py` — the existing slippage stress branch
- `src/core/strategy/mechanism_registry.py` — cost-sensitivity tripwires for the tracked edge
- `src/core/io/bitfinex/ws_public.py` — Bitfinex public WS (dormant; ticker-only, no `book` channel)
- GitHub Issue #12 — post-freeze cost-fragility follow-up (freeze ends 2026-12-31)
- Bitfinex zero-fee announcement (effective 2025-12-17): [bitfinex.com/zero-fee-trading](https://www.bitfinex.com/zero-fee-trading/),
  [blog.bitfinex.com — zero-fees Q&A](https://blog.bitfinex.com/education/zero-fees-qa/)

## Current compiled understanding

- **Bitfinex publishes no general slippage figure.** It exposes market data and an order book; slippage
  is a property of *your order against that book*, not a headline number. So the backtest must never
  encode a claim like "Bitfinex slippage = 5 bps" — it must either derive slippage from order-book depth
  or run explicit stress scenarios.
- **Fee ≠ slippage, and the model already keeps them separate.** Commission and slippage are independent
  inputs in [position_tracker.py:120-121](../../src/core/backtest/position_tracker.py#L120-L121):
  `commission_rate` is charged on notional; `slippage_rate` moves the fill price. This separation is
  correct as-is — it is not a gap to fix.
- **Bitfinex trading fee is now zero — current documented standard, not an assumption.** Announced
  **2025-12-17**, Bitfinex moved maker and taker trading fees to zero for all eligible trading products
  (spot, margin, derivatives, Bitfinex Securities eligible products, OTC), with no volume / token-holding /
  tier condition. Bitfinex's own framing (verified against their sources): it is *"the new standard"*, *not
  a short-term promotion*, with *no fixed end date* — and they reserve the right to alter fees in future
  with customer notice. So this is **current documented Bitfinex reality**, not an eternal guarantee; the
  doc must not call it "permanent". Therefore `commission: 0.0` in `config/backtest_defaults.yaml` is the
  *correct current baseline* for Bitfinex spot backtests, not merely a convenience assumption. (The
  `commission_rate=0.002` Taker constructor default in `position_tracker.py` is now a historical value,
  harmless because config overrides it to 0.0.)
- **Funding / margin-lending is a separate exchange-cost component.** The zero-fee change did *not* touch
  margin lending or funding fees ("margin lending and funding fees are not changing"), nor deposit/withdrawal
  fees. Funding is separate from both fee and slippage and is relevant **only** when a strategy actually
  takes margin / leverage / funding exposure. Verified for the tracked champions: `tBTCUSD_1h.json` and
  `tBTCUSD_3h.json` are spot RI configs with fraction-of-capital sizing and **no** leverage/margin/funding
  parameters, and `position_tracker.py` models no funding/borrow cost — so funding does not apply to them as
  configured today. It would apply if a future strategy used funding exposure.
- **Order-book-derived slippage (the correct method when depth exists).** Walk the book until the order
  size is filled, take the size-weighted average fill price (VWAP), and express the gap to a reference
  price in basis points:
  - market **buy**: walk asks → VWAP; `slippage_bps = (VWAP − ref) / ref × 10_000`
  - market **sell**: walk bids → VWAP; `slippage_bps = (ref − VWAP) / ref × 10_000`
  - reference price choice: **mid** = cleanest market-impact measure (recommended default);
    **best bid/ask** = closer to execution; **candle close** = weaker approximation. The mid↔best-bid/ask
    gap is the half-**spread** — a distinct cost component, kept separate from slippage/market-impact (as
    fee is) rather than folded into the slippage number.
- **When no order book exists, run stress scenarios — and call them assumptions.** With only OHLCV
  data, slippage cannot be derived, so the conservative path is to sweep low / normal / stressed levels
  and report where the edge dies. These levels are *assumptions*, not Bitfinex facts, and must be
  labeled that way wherever they appear.
- **No trading-claim until the edge survives fee + slippage sensitivity.** A result that only holds at
  zero or low cost is not an edge. Survival across the cost grid is a precondition for any stronger
  claim; this stays deferred to post-freeze (Issue #12).

## Verified findings

- **The system is always in the stress branch today.** `ws_public.py` subscribes only to the `ticker`
  channel and the engine runs on OHLCV candles — there is no `book` channel, no depth storage, and no
  VWAP computation anywhere in `src/`. The order-book branch is greenfield.
- **Current slippage application is a flat, symmetric proxy.** In
  [position_tracker.py](../../src/core/backtest/position_tracker.py) the fill is
  `price * (1 ± slippage_rate)` on entry, exit, and partial exit — size-independent and applied against
  the candle price, not a VWAP against mid. Constructor defaults: `commission_rate=0.002` (Taker),
  `slippage_rate=0.0005`. `config/backtest_defaults.yaml` overrides commission to `0.0` (current documented
  Bitfinex baseline) and keeps slippage at `0.0005` (still a proxy assumption).
- **The stress branch already exists as tooling.**
  [cost_stress_sweep.py](../../scripts/analyze/cost_stress_sweep.py) sweeps the tracked champions over
  commission ∈ {0, 5, 10, 20} bps × slippage ∈ {5, 10, 20, 40} bps and flags edge death at Sharpe < 1.0
  or PF < 1.1, writing `artifacts/diagnostics/cost_stress_sweep_<date>.md`. Read the two axes differently
  now: the **commission** axis is a *fee-return / robustness probe* (the realistic Bitfinex baseline is the
  zero column), while the **slippage** axis stays a *realistic conservative proxy* — order-book depth is not
  yet modeled, so sweeping slippage is the honest way to bound an unmeasured cost.
- **The cost-fragility is already recorded.** `mechanism_registry.py` encodes tripwires that the tracked
  `tBTCUSD_1h` edge does not survive slippage ≥ 40 bps; `queries/2026-06-17-champion-1h-trade-frequency.md`
  records the same fragility (dies by ~10 bps on the 0.60 gate).

## Tensions to resolve

- **Ideal method vs current proxy.** The correct method is VWAP-from-order-book against mid; the engine
  applies a flat rate against candle close. The proxy is a reasonable stand-in while no depth data
  exists, but the divergence should be closed (or explicitly accepted) before any execution-near claim.
- **Which numbers are facts vs assumptions (cost numbers are not all assumptions).** Keep the taxonomy
  precise:
  - `commission: 0.0` is **documented Bitfinex reality** for eligible maker/taker trading (since
    2025-12-17), not an assumption.
  - `slippage: 0.0005` and the **slippage** stress levels remain **assumptions about an unmeasured book**
    until derived from order-book depth, and must be labeled so wherever cited.
  - the commission stress values above zero (`{5, 10, 20}` bps in the sweep) are **hypothetical robustness
    probes** ("what if fees returned"), not current-reality claims.
  - funding / margin-lending is a **separate** cost that applies **only** under margin / leverage / funding
    exposure (not the spot `tBTCUSD` champions).
- **Claim gate.** No edge claim may rest on low-cost results alone; survival across the fee + slippage
  grid is required. This is deferred behind the champion freeze (ends 2026-12-31, Issue #12) and must
  not reopen champion config before then.

## Implication: zero trading fees ≠ zero execution cost

The zero-fee change removes the *fee* line, not the *cost* of executing. An order still moves the book,
crosses the spread, and arrives with latency against an informed counterparty. So the research burden does
not shrink — it shifts off fees and onto components that were always there but were previously dwarfed by a
20 bps taker fee. Each is a **separate** cost to model, not a single "slippage" number:

- **spread** — the bid/ask gap actually crossed (half-spread per side), separate from market impact.
- **order-book depth** — how far the order walks the book before it is filled.
- **order-size-aware VWAP slippage** — the size-weighted fill vs a reference price (the deferred slice).
- **latency / adverse selection** — fills arriving late or against information, modeled as their own
  stress assumptions, not folded into the flat slippage proxy.

Net: with fees at zero for spot, these are now the dominant executable costs, and bounding them
conservatively (stress/proxy) remains the honest stance until order-book depth is actually measured.

## Implementation path (deferred order-book VWAP slice)

A future, separately validated slice — **planned, not built**, and out of scope under the current freeze
and the dormant-transport boundary.

With the Bitfinex trading fee now zero for spot, the fee axis of the cost grid collapses to ~0 and
slippage carries essentially all of the executable cost. That vindicates the fee ≠ slippage separation and
shifts all the weight to the slippage half — making this order-book VWAP slice relatively **more**
important, not less, once the freeze lifts.

The first build target is an **isolated, pure deterministic helper** — `orderbook_vwap_bps(...)` — validated
on fixture order books before anything else. No live transport, no engine wiring, no champion/promotion use
until it passes a separate validation gate.

- **Helper contract (deterministic, fixtures first):**
  - **inputs:** `side` (buy/sell), `order_size`, `bids` / `asks` (price/size ladders), `reference_price`.
  - **outputs:** `vwap`, `filled_size`, `slippage_bps`, `spread_bps` (or an explicit spread component),
    `depth_exhausted` flag (true when the book can't fill the full size).
  - **properties:** pure and side-effect-free; deterministic for identical input; spread and book-impact
    reported as **distinct** components, never folded into one number.
- **Scope IN:** the pure helper above and its fixture order books; a reference-price config knob (default
  mid); explicit, documented assumptions for **spread**, **partial fills**, and **liquidity / depth
  exhaustion**; later (only after the helper is validated) a `book`-channel / equivalent depth source and
  snapshot/stream persistence to feed it.
- **Scope OUT (now):** rebinding the dormant `ws_public.py` `book` subscription into the live transport
  path; any depth-pipeline or backtest-engine wiring; any runtime / champion-config surface; any promotion
  of cost numbers to authority.
- **Gating / sequence:** runs after the freeze; champion config stays untouched; no trading-claim without
  fee + slippage sensitivity evidence. Order: **(1)** pure helper on fixtures → **(2)** validation gate →
  **(3)** measured slippage distribution from real depth → **(4)** only then consider replacing the flat
  proxy. No step skips ahead.

## Immediate next checks

1. Post-freeze, run [cost_stress_sweep.py](../../scripts/analyze/cost_stress_sweep.py) on current data
   and record the actual survival surface (Issue #12) — do not build the order-book slice first.
2. Decide whether `config/backtest_defaults.yaml` should carry an inline comment marking `slippage` as
   an assumption, so the framing travels with the value.

## Durable notes

- Prefer linking to `position_tracker.py`, `cost_stress_sweep.py`, and the freeze/Issue-12 contract over
  copying their content here.
- Keep the page Obsidian-friendly: plain Markdown, stable headings, narrow scope.

## Current status

Open. Methodology is recorded and the order-book slice is scoped but deferred; the next concrete step is
the post-freeze stress run, not the implementation. Updated 2026-06-18 with the Bitfinex zero-fee change
(effective 2025-12-17): spot trading fee is now zero, funding/margin-lending remain, and slippage now
carries the executable cost for spot — raising the relative priority of the deferred VWAP slice.
