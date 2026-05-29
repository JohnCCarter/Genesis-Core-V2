from __future__ import annotations

import core.server as server_mod

EXPECTED_ROUTE_PATHS = {
    "/account/orders",
    "/account/positions",
    "/account/wallets",
    "/auth/check",
    "/config/runtime",
    "/config/runtime/propose",
    "/config/runtime/validate",
    "/debug/auth",
    "/docs",
    "/docs/oauth2-redirect",
    "/health",
    "/models/reload",
    "/observability/dashboard",
    "/openapi.json",
    "/paper/estimate",
    "/paper/submit",
    "/paper/whitelist",
    "/public/candles",
    "/redoc",
    "/strategy/evaluate",
    "/ui",
}


def test_transport_family_admission_keeps_route_inventory_stable() -> None:
    route_paths = {route.path for route in server_mod.app.routes}

    assert route_paths == EXPECTED_ROUTE_PATHS


def test_transport_family_admission_does_not_rebind_server_module() -> None:
    server_namespace = vars(server_mod)

    for name in ("rest_public", "rest_auth", "ws_public", "ws_auth", "ws_reconnect"):
        assert name not in server_namespace
