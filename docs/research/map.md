# Research knowledge product map

> **Boundary note:** this page is a navigation and registry surface for `docs/research/**`.
> It helps humans and agents find durable context quickly.
> It is not a runtime-authority or promotion-authority surface.

Agents working against the research wiki should read this file first, then drill into the relevant
pages it points to.

## Purpose

Make the research knowledge product legible as V2 grows.
This page answers three questions quickly:

1. Which pages exist right now?
2. What state are they in?
3. Where should validated conclusions be promoted next?

## Product entrypoints

- `index.md` ÔÇö product contract, boundaries, invariants, and operating rules
- `patterns.md` ÔÇö research pattern registry for artifacts, experiments, handoffs, capability cards,
  evidence pipelines, evaluation records, and endpoint security checklists
- `log.md` ÔÇö append-only chronology for research-product updates and ingest moments
- `operations.md` ÔÇö ingest/query/lint workflow for the wiki
- `sources/index.md` ÔÇö raw-source layer contract and current source families
- `templates/topic-template.md` ÔÇö canonical starting shape for new topic pages
- `templates/artifact-template.md` ÔÇö canonical starting shape for artifact records
- `templates/experiment-template.md` ÔÇö canonical starting shape for experiment records
- `templates/evidence-pipeline-template.md` ÔÇö canonical starting shape for scan/review/evidence records
- `templates/evaluation-record-template.md` ÔÇö canonical starting shape for eval/perf/security records
- `templates/handoff-template.md` ÔÇö canonical starting shape for session handoff notes
- `templates/query-template.md` ÔÇö canonical starting shape for durable query answers
- `templates/lint-template.md` ÔÇö canonical starting shape for lint passes
- `templates/capability-card-template.md` ÔÇö canonical starting shape for bounded capability reviews
- `templates/endpoint-security-checklist-template.md` ÔÇö canonical starting shape for endpoint safety reviews

## Companion agent workflow

- `.github/skills/v2-research-review/SKILL.md` ÔÇö small repo-local review skill for bounded research
  wiki slices. Detailed guidance is in `references/**`; optional helper boundaries are in
  `scripts/**`; compatibility is explicit. Guidance only; not authority.

## Operational pattern surfaces

- `artifacts/index.md` ÔÇö contract for atomic runnable research artifacts inside repo bounds
- `experiments/index.md` ÔÇö contract for black-box experiment records inside repo bounds
- `handoffs/index.md` ÔÇö contract for session baton-pass notes inside repo bounds
- `queries/index.md` ÔÇö contract for filed-back query answers inside repo bounds
- `lint/index.md` ÔÇö contract for recorded health checks inside repo bounds

## Companion surfaces

| Surface                | Purpose                                           | Current state                            |
| ---------------------- | ------------------------------------------------- | ---------------------------------------- |
| `artifacts/index.md`   | inventory and rules for atomic runnable artifacts | scaffolded, no admitted artifacts yet    |
| `experiments/index.md` | inventory and rules for black-box experiments     | scaffolded, no admitted experiments yet  |
| `handoffs/index.md`    | inventory and rules for session baton-pass notes  | active, recovery handoff now tracked     |
| `queries/index.md`     | inventory and rules for filed-back query answers  | active, first filed answer now tracked   |
| `lint/index.md`        | inventory and rules for wiki health checks        | active, first recorded lint pass tracked |

## Current page registry

| Page                                                     | Type    | Status | Core question                                                                                            | Promotion touchpoints                                                                           |
| -------------------------------------------------------- | ------- | ------ | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `champion-results-review.md`                             | topic   | active | What is the current V2 meaning of the admitted champion subset and seed fallback contract?               | `README.md`, `docs/SKELETON_SCOPE.md`, `tests/governance/test_v2_seed_boundaries.py`            |
| `handoffs/2026-06-08-wiki-recovery.md`                   | handoff | closed | What was restored from the previously lost research-wiki slice, and where should future sessions resume? | `docs/research/log.md`, `README.md`, `docs/SKELETON_SCOPE.md`                                   |
| `queries/2026-06-04-karpathy-agent-discipline.md`        | query   | closed | What does Karpathy-style `llm-wiki` imply about agent discipline for V2 research work?                   | `docs/research/index.md`, `docs/research/operations.md`                                         |
| `queries/2026-06-04-nvidia-skills-cherry-pick-review.md` | query   | closed | Which NVIDIA skills patterns fit V2 without replacing the repo-native research wiki?                     | `docs/research/index.md`, `docs/research/patterns.md`, capability/artifact/experiment templates |
| `lint/2026-06-04-structure-health-check.md`              | lint    | closed | Is the fuller Karpathy-style research wiki shape structurally aligned and internally consistent?         | `docs/research/index.md`, `seed_manifest.json`, `tests/governance/test_v2_seed_boundaries.py`   |

## Page states

- `active` ÔÇö primary current research surface
- `watch` ÔÇö relevant and maintained, but not the main active review
- `closed` ÔÇö bounded question answered for now
- `superseded` ÔÇö preserved for history, replaced by a newer page or stronger contract surface

## Promotion path

1. Compile findings here from raw repo sources.
2. Validate behavior in tests, source seams, or other evidence surfaces.
3. Promote stable, load-bearing conclusions into admitted authority or verification surfaces such as:
   - `README.md`
   - `docs/SKELETON_SCOPE.md`
   - `seed_manifest.json`
   - focused tests

## Add a new topic page

1. Copy `templates/topic-template.md`.
2. Name the page after a bounded question or slice.
3. Register it in the table above with status and promotion touchpoints.
4. Append a dated entry to `log.md`.

## Add a new experiment record

1. Copy `templates/experiment-template.md`.
2. Keep one parameter family or experiment question per page.
3. Make evaluation surface, result, and linked log entry explicit.
4. Register the new record in `experiments/index.md`.

## Add an evaluation/performance record

1. Copy `templates/evaluation-record-template.md`.
2. Keep one bounded claim, candidate, or comparison per page.
3. Split candidate, baseline, quality signals, performance signals, result, and promotion decision.
4. Register the record in `experiments/index.md` unless a narrower index is added later.

## Add a new handoff

1. Copy `templates/handoff-template.md` into `handoffs/` using a dated, bounded filename.
2. Keep it short: what changed, current hypothesis, next steps, blockers.
3. Append a short chronology entry to `log.md` if the handoff changes repo understanding.
4. Promote durable findings into a topic page instead of leaving them stranded in the handoff.

## File back a query answer

1. Copy `templates/query-template.md`.
2. Record the question, consulted pages, and answer summary.
3. Capture any durable insight worth reusing in later sessions.
4. Register the new page in `queries/index.md` if it should remain part of the product.

## Run a lint pass

1. Use `operations.md` to decide the scope of the lint.
2. Optionally run `scripts/audit/research_wiki_lint.py` for structural checks.
3. Record the pass with `templates/lint-template.md` when the findings matter.
4. Promote important fixes into topic pages, map entries, or authority-adjacent docs as needed.

## Add a capability card

1. Copy `templates/capability-card-template.md`.
2. Keep one capability per page: agent skill, helper script, endpoint, workflow, or checklist.
3. Make scope IN/OUT, data/secret boundary, risks, mitigations, and validation evidence explicit.
4. Treat the card as research/validation planning only until a separate authority surface admits it.

## Add a scan/review/evidence pipeline

1. Copy `templates/evidence-pipeline-template.md`.
2. Keep one capability or artifact per evidence record.
3. Record scan result, review result, evidence marker, risks, limitations, and admission boundary.
4. Do not treat the evidence marker as NVIDIA signing or cryptographic signing.

## Run an endpoint security checklist

1. Copy `templates/endpoint-security-checklist-template.md`.
2. Name the trust boundary, allowed endpoints/tools, auth mode, and data classification.
3. Make deny-by-default egress, redaction, failure modes, and user-confirmation triggers explicit.
4. Treat the checklist as safety evidence only; do not use it to activate runtime/deployment surfaces.

## Which surface to use

- Need durable topic understanding? Use a topic page.
- Need quick chronology? Append to `log.md`.
- Need a pause/resume checkpoint for the next session? Use `templates/handoff-template.md`.
- Need a bounded parameter/evaluation/result/log loop? Use `templates/experiment-template.md`.
- Need scan/review/evidence before admission? Use `templates/evidence-pipeline-template.md`.
- Need eval/perf/security evidence with a baseline and promotion decision? Use `templates/evaluation-record-template.md`.
- Need to show one idea or seam end-to-end in a tiny runnable form? Follow `artifacts/index.md`.
- Need an answer to persist beyond chat? Use `templates/query-template.md`.
- Need to health-check the wiki itself? Use `templates/lint-template.md` and `lint/index.md`.
- Need to describe a bounded capability safely? Use `templates/capability-card-template.md`.
- Need to review an external endpoint, MCP, hosted model, or agent tool boundary? Use `templates/endpoint-security-checklist-template.md`.

## Maintenance notes

- Prefer updating a bounded existing page over opening overlapping pages.
- If a page becomes stale, move it to `watch`, `closed`, or `superseded` explicitly.
- Prefer links to authority surfaces over copying large payloads into markdown.
- Use `log.md` for chronology, `handoffs/**` for baton passes, and topic pages for durable understanding.
- Keep `map.md` content-oriented: it is the first file an agent should read when answering against the wiki.
