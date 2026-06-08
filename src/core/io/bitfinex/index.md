# `src/core/io/bitfinex/`

## Purpose

Holds the admitted Bitfinex transport family in V2, including the active REST read spine and the
dormant package-only modules retained for constrained completeness.

## Scope IN

- REST public/account read helpers admitted in V2
- constrained package-level transport completeness
- offline/local verification of read-spine semantics

## Scope OUT

- live/private execution authority
- server/startup rebinding of dormant modules
- paper/live execution widening
- deployment or operational transport guidance

## Inputs

- Bitfinex REST request parameters
- server-injected read/public route calls

## Outputs

- public candle data
- read-only account data
- transport helper behavior verified in tests

## Invariants

- `exchange_client.py` and `read_helpers.py` are the active admitted read spine
- remaining transport modules may exist but stay dormant as package surface
- server routes must not widen beyond admitted read-spine binding

## Must Not

- activate websocket/private transport paths by accident
- bypass constrained route convergence through `core.server`
- turn dormant modules into runtime authority without a separate validated slice

## Related tests

- `tests/runtime/test_transport_read_spine.py`
- `tests/runtime/test_transport_route_inertness.py`
- `tests/utils/test_rest_public_min.py`
- `tests/utils/test_rest_auth_routes_to_exchange_client.py`
- `tests/utils/test_ws_auth_min.py`
- `tests/utils/test_ws_public_min.py`
- `tests/utils/test_ws_reconnect.py`

## Governance boundaries

- Active admission is limited to the REST read spine and constrained semantics already verified.
- Wider live-adjacent transport use remains deferred.

## Lifecycle role / authority level

Mixed surface: active read-only transport helpers plus dormant package-only transport modules.
