# CLAUDE.md — Genesis-Core-V2

Claude Code operating rules for this repo. Domain rules live in [AGENTS.md](AGENTS.md) (operating
contract) and [.github/copilot-instructions.md](.github/copilot-instructions.md) (operating model:
Research → Validate → Promote, RI-first authority). This file owns **only** Claude-Code-specific
behavior; where a domain doc is more specific, it wins.

## Response banner

Begin every response with: `Mode: <MODE> (source=<resolution reason>)`

MODE follows the lifecycle (Research → Validate → Promote) resolved from the working branch/intent:

- research branches (e.g. `feature/research-candidate`) → **RESEARCH**
- validation slices / validate-intent work → **VALIDATE**
- promotion-facing work (champion / runtime authority) → **PROMOTE**

Cite the resolution reason, e.g. `Mode: RESEARCH (source=branch feature/research-candidate)`.

## Work thresholds

- **Tools/agents**: check this project's `MEMORY.md` first. Answer trivial questions directly. Try
  Read/Glob/Grep before escalating to Task/Explore. Never call a tool you don't need.
- **Subagents**: each subagent runs its own requests (token cost). Be deliberate — prefer inline
  Read/Glob/Grep for scoped lookups; reserve subagents for genuine broad/parallel fan-out. When a
  subagent is warranted for simple search or operational work, run it on Sonnet (Max) via the Agent
  `model:"sonnet"` + `effort:"max"` parameters and keep the main reasoning on the session model.
- **Plan mode**: skip for single-file/config/doc edits. Require for multi-file changes, new features,
  refactors, and pipeline/governance touches. When in doubt, ask.
- **Governance review**: LOW risk (docs, config, memory) → none. HIGH risk (behavior changes, pipeline,
  STRICT surfaces per AGENTS.md) → review via the `advisor` tool before merge. Self-review never counts.

## Session discipline

- **Bounded sessions**: reset at natural milestones (PR merged, experiment concluded, feature shipped,
  context > 60%). Don't compact indefinitely — start fresh.
- **State externalization**: before a milestone reset, overwrite the rolling handoff at
  `docs/research/handoff.md` (milestone, files changed, decisions, open questions, next-session primer).
  It is tracked and readable by any session/machine/agent — `.claude/` is machine-local and must not
  hold durable handoffs. The next session reads the artifact, not the history.
- **Output compression**: no trailing summaries, no "I've completed X" narration — show the result.
  One sentence per status update. Code comments only for non-obvious WHY.

## Scope & safety

- RESEARCH mode on research branches; no champion-config changes during the champion freeze; don't
  rebind dormant optimizer/transport surfaces; the run-trace is evidence-only and never issues
  promotion authority. See [AGENTS.md](AGENTS.md) Track A/B for the admitted boundary.
- Commit/push only when asked. Branch off `main` before committing if on it.
