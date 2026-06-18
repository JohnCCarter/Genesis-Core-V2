# `mcp_server/`

> Verification-only boundary surface. This page exists so agents do not accidentally widen the MCP
> tool surface. It frames the current admitted boundary; it does not authorize activation.

## Purpose

Holds the admitted, constrained MCP server semantics for V2 — authorization, safe-mode, confirm-token,
and transport-alias behavior — as a read/verification surface only. The local stdio shell lives in
[scripts/mcp/](../scripts/mcp/); this package is the server-side contract those tests exercise.

## Scope IN

- read/verification MCP semantics already admitted in the seed
- authorization, safe-mode, and confirm-token enforcement
- transport-alias (SSE) behavior verified offline in tests

## Scope OUT

- operational launchers, tunnels, proxies, or deployment/hosting guidance (Track B, deferred)
- adding new tools without a `seed_manifest.json` declaration and an authorization test
- any write/execution authority beyond the admitted constrained semantics
- widening the MCP surface into runtime/champion/transport activation

## Inputs

- MCP client tool calls routed through the server
- remote safe/git config (`config/mcp_settings.remote_safe.json`, `config/mcp_settings.remote_git.json`)

## Outputs

- authorized read/verification responses
- confirm-token-gated git workflow results
- authorization/transport behavior verified in tests

## Invariants

- the MCP tool surface stays read/verification by default
- every new tool is declared in [seed_manifest.json](../seed_manifest.json) and covered by an authorization test
- auth-required / safe-mode / confirm-token semantics are preserved, never bypassed

## Must Not

- ship operational launchers, deployment, or tunnel/proxy guidance
- admit a tool that is undeclared in the seed or untested for authorization
- treat this surface as live runtime/transport authority

## Related tests

- `tests/governance/test_mcp_remote_authorization.py`
- `tests/integration/test_mcp_git_status_remote_filters.py`
- `tests/integration/test_mcp_remote_git_workflow_confirm.py`
- `tests/utils/test_remote_server_fastmcp_sse_alias.py`
- `tests/runtime/test_local_mcp_script.py`
- `tests/runtime/test_local_mcp_setup.py`

## Governance boundaries

- Admission is limited to constrained read/verification semantics already verified in the seed
  ([AGENTS.md](../AGENTS.md) Track A; [docs/agent-ecosystem-inventory.md](../docs/agent-ecosystem-inventory.md) §3.6).
- Operational/deployment widening remains deferred (Track B).

## Lifecycle role / authority level

Verification-only surface: admitted constrained MCP semantics with no operational or runtime authority.
