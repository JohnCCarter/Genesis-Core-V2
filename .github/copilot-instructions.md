# Copilot Instructions — Genesis-Core-V2

## Genesis-Core-V2 Operating Model

Last update: 2026-06-01

## Mission

Genesis-Core-V2 exists to make research faster, validation stronger, and promotion safer.

Research fast.
Validate hard.
Promote rarely.

Genesis-Core-V2 is an evidence-first repository.

Governance supports reliable decisions; it is not an end in itself.

## Core Workflow

Research
↓
Validate
↓
Promote

Every feature, policy, strategy, experiment, and architectural decision should be traceable to one of these stages.

## Strategy Family Authority

Genesis-Core-V2 is an RI-first repository.

RI is the sole active strategy family on runtime, config-authority, champion-default, and promotion-facing surfaces.

Legacy is historical reference only.

Legacy may be retained for:

- historical comparison
- replay comparison
- audit purposes
- migration reference

Legacy must not act as:

- runtime authority
- promotion authority
- default admission target
- architectural authority

Future development should assume RI as the active strategy family unless explicitly approved otherwise.

## Research Lane

Research exists to discover.

Research should be lightweight, inexpensive, and fast.

Research outputs are evidence surfaces, not authority surfaces.

Research outputs are not runtime truth.

Research outputs are not promotion evidence until validated.

## Validation Lane

Validation exists to verify.

Validation determines whether research survives controlled testing.

Validation is intentionally more rigorous than research.

Validation determines credibility.

Validation does not automatically grant promotion authority.

## Promotion Lane

Promotion exists to protect runtime integrity.

Promotion determines whether a validated candidate becomes operational authority.

Promotion is intentionally rare.

Promotion requires evidence.

Promotion never occurs because an idea appears promising.

## Core Principles

- Evidence Over Opinion
- Validation Before Promotion
- Runtime Authority Must Be Earned
- Research Is Cheap
- Validation Is Expensive
- Promotion Is Rare
- Minimal Diffs
- Deterministic Runtime
- Security First

## Governance Philosophy

Governance supports:

Research
↓
Validate
↓
Promote

Process should always be proportional to risk.

Low-risk research should remain fast.

High-risk runtime changes should remain protected.

## Agent Philosophy

AI agents are collaborators.

AI agents may:

- research
- implement
- validate
- review

AI agents do not create authority.

Authority comes from evidence, validation, promotion decisions, and approved governance paths.

The binding agent epistemic principles — "Research should be easy, authority should be hard" and "Do not
choose convenience over validity" — live in `AGENTS.md` under "Agent epistemic principles".

The repo's research/audit tooling paths are non-authoritative (they may propose/evidence, not approve), and
`build_candidate_packet.py` is boundary-spanning (default output non-authoritative; explicit human override +
signoff is the authority path). See ADR 0003 (`docs/adr/0003-research-tooling-non-authoritative.md`) and
`seed_manifest.json` `research_tooling_surfaces`.

## Repository Philosophy

Genesis-Core-V2 prioritizes:

1. Faster research
2. Better validation
3. Safer promotion
4. Higher AI-agent effectiveness
5. Lower operational complexity
6. Clear repository structure

## Operating Rule

When uncertainty exists:

1. Research first.
2. Validate second.
3. Promote last.

Never reverse this order.

This operating model frames repository intent. Specific scope, safety, boundary, and verification rules below remain authoritative when they are more specific.

Read `AGENTS.md` and `docs/SKELETON_SCOPE.md` before widening scope.

## Default behavior

- Prefer the smallest admissible slice.
- Prioritize V2 evidence quality, runnable completeness, and repository clarity before widening scope.
- Keep `Genesis-Core` as historical reference and migration/audit source when useful; do not let it override admitted V2 authority surfaces without an explicit validated slice.
- Prefer generator-driven changes in `Genesis-Core` over manual drift in this repo.
- For admitted V2-scoped work, prefer direct, minimal changes in `Genesis-Core-V2`; avoid speculative cross-repo drift.
- Keep the local-only API shell runnable and tested.
- Keep the Batch E1 public candles endpoint semantics (`core.api.public`) bound only through the generated `core.server.get_exchange_client` surface.
- Keep the Batch E2 read-only account semantics (`core.api.account`) bound only through the generated `core.server.bfx_read` surface.
- Keep the Batch E3 local paper semantics (`core.api.paper`) limited to offline/local verification through generated `core.server` helper seams; do not treat it as live-ready transport admission.
- Keep the admitted Bitfinex transport family (`core.io.bitfinex.*`) dormant as package surface only; do not rebind it into server routes, startup wiring, or paper/live execution.
- Keep Batch G2 generated public/account route defaults bound only through `core.server.get_exchange_client` and `core.server.bfx_read` to that admitted REST read spine.
- Keep Batch H1 pure runtime decision/component/intelligence helper and composable-config admissions isolated from transport, optimizer, and runtime-authority widening.
- Keep Batch I1 dormant optimizer/package admissions (`core.optimizer.*`, `core.utils.optuna_helpers`, `core.utils.diffing.{config_equivalence,optuna_guard,trial_cache}`, `config/optimizer/**`) limited to import/test completeness only; do not admit execution roots, startup/server bindings, or runtime-authority payloads.
- Keep the admitted local UI shell (`core.api.ui`) aligned with admitted local endpoints only; do not expand it into deployment or live-ops claims.
- Keep the local MCP stdio shell local-first and safe by default.
- Keep the admitted strategy authority helpers (`core.config.authority_mode_resolver`, `core.strategy.family_registry`, `core.strategy.family_admission`, `core.strategy.run_intent`) runnable and tested.
- Keep the admitted config/runtime authority semantics (`core.config.authority`, `core.config.schema`, `core.api.config`) verification-only, with repo-tracked `config/runtime.seed.json` preserved read-only and local `config/runtime.json` still excluded from the seed.
- Keep the admitted Batch F verified champion subset (`config/strategy/champions/tBTCUSD_1h.json`, `config/strategy/champions/tBTCUSD_3h.json`) read-only; candidate/test/backup champion payloads remain deferred.
- Keep the admitted backtest comparison/diff semantics (`core.utils.diffing.results_diff`, `tools.compare_backtest_results`) tmp-path-isolated and out of execution-root expansion.
- Keep the admitted remote MCP semantics (`mcp_server.remote_server`, `config/mcp_settings.remote_{safe,git}.json`) limited to authorization, safe-mode, confirm-token, and transport-alias behavior already present in source.
- Prefer generated local `scripts/mcp/mcp_stdio.py` or `.vscode/mcp.json` for non-installed MCP startup.
- Prefer generated local `scripts/api/api_shell.py` or editor task/debug profiles for non-installed API startup.
- Prefer generated local `scripts/validate/pytest_suite.py` or editor task/debug profiles for non-installed pytest loops.
- Prefer generated local `scripts/smoke/*.py` wrappers or `python -m core.bootstrap...` commands for non-installed smoke loops.
- Prefer the generated local VS Code tasks, debug profiles, settings, and extension recommendations for repeatable API/smoke/test loops when working interactively.
- Prefer fixture-backed smoke tests before moving wider runtime content.

## Out of scope by default

- activation of the dormant Bitfinex transport family into server/startup/paper/live runtime paths
- remote MCP operational launchers, deployment/tunnel/proxy guidance, and other live-adjacent surfaces
- local runtime override payloads and non-authoritative champion payloads
- backtest execution roots, results corpora, promotion surfaces, and freeze-sensitive surfaces
- optimizer execution roots (`scripts/run/run_backtest.py`, `scripts/optimize/**`, preflight/validation CLIs), runtime-authority payload widening, and server/startup activation of the dormant optimizer package
- unverified content migration for its own sake
