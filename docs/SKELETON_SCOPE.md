# Genesis-Core-V2 Skeleton Scope

## Current target

`Genesis-Core-V2` is intentionally a thin, runnable shell:

- minimal repo structure
- runtime pipeline orchestration via `src/core/pipeline.py`
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
- repo-local MCP launcher (`scripts/mcp/mcp_stdio.py`) for non-installed stdio startup
- repo-local API launcher (`scripts/api/api_shell.py`) for non-installed startup
- repo-local pytest launcher (`scripts/validate/pytest_suite.py`) for non-installed test execution
- repo-local smoke scripts (`scripts/smoke/*.py`) for non-installed execution
- `config/mcp_settings.json` and `mcp_server/**` for local MCP use
- local-only API shell (`config`, `info`, `status`, `models`, `strategy`)
- `src/core/pipeline.py` plus narrow deterministic seeding helper `src/core/utils/random_seeds.py`
- runtime determinism guardrails for pipeline fast-hash policy and feature-cache hash stability
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
- Local task loop: `genesis-v2: api shell`, `genesis-v2: mcp stdio`, `genesis-v2: smoke suite`, `genesis-v2: pytest`
- Local debug loop: `genesis-v2: api shell`, `genesis-v2: mcp stdio`, `genesis-v2: smoke suite`, `genesis-v2: pytest`
- Local editor settings: `python.analysis.extraPaths`, `python.testing.*`, `python.envFile`
- Local editor recommendations: `ms-python.python`, `ms-python.vscode-pylance`, `charliermarsh.ruff`
- Local pre-commit workflow: `pre-commit install`, then `pre-commit run --all-files`
- Local QA defaults: `pytest` recursion guards plus narrow `ruff`/`black` excludes in `pyproject.toml`
- Non-installed local MCP launcher: `python scripts/mcp/mcp_stdio.py`, optional config probe via `python scripts/mcp/mcp_stdio.py --print-config`
- Non-installed local API launcher: `python scripts/api/api_shell.py`, optional reload via `python scripts/api/api_shell.py --reload`
- Non-installed local pytest launcher: `python scripts/validate/pytest_suite.py`, optional focused run via `python scripts/validate/pytest_suite.py tests/runtime/test_local_api_shell_script.py -q`
- Non-installed local smoke scripts: `python scripts/smoke/fixture_smoke.py`, `python scripts/smoke/backtest_smoke.py`, `python scripts/smoke/champion_smoke.py`, `python scripts/smoke/evaluate_champion_smoke.py`, `python scripts/smoke/model_smoke.py`, `python scripts/smoke/smoke_suite.py`
- Installable local console scripts: `genesis-v2-api-shell`, `genesis-v2-mcp-stdio`, `genesis-v2-pytest`, `genesis-v2-champion-smoke`, `genesis-v2-evaluate-champion-smoke`, `genesis-v2-fixture-smoke`, `genesis-v2-backtest-smoke`, `genesis-v2-model-smoke`, `genesis-v2-smoke-suite`
- Installable console-script verification: `python -m pip install -e ".[dev,mcp]"`, then `pytest tests/runtime/test_installed_console_scripts.py -q`
- Editable-install module loop: `python -m uvicorn core.server:app --app-dir src --reload`, `python -m mcp_server.server`, `python -m pytest -q`
- Editable-install smoke module loop: `python -m core.bootstrap.model_smoke`, `python -m core.bootstrap.champion_smoke`, `python -m core.bootstrap.evaluate_champion_smoke`, `python -m core.bootstrap.fixture_smoke`, `python -m core.bootstrap.backtest_smoke`, `python -m core.bootstrap.smoke_suite`
- Optional local MCP install: `python -m pip install -e ".[mcp]"`
