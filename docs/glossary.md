# Glossary — Genesis-Core-V2

> **Boundary note:** this is a navigation/definition surface. It points at the authoritative source
> for each term; it does not restate or override it. Where a definition here and its source disagree,
> the source wins. This page carries no runtime or promotion authority.

Repo-specific terms an agent meets early. Each row links to the single source of truth (SSOT) that
owns the term — read that, not a paraphrase.

| Term | Meaning (one line) | Authoritative source |
| --- | --- | --- |
| **admitted** | A surface explicitly carried into the seed as in-scope for V2. | [AGENTS.md](../AGENTS.md) Track A; [seed_manifest.json](../seed_manifest.json) (machine authority) |
| **deferred** | A surface not admitted into the seed; treat as out-of-scope until a validated slice admits it. | [AGENTS.md](../AGENTS.md) "Default" + Track B |
| **dormant** | Code admitted as package/import surface only — present and tested, but not rebound into runtime/server/execution paths. | [AGENTS.md](../AGENTS.md) Track A (Batch H2 transport, Batch I1 optimizer); per-subsystem `index.md` |
| **Track A / Track B** | A = skeleton-completeness work admissible now; B = authority-migration work deferred by default. | [AGENTS.md](../AGENTS.md) Track A / Track B |
| **RESEARCH / VALIDATE / PROMOTE** | The lifecycle: hypotheses → evidence → admitted authority. | [.github/copilot-instructions.md](../.github/copilot-instructions.md) Core Workflow; [AGENTS.md](../AGENTS.md) Lifecycle |
| **STRICT / RESEARCH / SANDBOX** | Governance modes resolved deterministically from override/branch/freeze. | [docs/governance_mode.md](governance_mode.md) (SSOT) |
| **champion freeze** | Window (through 2026-12-31) during which champion config is frozen; touching it fails closed to STRICT. | [docs/governance_mode.md](governance_mode.md) freeze escalation |
| **run-intent** | The declared purpose of a run (e.g. validate vs promote), gating premortem/promotion phases. | [src/core/strategy/run_intent.py](../src/core/strategy/run_intent.py); [src/core/strategy/index.md](../src/core/strategy/index.md) |
| **family / RI** | Strategy family; RI is the sole active family on runtime/config/champion/promotion surfaces. | [.github/copilot-instructions.md](../.github/copilot-instructions.md) Strategy Family Authority |
| **champion** | The verified, freeze-held BTC strategy subset; runtime falls back to `baseline:runtime_seed`. | [AGENTS.md](../AGENTS.md) Track A; [src/core/strategy/index.md](../src/core/strategy/index.md) |
| **premortem** | Deterministic, fail-closed post-validation risk reflection bound to evidence surfaces. | [docs/subsystem-index-and-premortem-convention.md](subsystem-index-and-premortem-convention.md) |

## Maintenance

- One row per term, one line of meaning, then the link. Do not grow definitions here — fix the SSOT.
- Add a term only when an agent would otherwise have to reverse-engineer it from code or chat.
- If a source moves, update the link here; the definition still lives there.
