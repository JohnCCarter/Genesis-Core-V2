# `src/core/api/`

## Purpose

Provides the admitted local-only API shell for runtime visibility, constrained config/account/public
seams, and local paper/UI verification surfaces.

## Scope IN

- local-only API routes
- public candles semantics through injected exchange client seam
- read-only account semantics through injected read-helper seam
- local config/status/info/models/strategy/paper/ui endpoints already admitted in V2

## Scope OUT

- deployment guidance
- live private trading authority
- widening dormant transport families into new route roots
- remote operational control planes

## Inputs

- validated runtime/config surfaces
- injected server seams (`get_exchange_client`, `bfx_read`)
- local-only request payloads

## Outputs

- local API responses
- config validation/propose responses within admitted boundaries
- paper/UI verification responses

## Invariants

- API shell remains local-only
- public/account defaults bind only to admitted read spine seams
- no accidental rebinding into broader transport execution
- guarded config writes remain fail-closed

## Must Not

- claim live-ready transport authority
- bypass bearer/config guards
- import dormant optimizer package as route authority
- widen into deployment or remote-ops claims

## Related tests

- `tests/runtime/test_public_candles_endpoint.py`
- `tests/runtime/test_account_endpoints.py`
- `tests/runtime/test_paper_endpoints.py`
- `tests/runtime/test_ui_endpoints.py`
- `tests/integration/test_config_endpoints.py`

## Governance boundaries

- API surfaces are admitted only within the current local V2 boundary.
- Transport widening remains deferred unless separately validated.

## Lifecycle role / authority level

Local runtime interface surface. Exposes admitted read/config/paper semantics but does not by itself
expand transport or promotion authority.
