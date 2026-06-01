from __future__ import annotations

import asyncio

from fastapi.testclient import TestClient

from core.server import app


def test_auth_check_uses_injected_read_helpers(monkeypatch) -> None:
    async def fake_wallets():
        return []

    async def fake_positions():
        return []

    import core.api.account as account_api
    import core.server as srv

    monkeypatch.setattr(srv.bfx_read, "get_wallets", fake_wallets)
    monkeypatch.setattr(srv.bfx_read, "get_positions", fake_positions)

    client = TestClient(app)
    direct_json = asyncio.run(srv.auth_check())
    route_json = client.get("/auth/check").json()

    assert direct_json == route_json == {"ok": True, "wallets": 0, "positions": 0}
    assert srv.auth_check is account_api.auth_check
    assert srv.account_wallets is account_api.account_wallets
    assert srv.account_positions is account_api.account_positions
    assert srv.account_orders is account_api.account_orders
    assert srv.account_router is account_api.router
    assert srv._ACCOUNT_CACHE is account_api._ACCOUNT_CACHE
    assert srv._ACCOUNT_TTL == account_api._ACCOUNT_TTL


def test_account_wallets_filters_exchange_only(monkeypatch) -> None:
    async def fake_wallets():
        return [
            ["exchange", "USD", 100.0, 0.0, 80.0],
            ["margin", "USD", 50.0, 0.0, 30.0],
            ["exchange", "ETH", 2.0, 0.0, 1.5],
        ]

    import core.server as srv

    monkeypatch.setattr(srv.bfx_read, "get_wallets", fake_wallets)

    client = TestClient(app)
    response = client.get("/account/wallets")

    assert response.status_code == 200
    data = response.json()
    items = data.get("items") or []
    assert all(item.get("type") == "exchange" for item in items)
    assert sorted(item.get("currency") for item in items) == ["ETH", "USD"]


def test_account_wallets_fail_closed_without_transport(monkeypatch) -> None:
    async def boom_wallets():
        raise RuntimeError("boom")

    def unexpected_get_exchange_client():
        raise AssertionError("unexpected real exchange client bootstrap")

    import core.io.bitfinex.exchange_client as exchange_client_mod
    import core.server as srv

    monkeypatch.setattr(exchange_client_mod, "get_exchange_client", unexpected_get_exchange_client)
    monkeypatch.setattr(srv.bfx_read, "get_wallets", boom_wallets)

    client = TestClient(app)
    srv._ACCOUNT_CACHE["wallets"] = {"ts": 0.0, "data": {"items": []}}
    response = client.get("/account/wallets")

    assert response.status_code == 200
    raw = response.text
    assert "Deferred account read helpers" not in raw
    assert response.json().get("error") == "internal_error"


def test_account_positions_and_orders_filter_test_symbols(monkeypatch) -> None:
    async def fake_positions():
        return [
            ["tBTCUSD", "ACTIVE", 0.1, 30000.0],
            ["tTESTETH:TESTUSD", "ACTIVE", 1.2, 1500.0],
        ]

    async def fake_orders():
        real_order = [0, 0, 0, "tBTCUSD", 0, 0, 0.01, 0, "EXCHANGE MARKET", 0, 0, 0, 0, "ACTIVE"]
        test_order = [
            0,
            0,
            0,
            "tTESTDOGE:TESTUSD",
            0,
            0,
            25.0,
            0,
            "EXCHANGE MARKET",
            0,
            0,
            0,
            0,
            "ACTIVE",
        ]
        return [real_order, test_order]

    import core.server as srv

    monkeypatch.setattr(srv.bfx_read, "get_positions", fake_positions)
    monkeypatch.setattr(srv.bfx_read, "get_orders", fake_orders)

    client = TestClient(app)
    positions = client.get("/account/positions")
    orders = client.get("/account/orders")

    assert positions.status_code == 200
    assert orders.status_code == 200
    assert positions.json()["items"] == [
        {
            "symbol": "tTESTETH:TESTUSD",
            "status": "ACTIVE",
            "amount": 1.2,
            "base_price": 1500.0,
        }
    ]
    assert orders.json()["items"] == [
        {
            "symbol": "tTESTDOGE:TESTUSD",
            "amount": 25.0,
            "type": "EXCHANGE MARKET",
            "status": "ACTIVE",
        }
    ]
