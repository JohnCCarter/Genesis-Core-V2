# Filed query answers

> **Boundary note:** this page governs durable query answers for `docs/research/**`.
> Query pages preserve useful answers, but they do not act as runtime or promotion authority.

## Purpose

Give V2 a place to file back answers that are too useful to leave stranded in chat history.

## Minimum query record

Every durable query answer should include:

- the bounded question
- the consulted surfaces
- the answer summary
- the durable takeaways
- the linked `docs/research/log.md` entry

## Good fits

- repeated onboarding questions
- strategy/governance interpretation questions
- architecture explanations worth reusing later
- answers that changed how the research wiki should be structured

## Current registry

- `2026-06-04-karpathy-agent-discipline.md` ÔÇö filed answer capturing what Karpathy-style
  agent discipline means for V2 research work
- `2026-06-04-nvidia-skills-cherry-pick-review.md` ÔÇö filed answer capturing which NVIDIA
  skills patterns fit V2 without displacing the repo-native research wiki
- `2026-06-17-champion-1h-trade-frequency.md` - filed answer that the tracked 1h champion is
  effectively inert (entry gate too high) while a real but cost-fragile edge exists at a lower
  gate; the 3h re-tune was neutral-to-worse. Post-freeze validation target (Issue #12).
- `2026-06-17-karpathy-wiki-fidelity-review.md` — filed answer comparing the V2
  research wiki to Karpathy's `llm-wiki` gist: faithful in form (layers, loop,
  index/log), deliberately divergent in motor (human-gated, derivative,
  non-authoritative); largest gap is semantic lint.
- `2026-06-18-edge-mechanism-map-review.md` — non-authoritative edge/mechanism map under
  unresolved VWAP: both champions and both registered mechanisms `UNRESOLVED`, `EDGE_MAP=UNRESOLVED`;
  the only real OOS number is negative and the in-sample edge is bug-bypass-dependent. Not a
  profitability or promotion review.

## Next use

When a new answer proves reusable across sessions, start from `../templates/query-template.md`,
keep the question bounded, and link back to the raw sources it depends on.
