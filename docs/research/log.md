# Research log

> **Boundary note:** this file is an append-only chronology for `docs/research/`.
> It records research-layer updates and source-ingest moments.
> It is not a runtime-authority surface.

## Entry format

Use:

`## [YYYY-MM-DD] kind | short title`

Suggested kinds:

- `bootstrap`
- `ingest`
- `update`
- `lint`
- `question`
- `close`

## [2026-06-04] bootstrap | initialize research knowledge layer

- Created `docs/research/index.md` as the bounded research knowledge-layer contract.
- Created `docs/research/champion-results-review.md` as the first active topic page.
- Seeded the page with current evidence links for:
  - `config/strategy/champions/tBTCUSD_1h.json`
  - `config/strategy/champions/tBTCUSD_3h.json`
  - `config/optimizer/3h/phased_v3/PHASED_V3_RESULTS.md`
  - `artifacts/diagnostics/v2_gap_audit_2026-06-01.md`
- Intent: keep champion-results review durable, repo-tracked, and non-load-bearing for future
  agent sessions.

## [2026-06-04] ingest | verify champion loader fallback semantics

- Read and linked the current loader implementation in `src/core/strategy/champion_loader.py`.
- Confirmed via `tests/runtime/test_stateful_authority_payloads.py` that both tracked champion
  files currently resolve to `baseline:runtime_seed` at runtime.
- Confirmed via `tests/governance/test_v2_seed_boundaries.py` that the repo contract explicitly
  treats the tracked subset as demoted while seed fallback remains active.
- Updated `docs/research/champion-results-review.md` with a source-backed finding so future
  sessions do not need to rediscover this seam from scratch.

## [2026-06-04] update | reconcile current champion authority wording

- Reconciled `README.md` and `docs/SKELETON_SCOPE.md` around the current champion/runtime
  authority contract.
- Added one compact statement clarifying that the tracked champion subset is admitted and
  evidence-bearing, but demoted for runtime authority.
- Kept the existing Batch F wording intact while making the runtime-active fallback behavior more
  explicit for human readers and future agents.
- Updated `docs/research/champion-results-review.md` so the research layer reflects the new repo
  wording.

## [2026-06-04] update | productize research knowledge layer

- Elevated `docs/research/**` from a minimal knowledge layer to a first-class, repo-tracked
  knowledge product for V2 growth.
- Added `docs/research/map.md` as the navigation/registry surface and
  `docs/research/templates/topic-template.md` as the canonical topic-page template.
- Anchored the product in `README.md`, `docs/SKELETON_SCOPE.md`, `seed_manifest.json`, and
  `tests/governance/test_v2_seed_boundaries.py`.
- Kept the product plain-Markdown, Obsidian-friendly, and explicitly non-authoritative.

## [2026-06-04] update | admit research patterns fully

- Added explicit product surfaces for three admitted research patterns:
  - atomic runnable artifacts
  - black-box experiments
  - agent handoff/log continuity
- Added new templates for experiment and handoff notes plus an artifact contract surface.
- Updated `index.md`, `map.md`, `seed_manifest.json`, and governance coverage so these patterns
  are now first-class within the research knowledge product.

## [2026-06-04] update | align product to full karpathy llm-wiki shape

- Clarified the Karpathy-style three-layer mapping inside `docs/research/index.md`:
  raw sources, wiki, and schema.
- Added explicit source, query, and lint surfaces plus `operations.md` for the ingest/query/lint
  loop.
- Added durable query and lint templates plus a structural lint script entrypoint for the research
  wiki.
- Extended manifest/test coverage so the fuller schema/index/log/operations shape is now tracked in
  repo contract surfaces.

## [2026-06-04] question | file back karpathy agent discipline answer

- Added `docs/research/queries/2026-06-04-karpathy-agent-discipline.md` as the first durable
  query-answer page in the product.
- Captured the repo-facing implication of Karpathy-style agent discipline:
  schema/index/log structure, durable artifacts, and explicit ingest/query/lint workflow.
- Registered the query page in `map.md` so later sessions can reuse it without depending on chat
  history.

## [2026-06-04] lint | run first research wiki structure health check

- Ran `python scripts/audit/research_wiki_lint.py` after the fuller Karpathy-style wiki alignment.
- Confirmed zero missing paths and zero missing markers across the current schema/index/log and
  support surfaces.
- Recorded the first lint pass in `docs/research/lint/2026-06-04-structure-health-check.md`.

## [2026-06-04] question | file back NVIDIA skills cherry-pick review

- Reviewed `NVIDIA/skills` against the current V2 research-wiki and scope boundaries.
- Captured the conclusion that V2 should cherry-pick lightweight governance, evaluation,
  performance, and security patterns before considering any RAG/AI-Q deployment slice.
- Added `docs/research/queries/2026-06-04-nvidia-skills-cherry-pick-review.md` so later
  sessions can reuse the decision without relying on chat history.

## [2026-06-04] update | add V2 capability card template

- Added `docs/research/templates/capability-card-template.md` as the first V2-native adaptation
  from the NVIDIA skills audit.
- Registered capability cards as a research-only pattern for describing bounded agent, tool,
  endpoint, workflow, or checklist capabilities.
- Kept the card explicitly non-authoritative: it documents scope, risks, boundaries, validation,
  and promotion path without importing external runtime stacks.

## [2026-06-04] update | add V2 eval and endpoint security templates

- Added `docs/research/templates/evaluation-record-template.md` to capture eval/perf/security
  evidence with candidate, baseline, signals, result, interpretation, and promotion decision.
- Added `docs/research/templates/endpoint-security-checklist-template.md` to capture endpoint,
  MCP, hosted-model, and agent-tool trust boundaries with deny-by-default safety assumptions.
- Registered both as V2-native adaptations of NVIDIA skill patterns without adding RAG, AI-Q,
  NeMo, deployment, or runtime dependencies.

## [2026-06-04] update | add repo-local V2 research review skill

- Added `.github/skills/v2-research-review/SKILL.md` as a project-local agent skill for bounded
  research-wiki reviews.
- The skill points agents toward capability cards, evaluation records, endpoint security
  checklists, and existing wiki templates while preserving Research -> Validate -> Promote order.
- Kept the skill as guidance only; it does not create runtime, config, transport, deployment, or
  promotion authority.

## [2026-06-04] update | tighten NVIDIA pattern adaptations

- Added `docs/research/templates/evidence-pipeline-template.md` for scan -> review -> evidence
  records without NVIDIA signing or external attestation.
- Tightened capability cards with owner, purpose, risks, outputs, version/provenance, evidence,
  limitations, and scan/review/evidence state.
- Tightened eval/perf records with artifact layout, summary table, and failure table.
- Tightened endpoint security checklists with endpoint trust confirmation, no-secrets-in-prompts,
  deny-by-default egress, and path/method scoped external calls.
- Split `.github/skills/v2-research-review` into small `SKILL.md`, detailed `references/**`,
  explicit `scripts/**` boundary, and compatibility notes.

## [2026-06-08] update | restore research wiki and ecosystem inventory docs

- Restored `docs/agent-ecosystem-inventory.md` into the repo from the recoverable historical PR #2
  content.
- Restored the broader Karpathy-style research wiki under `docs/research/**` from local
  unreachable commit evidence.
- Restored `scripts/audit/research_wiki_lint.py` and
  `tests/runtime/test_local_research_wiki_lint_script.py` so the recovered wiki has a repo-local
  structural verification loop again.
- Ran the recovered wiki lint and focused test successfully before removing temporary forensic
  recovery artifacts.
- Added a dated handoff note so future sessions can start from the restored wiki rather than repeat
  transcript/PR archaeology.
