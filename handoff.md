# Genesis-Core-V2 handoff

Date: 2026-06-01

## Current repo state

- Repo path: `C:\Users\fa06662\Projects\Genesis-Core-V2`
- Branch: `main`
- Local baseline commit: `cee1f25` — `seed: lock verified runtime-first baseline`
- Worktree status at latest acceptance check: clean
- Source-of-truth repo for generator-driven widening: `Genesis-Core`

## Acceptance already completed

The following acceptance pass was rerun against `cee1f25` and passed:

1. Full test suite
   - `python -m pytest -q`
   - Result: passed
2. Smoke suite
   - `python scripts/smoke/smoke_suite.py`
   - Result: passed
3. API startup + health probe
   - `python -m uvicorn core.server:app --app-dir src --host 127.0.0.1 --port 8012`
   - `GET /health`
   - Result: `200 OK` with `{"status":"ok", ...}`

Known non-blocking output:

- Optuna `ExperimentalWarning` warnings in optimizer-related tests
- No failing tests in the latest acceptance pass

## What this repository is

`Genesis-Core-V2` is a **skeleton-first, runtime-first local seed**.
It is intentionally narrower than `Genesis-Core`.

It is ready for real work, but changes should still respect the admitted boundary recorded in the repo docs and manifest.

## Start-here files for the next agent

Read these first, in this order:

1. `AGENTS.md`
   - high-level skeleton contract
   - Track A vs Track B boundaries
   - change workflow and default defer rules
2. `.github/copilot-instructions.md`
   - concrete working rules for what must stay admitted, dormant, excluded, or verification-only
3. `docs/SKELETON_SCOPE.md`
   - current admitted scope
   - verification loop
   - explicit deferred surfaces
4. `README.md`
   - practical repo summary
   - included vs excluded surfaces
   - local commands and workflow surfaces
5. `seed_manifest.json`
   - machine-readable inventory of admitted files, generated files, verification surfaces, and exclusions

## Other markdown files in the repo

### Operational / relevant

- `config/optimizer/README.md`
  - context for admitted read-only optimizer corpus
- `config/optimizer/3h/phased_v3/PHASED_V3_RESULTS.md`
  - optimizer research artifact carried in the admitted config corpus
- `config/optimizer/6h/PHASED_NORMALIZATION_PLAN.md`
  - optimizer research/plan artifact carried in the admitted config corpus

### Ignore for decision-making

- `.pytest_cache/README.md`
  - cache metadata, not an authoritative project document

## Practical rules for new work

- Treat `cee1f25` as the stable local baseline.
- Prefer the **smallest admissible slice**.
- Do not reopen the migration without a specific reason.
- Prefer generator-driven widening in `Genesis-Core` over manual drift in V2 when a slice is not already admitted.
- Keep the local API shell runnable and tested.
- Keep dormant transport and dormant optimizer surfaces dormant unless a new verified slice explicitly widens them.
- Keep runtime/config authority semantics verification-only unless a new governed slice explicitly changes that.

## What is already admitted

High-value admitted surfaces include:

- runtime pipeline + backtest kernel
- local API shell (`account`, `config`, `info`, `models`, `paper`, `public`, `status`, `strategy`, `ui`)
- Bitfinex REST read spine
- dormant transport-family package surface
- pure runtime decision/component/intelligence helpers
- dormant optimizer package + read-only `config/optimizer/**` corpus
- verified BTC champion subset
- fixture-backed smoke infrastructure
- local VS Code workflow files
- local MCP stdio shell
- constrained remote MCP semantics (verification-only)

Use `README.md`, `docs/SKELETON_SCOPE.md`, and `seed_manifest.json` for exact file-level truth.

## What is still deferred by default

Examples of still-deferred surfaces:

- live/private execution rebinding of dormant Bitfinex transport surfaces
- optimizer execution roots (`scripts/run/run_backtest.py`, `scripts/optimize/**`, preflight/validation CLIs)
- local `config/runtime.json`
- non-authoritative champion payloads and backups/candidates
- remote MCP deployment/launcher/tunnel/proxy guidance
- broad historical docs/research migration for its own sake

## Good starting commands

### Full validation

- `python -m pytest -q`
- `python scripts/smoke/smoke_suite.py`

### API

- `python scripts/api/api_shell.py --reload`
- or `python -m uvicorn core.server:app --app-dir src --reload`

### Local pytest wrapper

- `python scripts/validate/pytest_suite.py`

### MCP stdio

- `python scripts/mcp/mcp_stdio.py`

## Recommended first move for the next agent

1. Read `AGENTS.md`, `.github/copilot-instructions.md`, `docs/SKELETON_SCOPE.md`, and `README.md`.
2. Inspect `seed_manifest.json` for exact admitted/deferred boundaries.
3. Confirm the requested change belongs inside already admitted V2 scope.
4. If it does, implement the smallest slice directly in V2.
5. If it does not, widen via the generator path in `Genesis-Core` first.

## Short prompt for the next V2 chat

Use this if you want to bootstrap the next agent quickly:

> We are now working in `Genesis-Core-V2` at `C:\Users\fa06662\Projects\Genesis-Core-V2`.
> Baseline commit is `cee1f25` (`seed: lock verified runtime-first baseline`) and latest acceptance already passed: full `pytest -q`, `scripts/smoke/smoke_suite.py`, and API `/health`.
> Read `AGENTS.md`, `.github/copilot-instructions.md`, `docs/SKELETON_SCOPE.md`, `README.md`, and `seed_manifest.json` first.
> Treat V2 as the active core repo, keep changes inside admitted scope unless explicitly widening through `Genesis-Core`, and continue with the smallest admissible slice.
