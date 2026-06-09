# NVIDIA skills cherry-pick review

> **Boundary note:** this is a durable query-answer record.
> It preserves a bounded answer for later sessions, but it does not act as runtime or promotion
> authority.

Date: 2026-06-04
Working branch: `feature/champion-results-review`
Knowledge product links: `../index.md` ┬À `../map.md` ┬À `../log.md`

## Question

Which parts of `https://github.com/NVIDIA/skills` are worth cherry-picking into
`Genesis-Core-V2`, and do they conflict with the existing Karpathy-style LLM wiki?

## Why this answer should persist

The NVIDIA skills catalog is broad and operationally heavy. V2 needs a stable decision record so
future sessions do not re-propose a full RAG/AI-Q/NemoClaw deployment when the current repository
boundary only admits a plain-Markdown, non-authoritative research knowledge product.

## Consulted surfaces

- `docs/research/index.md`
- `docs/research/map.md`
- `docs/research/operations.md`
- `docs/SKELETON_SCOPE.md`
- `AGENTS.md`
- `https://github.com/NVIDIA/skills`
- `https://docs.nvidia.com/skills`
- `https://agentskills.io/specification`
- `https://github.com/NVIDIA/skills/blob/main/docs/scanning-agent-skills.mdx`
- `https://github.com/NVIDIA/skills/blob/main/docs/signing-agent-skills.mdx`
- `https://github.com/NVIDIA/skills/blob/main/docs/skill-cards.mdx`
- `https://github.com/NVIDIA/skills/blob/main/docs/advanced-install.mdx`
- `skills/rag-blueprint/SKILL.md` from a temporary read-only clone of `NVIDIA/skills`
- `skills/rag-eval/SKILL.md` from a temporary read-only clone of `NVIDIA/skills`
- `skills/rag-perf/SKILL.md` from a temporary read-only clone of `NVIDIA/skills`
- `skills/aiq-research/SKILL.md` from a temporary read-only clone of `NVIDIA/skills`
- `skills/nemo-retriever/SKILL.md` from a temporary read-only clone of `NVIDIA/skills`
- `skills/skill-card-generator/SKILL.md` from a temporary read-only clone of `NVIDIA/skills`
- `skills/nemoclaw-user-configure-security/references/best-practices.md` from a temporary
  read-only clone of `NVIDIA/skills`

## Answer summary

The highest-value cherry-pick is not the NVIDIA RAG runtime itself. V2 should keep the
Karpathy-style wiki as the source-of-truth knowledge surface and cherry-pick lightweight patterns
around skill governance, evaluation records, retrieval experiment design, security boundaries, and
progressive-disclosure packaging.

Recommended order:

1. Cherry-pick NVIDIA's skill trust pipeline pattern as V2 research-artifact metadata: skill card,
   scan/review evidence, version/provenance, and explicit risks.
2. Cherry-pick the RAG `eval` / `perf` separation as experiment-record vocabulary, not as a
   deployed RAG dependency.
3. Cherry-pick NemoClaw-style security rules for any future agent/external endpoint work:
   deny-by-default egress, endpoint trust confirmation, no secrets in prompts, and path/method
   scoped external calls.
4. Cherry-pick Agent Skills progressive-disclosure structure if V2 later adds repo-local custom
   skills: small `SKILL.md`, deeper `references/**`, optional `scripts/**`, explicit compatibility.
5. Treat AI-Q, RAG Blueprint, NeMo Retriever, Dynamo, VSS, and deployment-heavy skills as deferred
   reference material unless a separate validated slice explicitly admits external services.

## Durable takeaways

- NVIDIA RAG Blueprint does not have to conflict with the LLM wiki, but it would conflict if it
  became a required hidden retrieval dependency or a second source of truth.
- `docs/research/**` should remain plain Markdown, Obsidian-friendly, derivative, and
  non-authoritative.
- If RAG is explored later, it should index/export from the wiki as a read-only retrieval lens, not
  replace or mutate the wiki.
- `rag-eval` and `rag-perf` are more useful to V2 as naming and artifact patterns than as copied
  code today.
- NVIDIA's strongest portable lesson for V2 is capability governance: every agent-facing capability
  should have clear owner, intended use, risks, evidence, version, and verification notes.

## Linked log entry

See `docs/research/log.md` entry `2026-06-04 question | file back NVIDIA skills cherry-pick review`.

## Current status

Closed for current research planning. The first V2-native adaptations now cover capability cards,
scan/review/evidence pipeline records, evaluation/performance records, endpoint security checklists,
and a progressive-disclosure repo-local research-review skill without importing NVIDIA runtime stacks.
