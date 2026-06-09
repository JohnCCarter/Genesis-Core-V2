# Research patterns

> **Boundary note:** this page records admitted research patterns for `docs/research/**`.
> It captures useful working shapes for humans and agents, but it does not act as runtime or
> promotion authority by itself.

## Purpose

Turn useful working patterns into explicit repo-native defaults so V2 can grow without forcing each
session to rediscover how research should be structured.

These patterns cherry-pick the **shape** of useful external examples, not their code.

## Pattern 1 ÔÇö Atomic runnable artifacts

Use this when one small artifact can show the whole idea end-to-end.

Good fit:

- one seam
- one question
- one minimal runnable or inspectable artifact
- fast clarity for humans and agents

Preferred placement:

- runnable repo-bounded code under an admitted script surface such as `scripts/audit/` when code is warranted
- documentation-backed artifact records under `docs/research/artifacts/**`

Minimum contract:

- bounded question
- linked source surfaces
- how to run or inspect
- expected output or signal
- short result summary
- linked `log.md` entry

Must not:

- widen into runtime authority by itself
- sprawl into mini-frameworks
- smuggle experimental code into `src/core/**` without a separately validated reason

## Pattern 2 ÔÇö Black-box experiments

Use this when the goal is to test a bounded parameter or assumption with explicit evaluation.

Good fit:

- sensitivity checks
- threshold studies
- fixture-backed comparisons
- bounded research/validation probes

Minimum contract:

- parameter under test
- evaluation surface
- baseline or comparison point
- result summary
- linked `log.md` entry

Preferred placement:

- `docs/research/experiments/**` for recorded experiment pages
- bounded helper code only when the experiment genuinely needs it

Must not:

- pretend to be promotion evidence by default
- expand into optimizer/edge hunting for trading alpha
- hide parameter/evaluation/result logic across many disconnected files

## Pattern 3 ÔÇö Agent handoff and log

Use this when the next session needs to understand not only what changed, but what the current
thinking is and what should happen next.

Role split:

- `log.md` ÔÇö chronology and research-product change history
- `handoffs/**` ÔÇö session baton-pass notes
- topic pages ÔÇö durable subject understanding

Minimum handoff contract:

- why this handoff exists
- what changed
- current understanding or hypothesis
- next steps
- blockers or open questions

Must not:

- become a second wiki
- carry authority claims
- store durable conclusions that belong in topic pages or tests

## Pattern 4 ÔÇö Capability cards

Use this when a potential agent skill, helper script, endpoint, workflow, or checklist needs a
clear operating contract before it is used broadly.

Good fit:

- external skill patterns adapted into V2-native form
- capability reviews that need explicit data/secret boundaries
- workflows that may later need validation or promotion but are still research-only today
- reusable agent/tool guidance that should not stay buried in chat

Minimum contract:

- owner and maintainer
- purpose and trigger
- scope IN and scope OUT
- expected outputs
- version and provenance
- source surfaces and dependencies
- secret/data boundary
- allowed operations
- known risks and mitigations
- limitations
- scan/review/evidence state
- validation evidence and promotion path
- linked `log.md` entry

Preferred placement:

- start from `docs/research/templates/capability-card-template.md`
- store concrete cards under a bounded research surface when the first capability is admitted

Must not:

- import external runtime stacks just because a capability card exists
- claim runtime or promotion authority by itself
- bypass tests, manifest updates, or authority-surface promotion when a capability becomes load-bearing

## Pattern 4a ÔÇö Scan-review-evidence pipeline

Use this when an agent-facing capability needs explicit evidence before it can be called admitted.
This borrows the trust-pipeline shape without adopting NVIDIA signing or external attestation.

Minimum contract:

- capability or artifact under review
- scan stage
- review stage
- evidence decision stage
- risk and limitation register
- admission boundary
- linked `log.md` entry

Preferred placement:

- start from `docs/research/templates/evidence-pipeline-template.md`
- link the concrete record from the relevant capability card

Must not:

- imply cryptographic signing unless a separate validated slice explicitly admits it
- mark a capability as runtime- or promotion-admitted by research evidence alone
- skip reviewer, risks, limitations, or failed-scan details

## Pattern 5 ÔÇö Evaluation and performance records

Use this when a bounded claim needs explicit evaluation evidence, especially when adapting external
patterns such as RAG eval/perf vocabulary without importing the runtime stack.

Good fit:

- quality, regression, safety, or performance checks
- candidate-versus-baseline comparisons
- hosted-model helper or research-tool behavior checks
- no-runtime retrieval-lens experiments over the wiki

Minimum contract:

- evaluation question
- candidate under review
- baseline or comparison
- source surfaces and fixtures
- artifact layout
- quality signals
- performance signals
- summary table
- failure table
- security/data boundary
- result summary and interpretation
- validation evidence
- promotion decision

Preferred placement:

- start from `docs/research/templates/evaluation-record-template.md`
- register concrete records in `docs/research/experiments/index.md` until a narrower index exists

Must not:

- replace source-of-truth wiki pages with hidden retrieval outputs
- treat promising metrics as promotion by default
- hide baselines, thresholds, or data boundaries

## Pattern 6 ÔÇö Endpoint security checklists

Use this when a capability touches hosted APIs, MCP, exchange endpoints, browser/tooling surfaces, or
other agent-accessible trust boundaries.

Good fit:

- NVIDIA NIM or other hosted-model endpoint reviews
- MCP tool or remote-server safety reviews
- external service probes kept in research/validation lanes
- future agent-tool capabilities that need deny-by-default egress and data-boundary clarity

Minimum contract:

- trust boundary
- endpoint trust confirmation
- intended use and scope OUT
- endpoint inventory
- auth and secret handling
- no secrets in prompts
- data classification
- egress and endpoint controls
- path/method scoped external calls
- prompt/tool boundary
- logging and redaction rules
- failure modes
- validation evidence and promotion gates

Preferred placement:

- start from `docs/research/templates/endpoint-security-checklist-template.md`
- keep concrete checklists in a bounded research surface unless a narrower index is admitted later

Must not:

- store secrets or non-redacted private data
- authorize deployment, live/private trading, or remote operations by checklist alone
- widen runtime/startup/server bindings without a separate validated slice
