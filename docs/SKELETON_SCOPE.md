# Genesis-Core-V2 Skeleton Scope

## Current target

`Genesis-Core-V2` is intentionally a thin, runnable shell:

- minimal repo structure
- local-only API
- local MCP stdio shell
- generated workflow guidance for agent-driven work
- fixture-backed smoke tests
- no exchange, no UI, and no private runtime edges

`Genesis-Core` remains the source of truth until each slice is proven.

## Track A — skeleton completeness

Included in the current priority lane:

- README and local workflow docs
- `AGENTS.md`, `.github/copilot-instructions.md`, and `.pre-commit-config.yaml`
- `.vscode/mcp.json`, `.vscode/tasks.json`, `.vscode/launch.json`, `.vscode/settings.json`, and `.vscode/extensions.json` for local editor workflow
- tracked local env bootstrap template (`.env.example`) plus ignored local placeholder `.env`
- narrow local pytest/ruff/black defaults in `pyproject.toml`
- repo-local smoke scripts (`scripts/smoke/*.py`) for non-installed execution
- `config/mcp_settings.json` and `mcp_server/**` for local MCP use
- local-only API shell (`config`, `status`, `models`, `strategy`)
- fixture-backed smoke tests and console scripts
- explicitly admitted non-sensitive config/model artifacts already carried into the seed

## Track B — authority migration

Deferred to separate verified slices:

- strategy authority expansion
- config semantics and runtime authority
- backtest authority plus comparison/readiness surfaces
- remote MCP surfaces remain deferred (`mcp_server/remote_server.py`, remote-safe/git configs)
- exchange, paper, UI, and other private/live-adjacent edges
- freeze-sensitive surfaces

## Verification loop

- In `Genesis-Core`: `python -m pytest tests/utils/test_open_v2_runtime_seed.py -q`
- Regenerate the seed: `python scripts/extract/open_v2_runtime_seed.py --clean`
- In `Genesis-Core-V2`: `python -m pytest -q`
- Local task loop: `genesis-v2: api shell`, `genesis-v2: smoke suite`, `genesis-v2: pytest`
- Local debug loop: `genesis-v2: api shell`, `genesis-v2: smoke suite`, `genesis-v2: pytest`
- Local editor settings: `python.analysis.extraPaths`, `python.testing.*`, `python.envFile`
- Local editor recommendations: `ms-python.python`, `ms-python.vscode-pylance`, `charliermarsh.ruff`
- Local pre-commit workflow: `pre-commit install`, then `pre-commit run --all-files`
- Local QA defaults: `pytest` recursion guards plus narrow `ruff`/`black` excludes in `pyproject.toml`
- Non-installed local smoke scripts: `python scripts/smoke/fixture_smoke.py`, `python scripts/smoke/backtest_smoke.py`, `python scripts/smoke/smoke_suite.py`
- Optional local MCP install: `python -m pip install -e ".[mcp]"`
