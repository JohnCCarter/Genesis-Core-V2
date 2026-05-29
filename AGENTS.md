# AGENTS.md — Genesis-Core-V2 Skeleton Contract

## Purpose

`Genesis-Core-V2` is a generated, local-only skeleton repository.
`Genesis-Core` remains the source of truth until a slice is explicitly admitted and verified.

## Working rule

Prioritize V2 skeleton completeness before content migration.

## Track A — skeleton completeness

Use this track for:

- repo structure and generated workflow files
- local MCP stdio shell and safe editor hookup
- repo-local MCP launcher under `scripts/mcp/`
- repo-local API launcher under `scripts/api/`
- repo-local pytest launcher under `scripts/validate/`
- repo-local smoke scripts under `scripts/smoke/`
- local VS Code tasks, debug profiles, settings, and extension recommendations
- local-only API shell
- admitted strategy authority helpers (`family_registry`, `family_admission`, `authority_mode_resolver`, `run_intent`)
- admitted config/runtime authority semantics (`ConfigAuthority`, runtime schema, config API contract) without carrying runtime payloads
- fixture-backed smoke tests
- README/docs that explain the current admitted boundary
- local developer and agent workflow guidance

## Track B — authority migration

Defer these to separate verified slices:

- backtest authority, comparison, readiness, and promotion surfaces
- remote MCP exposure and remote Git workflow surfaces
- exchange, paper, UI, and other private/live-adjacent edges
- freeze-sensitive surfaces

## Change workflow

1. Change the generator in `Genesis-Core`.
2. Regenerate `Genesis-Core-V2`.
3. Run the focused generator regressions in `Genesis-Core`.
4. Run `pytest -q` in `Genesis-Core-V2`.
5. Commit only green, scoped slices.

## Default

If a surface is not explicitly admitted into the seed, treat it as deferred.
