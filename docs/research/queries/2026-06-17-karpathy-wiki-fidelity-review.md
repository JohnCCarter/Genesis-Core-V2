# Karpathy LLM-wiki fidelity review

> **Boundary note:** this is a durable query-answer record.
> It compiles one bounded comparison for later sessions, but it does not act as
> runtime or promotion authority.

Date: 2026-06-17
Working branch: `claude/karpathy-llm-wiki-obsidian-refanw`
Knowledge product links: `../index.md` · `../map.md` · `../log.md`

## Question

How faithfully does the V2 research wiki (`docs/research/**`) implement Andrej
Karpathy's `llm-wiki` pattern, and where does it deliberately diverge?

## Why this answer should persist

The repo's whole research layer is an adaptation of an external pattern. A
session asked to extend or defend that layer should not have to re-derive what
was borrowed faithfully versus what was changed on purpose. This page makes the
form-vs-motor split explicit so future work changes the right knob.

## Consulted surfaces

- `docs/research/index.md` (three-layer mapping, invariants, governance)
- `docs/research/map.md` (navigation/registry)
- `docs/research/operations.md` (ingest/query/lint loop)
- `docs/research/patterns.md` (Pattern 7 external-pattern absorption rule)
- `docs/research/sources/index.md` (raw-source layer contract)
- `scripts/audit/research_wiki_lint.py` (structural lint behavior)
- `docs/research/queries/2026-06-04-karpathy-agent-discipline.md` (prior answer)
- `https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f` (gist)

## Answer summary

The V2 wiki reproduces Karpathy's **form** almost exactly — the three-layer
split (raw sources → wiki → schema), the three operations (ingest / query /
lint), a content-oriented navigation index (`map.md` ≈ his `index.md`), and an
append-only prefixed chronology (`log.md`). It then swaps out his **motor**:
where Karpathy's wiki is LLM-owned, low-friction, and treated as the
compounding source of truth, V2's is human-gated, high-friction, and explicitly
derivative/non-authoritative. Faithful in the skeleton; deliberately heretical
in the soul. This is a defensible trade for a fail-closed trading domain, but it
partially gives up Karpathy's core value proposition (query the compiled
artifact instead of re-deriving).

## Form vs motor

| Dimension        | Karpathy gist                                  | V2 `docs/research/**`                                  |
| ---------------- | ---------------------------------------------- | ----------------------------------------------------- |
| Layer split      | raw sources → wiki → schema                    | same; schema = `index.md` + `AGENTS.md` + copilot doc |
| Operations       | ingest / query / lint                          | same, codified in `operations.md`                     |
| Navigation index | `index.md`, content-oriented, per-ingest       | `map.md` plays this role (faithful)                   |
| Chronology       | `log.md`, append-only, `## [date] kind` prefix | same format and kinds (faithful)                      |
| Ownership        | LLM owns the wiki layer ("humans read")        | human-gated, reviewable, `advisor` review on HIGH     |
| Page shape       | dense entity pages (tools/people/themes)       | bounded topic/query/handoff/experiment pages          |
| Cross-linking    | heavy `[[wiki-links]]`, graph-meaningful       | sparse; navigation via registry tables                |
| Lint             | semantic (contradictions, stale, orphans)      | structural presence/marker check only                 |
| Trust model      | wiki = source of truth                         | wiki = derivative; raw repo sources = truth           |

## Divergence 1 — ownership: "humans read; LLMs write" is inverted

Karpathy's core rule is that the agent owns the wiki layer entirely and a single
ingested source touches 10–15 pages automatically. V2 instead gates writes
behind discipline: pages are "derivative and reviewable", carry status and
promotion touchpoints, and HIGH-risk work needs `advisor` review ("self-review
never counts"). V2 added a human gate exactly where Karpathy removed one.

## Divergence 2 — a structured research log, not an entity graph

Karpathy's wiki is Wikipedia-shaped: dense entity pages, heavy `[[ ]]`
cross-links, a meaningful Obsidian graph view. V2's surface is bounded pages per
question (topic/query/handoff/experiment/lint). Navigation and chronology are
faithful, but the dense concept graph is absent; an Obsidian graph view today
would be sparse.

## Divergence 3 — "lint" is narrower than the gist's

Karpathy's lint is *semantic* health: contradictions, stale claims, orphan
pages, missing cross-references. `research_wiki_lint.py` is a *structural*
presence check — required paths + required heading markers
(`REQUIRED_PATHS` / `REQUIRED_MARKERS`). It verifies the schema is intact, not
that the knowledge is consistent. The semantic lint remains a human/agent
judgment in `operations.md`, unmechanized. This is the largest open gap against
the gist.

## Compounding vs discipline

Karpathy's promise compounds because bookkeeping is free ("the tedious part is
not the reading, it's the bookkeeping"); low friction → high compounding. V2 has
the compounding *mechanism* (query answers filed back to `queries/**`) but
deliberately adds friction (status, source links, promotion touchpoints, log
entries). The data shows it: nearly all pages are dated `2026-06-04`/`06-08`.
The machinery exists; velocity is intentionally throttled by the discipline
gate. In a domain where a hallucinated "fact" turned authority could cost money,
this is a defensible velocity-for-auditability trade.

## Authority & lifecycle — the deepest, most deliberate divergence

For Karpathy the wiki *is* the knowledge base — what you query and trust instead
of re-deriving. In V2 the wiki is permanently locked into the **Research** role
of the `Research → Validate → Promote` lifecycle: "never runtime or promotion
authority", and load-bearing conclusions must be promoted out into `README.md`,
`docs/SKELETON_SCOPE.md`, tests, or `seed_manifest.json`. This inverts the trust
model: Karpathy compounds context *and* authority; V2 compounds context and
navigation only, and hands authority off elsewhere. It is consistent with
`patterns.md` Pattern 7 (absorb patterns that let a solo human mechanically
catch agent error; never let an external pattern become V2 authority).

## Optional next steps (research-only; not authority)

- ~~Mechanize a semantic-lint slice: orphan detection and broken intra-wiki link
  detection in `research_wiki_lint.py` (closes the biggest gist gap).~~ **Done
  2026-06-18** — `run_semantic_checks()` adds `orphan_pages` + `broken_links` on a
  warn-only `semantic_ok`. Scope note: orphan reachability is broad (any mention);
  broken-link detection targets markdown `[text](target.md)` links only, because the
  wiki's backtick navigation is filename-mention prose everywhere except the
  registries — and those are already validated by the referential check.
- Decide explicitly whether to grow a denser entity-page layer with real
  `[[wiki-links]]`, or to record that V2 intentionally rejects the entity-graph
  shape in favor of bounded question pages.

## Durable takeaways

- V2 borrowed Karpathy's form, not his motor; changes should target the motor
  (governance/authority) knowingly, not the form.
- The structural lint is not a semantic lint; do not read a green lint as
  "the knowledge is consistent".
- The wiki is derivative by contract; never let a query page become the place a
  load-bearing decision lives.

## Linked log entry

`docs/research/log.md` → `question | file back karpathy wiki fidelity review`

## Current status

Closed — the bounded comparison is captured; semantic-lint and entity-graph
questions are recorded as optional, non-blocking next steps.
