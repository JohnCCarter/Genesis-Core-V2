# `docs/research/`

## Purpose

Provides the product-grade, repo-tracked research knowledge product for `Genesis-Core-V2`.
This folder is the repo-native LLM wiki: a plain-Markdown, Obsidian-friendly surface where humans
and agents can keep compiled context between sessions without turning chat history, ad hoc search,
or hidden retrieval into the source of truth.

`docs/research/**` is admitted as a product-grade, repo-tracked research knowledge product for durable human/agent context; it remains derivative, plain-Markdown, and non-authoritative.

## Product role

- durable cross-session context for bounded V2 questions
- navigation layer between raw evidence, open questions, and next validation steps
- repo-native knowledge product that can scale with V2 growth without adding hidden infrastructure
- derivative guidance surface only; never runtime or promotion authority

## Karpathy-style architecture mapping

Within V2, the research product maps the Karpathy LLM-wiki shape like this:

- raw sources ÔÇö repo-tracked docs, configs, tests, diagnostics, and code surfaces documented via
  `sources/index.md`; these are read, linked, and cited, but not rewritten as part of wiki
  maintenance
- the wiki ÔÇö compiled markdown under `docs/research/**`
- the schema ÔÇö this file plus repo-level guidance in `AGENTS.md` and
  `.github/copilot-instructions.md`, which together define structure, conventions, and workflow

Operationally:

- `index.md` acts as the local schema/contract
- `map.md` acts as the content-oriented index that agents should read first when working against
  the wiki
- `log.md` acts as the append-only chronology
- `operations.md` defines the ingest/query/lint loop

## Product surfaces

- `index.md` ÔÇö product contract, boundaries, and operating rules
- `map.md` ÔÇö navigation map, page registry, lifecycle states, and promotion path
- `log.md` ÔÇö append-only chronology of research-product updates and source-ingest moments
- `patterns.md` ÔÇö registry of admitted research patterns and when to use them
- `operations.md` ÔÇö Karpathy-style ingest/query/lint workflow for the research product
- `sources/index.md` ÔÇö raw-source layer contract and current source families
- `artifacts/index.md` ÔÇö contract for atomic runnable research artifacts within repo bounds
- `experiments/index.md` ÔÇö contract for black-box experiments and their bounded inventory
- `handoffs/index.md` ÔÇö contract for session handoff notes and baton-pass continuity
- `queries/index.md` ÔÇö filed-back query answers that should not disappear into chat history
- `lint/index.md` ÔÇö recorded health checks and lint passes over the wiki surface
- `templates/topic-template.md` ÔÇö canonical shape for new topic pages
- `templates/artifact-template.md` ÔÇö canonical shape for doc-first or runnable artifact records
- `templates/experiment-template.md` ÔÇö canonical shape for black-box experiments
- `templates/evidence-pipeline-template.md` ÔÇö canonical shape for scan/review/evidence records
- `templates/evaluation-record-template.md` ÔÇö canonical shape for eval/perf/security records
- `templates/handoff-template.md` ÔÇö canonical shape for next-session handoff notes
- `templates/query-template.md` ÔÇö canonical shape for durable filed-back query answers
- `templates/lint-template.md` ÔÇö canonical shape for wiki health-check records
- `templates/capability-card-template.md` ÔÇö canonical shape for bounded capability reviews
- `templates/endpoint-security-checklist-template.md` ÔÇö canonical shape for endpoint safety reviews
- topic pages such as `champion-results-review.md` ÔÇö bounded compiled pages for named questions

## Companion agent workflow

- `.github/skills/v2-research-review/SKILL.md` ÔÇö small repo-local review workflow for research-wiki
  slices. Details live in `.github/skills/v2-research-review/references/**`; optional helper
  boundaries live in `.github/skills/v2-research-review/scripts/**`; compatibility is explicit.
  It is guidance only and does not create runtime or promotion authority.

## Scope IN

- compiled research summaries derived from repo-tracked sources
- active review pages for bounded questions
- append-only research log entries
- product navigation and page templates that keep the knowledge surface maintainable as V2 grows
- atomic runnable artifact inventories and experiment records kept within repo bounds
- scan/review/evidence pipeline records for agent-facing capabilities before admission claims
- evaluation/performance records that make quality, performance, security, and comparison signals explicit
- bounded handoff notes for fast session continuity
- filed-back query answers and lint passes that keep the wiki compounding and healthy
- bounded capability cards that make agent/tool/workflow scope, risks, and validation explicit
- endpoint security checklists for external-service, MCP, hosted-model, or agent-tool boundaries
- links between evidence surfaces, open questions, and next validation steps

## Scope OUT

- runtime authority
- config/champion mutation by documentation alone
- opaque RAG/vector-store/database dependency as a precondition for use
- broad historical archive migration for its own sake
- raw source duplication when a link to the authority surface is enough

## Inputs

- repo-tracked docs, configs, diagnostics, and artifacts
- verified test/evidence outputs already present in the repository
- bounded user or agent research questions

## Outputs

- topic pages with current compiled understanding
- product navigation for current pages and lifecycle state
- experiment records with explicit parameter, evaluation, result, and log linkage
- scan/review/evidence records with explicit scan result, reviewer, evidence marker, risks,
  limitations, and admission boundary
- evaluation records with explicit candidate, baseline, quality/performance/security signals, and
  promotion decision
- handoff notes that preserve what changed, why it matters, and what comes next
- durable query answers that can be re-used by later sessions
- lint records that make contradictions, stale claims, and structural issues explicit
- capability cards that describe when a bounded capability may be used, what it must not do, and
  what evidence would be needed before promotion
- endpoint security checklists that document trust boundary, auth/secret handling, data boundary,
  egress controls, and validation evidence
- explicit source links and open questions
- append-only activity history in `log.md`

## Invariants

- raw repo sources remain the source of truth
- research pages are derivative and reviewable
- each topic page stays bounded to a named question or slice
- this folder remains plain Markdown and Obsidian-friendly; no RAG/database dependency is required
- page status, question, source surfaces, and next checks must stay explicit
- experiments must make parameter/evaluation/result/log explicit
- evidence pipeline records must make scan, review, evidence decision, risks, limitations, and
  admission boundary explicit
- evaluation records must split candidate, baseline, quality/performance/security signals, result,
  interpretation, and promotion decision
- capability cards must make scope, data/secret boundaries, allowed operations, risks, and
  validation evidence explicit
- endpoint security checklists must make trust boundary, auth/secret handling, data classification,
  egress controls, failure modes, and promotion gates explicit
- handoffs must stay short, dated, and baton-pass oriented rather than becoming a second wiki
- raw source surfaces remain immutable from the perspective of research ingest
- query answers that matter should be filed back into the wiki instead of staying chat-only
- session context must not become load-bearing; durable findings should be crystallized here

## Page states

- `active` ÔÇö currently driving research or reconciliation work
- `watch` ÔÇö still relevant, but not the main active review surface
- `closed` ÔÇö bounded question answered for now
- `superseded` ÔÇö preserved for history, replaced by a newer page or authority surface

## Minimum topic-page contract

- status/opened/working branch
- purpose
- review question
- source surfaces
- current compiled understanding
- verified findings or behavior
- tensions / open questions
- immediate next checks
- current status

## Continuity split

- topic pages carry durable, topic-level understanding
- `log.md` carries chronology and product-level change history
- handoff notes carry session continuity: what changed, what is believed, and what the next
  session should do
- experiment pages carry parameter/evaluation/result/log structure for bounded research or
  validation work

## Must Not

- claim runtime or promotion authority by itself
- silently override `README.md`, `docs/SKELETON_SCOPE.md`, tests, or config payloads
- accumulate stale notes without explicit status or next step
- turn into a generic scratchpad or dumping ground

## Current pages

- `map.md` ÔÇö knowledge-product navigation, lifecycle map, and page registry
- `log.md` ÔÇö append-only chronology for research-layer updates
- `patterns.md` ÔÇö adopted patterns for artifacts, experiments, handoffs, capability cards, and
  evidence pipelines
- `operations.md` ÔÇö ingest/query/lint workflow for the product
- `sources/index.md` ÔÇö raw-source layer index and immutability contract
- `artifacts/index.md` ÔÇö inventory/contract for atomic runnable artifacts
- `experiments/index.md` ÔÇö inventory/contract for black-box experiment records
- `handoffs/index.md` ÔÇö inventory/contract for session handoff notes
- `queries/index.md` ÔÇö inventory/contract for durable query answers
- `lint/index.md` ÔÇö inventory/contract for wiki health-check passes
- `champion-results-review.md` ÔÇö active compiled page for champion/evidence review

## Supporting pattern surfaces

- `patterns.md` ÔÇö operating patterns for artifacts, experiments, handoffs, and capability cards
- `operations.md` ÔÇö Karpathy-style ingest/query/lint loop
- `sources/index.md` ÔÇö source-of-truth layer and raw-source conventions
- `artifacts/index.md` ÔÇö home/base contract for atomic runnable research artifacts
- `experiments/index.md` ÔÇö home/base contract for black-box experiment records
- `handoffs/index.md` ÔÇö home/base contract for session baton-pass notes
- `queries/index.md` ÔÇö home/base contract for filed-back query answers
- `lint/index.md` ÔÇö home/base contract for lint passes and health checks
- `templates/topic-template.md` ÔÇö topic-page template
- `templates/artifact-template.md` ÔÇö artifact template
- `templates/experiment-template.md` ÔÇö experiment template
- `templates/evidence-pipeline-template.md` ÔÇö scan/review/evidence pipeline template
- `templates/evaluation-record-template.md` ÔÇö evaluation/performance record template
- `templates/handoff-template.md` ÔÇö handoff template
- `templates/query-template.md` ÔÇö query template
- `templates/lint-template.md` ÔÇö lint template
- `templates/capability-card-template.md` ÔÇö capability-card template
- `templates/endpoint-security-checklist-template.md` ÔÇö endpoint security checklist template

## Working pattern

1. Read source surfaces first.
2. Choose the right surface for the work:

- topic page for durable subject knowledge
- artifact record for a small whole-idea runnable or inspectable slice
- experiment record for parameter/evaluation/result/log work
- evidence pipeline for scan/review/evidence before an agent-facing capability is called admitted
- evaluation record for eval/perf/security evidence with explicit baseline and promotion decision
- handoff note for session baton-pass continuity
- query page for a durable answer worth filing back into the wiki
- lint page for a recorded health check over the current wiki state
- capability card for a bounded agent, tool, endpoint, or workflow capability that needs explicit
  scope, data boundary, risks, and validation path
- endpoint security checklist for external-service, MCP, hosted-model, or agent-tool trust boundaries

3. Update `map.md` when page state, scope, or promotion touchpoints change.
4. Append a short dated entry to `log.md`.
5. If a session stops mid-slice, capture a short structured handoff note rather than burying the
   next step inside a topic page.
6. Keep new questions linked back to source files.
7. Promote any load-bearing conclusion into admitted authority or verification surfaces separately.

## Governance boundaries

- Research pages may summarize and connect evidence.
- Validate remains the place where behavior is proven.
- Promote/authority decisions must still land in the admitted authority surfaces, not here.
- When a research conclusion becomes important enough to be load-bearing, promote it into
  `README.md`, `docs/SKELETON_SCOPE.md`, tests, manifest surfaces, or other admitted contracts.

## Lifecycle role / authority level

Research-only knowledge product. Durable context for humans and agents; never a runtime or
promotion authority surface.
