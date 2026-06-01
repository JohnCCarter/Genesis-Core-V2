# AGENTS.md — Genesis-Core-V2 Operating Contract

## Purpose

`Genesis-Core-V2` is an RI-first, evidence-first, local-first repository.

`Genesis-Core` may still be used as historical, migration, and audit reference when a slice
explicitly requires that path, but it does not override admitted V2 authority surfaces by default.

## Working rule

Prioritize V2 skeleton completeness before content migration.

## Lifecycle

Genesis-Core-V2 runs on three lifecycle stages:

1. Research
2. Validate
3. Promote

Promotion should only happen after validated evidence.

Track A and Track B below remain the compatibility map for seed/governance boundaries.

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
- Batch E1 public candles endpoint semantics via injected exchange-client verification
- Batch E2 read-only account endpoint semantics via injected read-helper verification
- Batch E3 local paper and UI semantics via injected helper verification while broader transport stays deferred
- Batch G1 Bitfinex REST read spine via direct module verification
- Batch G2 generated public/account route defaults bound through `core.server` to the admitted REST read spine only
- Batch H1 pure runtime decision/component/intelligence helpers plus repo-tracked composable strategy configs/tests
- Batch H2 dormant Bitfinex transport family admission without server/startup/paper-live rebinding
- Batch I1 dormant optimizer package/diffing utility admission plus repo-tracked `config/optimizer/**` research corpus without execution-root or runtime-authority widening
- Batch F repo-tracked runtime seed baseline plus the verified BTC champion subset while local runtime override and candidate/test/backup champions stay deferred
- admitted strategy authority helpers (`family_registry`, `family_admission`, `authority_mode_resolver`, `run_intent`)
- admitted config/runtime authority semantics (`ConfigAuthority`, runtime schema, config API contract) with repo-tracked `config/runtime.seed.json` while local `config/runtime.json` remains excluded
- admitted backtest comparison/diff semantics (`results_diff`, compare/parity tooling) without carrying execution roots or results corpora
- admitted constrained remote MCP semantics (`remote_server`, remote safe/git configs, auth/confirm/transport tests) without operational launchers or deployment guidance
- fixture-backed smoke tests
- README/docs that explain the current admitted boundary
- local developer and agent workflow guidance

## Track B — authority migration

Defer these to separate verified slices:

- remote MCP operational launchers and deployment/tunnel/proxy guidance
- activation/rebinding of the dormant Bitfinex transport family and other live-adjacent/private execution edges
- optimizer execution roots (`scripts/run/run_backtest.py`, `scripts/optimize/**`, preflight/validation CLIs) and any server/startup activation of the dormant optimizer package
- non-authoritative champion payloads and other freeze-sensitive surfaces

## Change workflow

1. Define a bounded V2 slice (scope IN/OUT).
2. Apply minimal changes directly in `Genesis-Core-V2` for V2-scoped work.
3. Use `Genesis-Core` source refresh only when the slice explicitly depends on generator/seed regeneration.
4. Run the relevant focused checks and `pytest -q` in `Genesis-Core-V2`.
5. Commit only green, scoped slices with traceable evidence.

## Default

If a surface is not explicitly admitted into the seed, treat it as deferred.
