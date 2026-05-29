from __future__ import annotations

import asyncio

import httpx
import pytest
from fastapi.testclient import TestClient

from core.server import app


def test_paper_submit_uses_injected_exchange_client(monkeypatch) -> None:
    class DummyResp:
        status_code = 200

        def json(self):
            return {"status": "OK"}

    class DummyEC:
        async def signed_request(self, **kwargs):
            calls.append(kwargs)
            return DummyResp()

    import core.api.paper as paper_api
    import core.server as srv

    calls: list[dict[str, object]] = []
    monkeypatch.setattr(srv, "get_exchange_client", lambda: DummyEC())

    client = TestClient(app)
    payload = {
        "symbol": "tTESTBTC:TESTUSD",
        "side": "LONG",
        "size": 0.003,
        "type": "MARKET",
    }

    direct_json = asyncio.run(srv.paper_submit(payload))
    route = client.post("/paper/submit", json=payload)

    assert route.status_code == 200
    assert direct_json == route.json()
    assert direct_json.get("ok") is True
    assert direct_json.get("exchange") == "bitfinex"
    assert direct_json.get("request", {}).get("symbol") == "tTESTBTC:TESTUSD"
    assert srv.paper_submit is paper_api.paper_submit
    assert srv.paper_estimate is paper_api.paper_estimate
    assert srv.paper_router is paper_api.router
    paper_submit_routes = [
        route for route in srv.app.routes if getattr(route, "path", None) == "/paper/submit"
    ]
    assert len(paper_submit_routes) == 1
    assert calls == [
        {
            "method": "POST",
            "endpoint": "auth/w/order/submit",
            "body": direct_json["request"],
        },
        {
            "method": "POST",
            "endpoint": "auth/w/order/submit",
            "body": direct_json["request"],
        },
    ]


def test_paper_estimate_route_and_canonical_module_parity(monkeypatch) -> None:
    import core.api.paper as paper_api
    import core.server as srv

    class DummySettings:
        BITFINEX_API_KEY = "key"  # pragma: allowlist secret
        BITFINEX_API_SECRET = "secret"  # pragma: allowlist secret

    class DummyResp:
        def json(self):
            return [0, 0, 0, 0, 0, 0, 50.0]

    class DummyEC:
        async def public_request(self, **kwargs):
            calls.append(kwargs)
            return DummyResp()

    async def fake_wallets():
        return [
            ["exchange", "USD", 0, 0, 250.0],
            ["exchange", "ETH", 0, 0, 7.0],
        ]

    calls: list[dict[str, object]] = []
    monkeypatch.setattr(srv, "get_settings", lambda: DummySettings())
    monkeypatch.setattr(srv.bfx_read, "get_wallets", fake_wallets)
    monkeypatch.setattr(srv, "get_exchange_client", lambda: DummyEC())
    monkeypatch.setattr(srv, "MIN_ORDER_SIZE", {"tTESTBTC:TESTUSD": 2.5})
    monkeypatch.setattr(srv, "MIN_ORDER_MARGIN", 0.2)
    monkeypatch.setattr(srv, "_real_from_test", lambda _sym: "tFAKEUSD")
    monkeypatch.setattr(srv, "_base_ccy_from_test", lambda _sym: "ETH")

    client = TestClient(app)
    direct_json = asyncio.run(srv.paper_estimate(symbol="tNOPE"))
    route = client.get("/paper/estimate", params={"symbol": "tNOPE"})

    assert route.status_code == 200
    assert srv.paper_estimate is paper_api.paper_estimate
    assert srv.paper_router is paper_api.router
    assert direct_json == route.json()
    assert direct_json == {
        "symbol": "tTESTBTC:TESTUSD",
        "required_min": 2.5,
        "min_with_margin": 3.0,
        "usd_available": 250.0,
        "base_available": 7.0,
        "last_price": 50.0,
        "est_max_size": 5.0,
    }
    assert calls == [
        {
            "method": "GET",
            "endpoint": "ticker/tFAKEUSD",
            "timeout": 5,
        },
        {
            "method": "GET",
            "endpoint": "ticker/tFAKEUSD",
            "timeout": 5,
        },
    ]
    paper_estimate_routes = [
        route for route in srv.app.routes if getattr(route, "path", None) == "/paper/estimate"
    ]
    assert len(paper_estimate_routes) == 1


def test_paper_estimate_without_credentials_skips_wallet_lookup(monkeypatch) -> None:
    import core.server as srv

    class DummySettings:
        BITFINEX_API_KEY = ""  # pragma: allowlist secret
        BITFINEX_API_SECRET = ""  # pragma: allowlist secret

    class DummyResp:
        def json(self):
            return [0, 0, 0, 0, 0, 0, 20.0]

    class DummyEC:
        async def public_request(self, **_kwargs):
            return DummyResp()

    async def unexpected_wallets():
        raise AssertionError("wallet lookup should be skipped without credentials")

    monkeypatch.setattr(srv, "get_settings", lambda: DummySettings())
    monkeypatch.setattr(srv.bfx_read, "get_wallets", unexpected_wallets)
    monkeypatch.setattr(srv, "get_exchange_client", lambda: DummyEC())

    direct_json = asyncio.run(srv.paper_estimate(symbol="tTESTBTC:TESTUSD"))

    assert direct_json["symbol"] == "tTESTBTC:TESTUSD"
    assert direct_json["required_min"] == 0.001
    assert direct_json["min_with_margin"] == pytest.approx(0.00105)
    assert direct_json["usd_available"] is None
    assert direct_json["base_available"] is None
    assert direct_json["last_price"] == 20.0
    assert direct_json["est_max_size"] is None


def test_paper_submit_invalid_symbol_returns_pinned_payload() -> None:
    import core.server as srv

    client = TestClient(app)
    payload = {"symbol": "tBTCUSD", "side": "LONG", "size": 0.003, "type": "MARKET"}

    direct_json = asyncio.run(srv.paper_submit(payload))
    route = client.post("/paper/submit", json=payload)

    expected = {
        "ok": False,
        "error": "invalid_symbol",
        "requested_symbol": "tBTCUSD",
        "message": "symbol must be one of TEST_SPOT_WHITELIST",
    }
    assert direct_json == route.json() == expected


@pytest.mark.parametrize(
    "payload",
    [
        {"symbol": "tTESTBTC:TESTUSD", "side": "NONE", "size": 1.0, "type": "MARKET"},
        {"symbol": "tTESTBTC:TESTUSD", "side": "LONG", "size": 0.0, "type": "MARKET"},
    ],
    ids=["invalid-side", "invalid-size"],
)
def test_paper_submit_invalid_action_or_size_route_parity(payload) -> None:
    import core.server as srv

    client = TestClient(app)
    direct_json = asyncio.run(srv.paper_submit(payload))
    route = client.post("/paper/submit", json=payload)

    assert route.status_code == 200
    assert direct_json == route.json() == {"ok": False, "error": "invalid_action_or_size"}


def test_paper_submit_wallet_cap_uses_shared_helpers(monkeypatch) -> None:
    import core.server as srv

    class DummySettings:
        WALLET_CAP_ENABLED = 1
        BITFINEX_API_KEY = "key"  # pragma: allowlist secret
        BITFINEX_API_SECRET = "secret"  # pragma: allowlist secret

    class DummyResp:
        def __init__(self, payload):
            self.status_code = 200
            self._payload = payload

        def json(self):
            return self._payload

    class DummyEC:
        async def public_request(self, **kwargs):
            ticker_calls.append(kwargs)
            return DummyResp([0, 0, 0, 0, 0, 0, 5.0])

        async def signed_request(self, **kwargs):
            signed_calls.append(kwargs)
            return DummyResp({"status": "OK"})

    async def fake_wallets():
        return [
            ["exchange", "USD", 0, 0, 20.0],
            ["exchange", "ETH", 0, 0, 3.0],
        ]

    ticker_calls: list[dict[str, object]] = []
    signed_calls: list[dict[str, object]] = []
    monkeypatch.setattr(srv, "get_settings", lambda: DummySettings())
    monkeypatch.setattr(srv.bfx_read, "get_wallets", fake_wallets)
    monkeypatch.setattr(srv, "get_exchange_client", lambda: DummyEC())
    monkeypatch.setattr(srv, "MIN_ORDER_SIZE", {"tTESTBTC:TESTUSD": 1.0})
    monkeypatch.setattr(srv, "MIN_ORDER_MARGIN", 0.1)
    monkeypatch.setattr(srv, "_real_from_test", lambda _sym: "tFAKEUSD")
    monkeypatch.setattr(srv, "_base_ccy_from_test", lambda _sym: "ETH")

    long_out = asyncio.run(
        srv.paper_submit(
            {
                "symbol": "tTESTBTC:TESTUSD",
                "side": "LONG",
                "size": 10.0,
                "type": "MARKET",
            }
        )
    )
    short_out = asyncio.run(
        srv.paper_submit(
            {
                "symbol": "tTESTBTC:TESTUSD",
                "side": "SHORT",
                "size": 10.0,
                "type": "MARKET",
            }
        )
    )

    assert long_out["ok"] is True
    assert long_out["meta"]["wallet_clamped"] is True
    assert long_out["meta"]["size_after"] == 4.0
    assert short_out["ok"] is True
    assert short_out["meta"]["wallet_clamped"] is True
    assert short_out["meta"]["size_after"] == 3.0
    assert ticker_calls == [
        {
            "method": "GET",
            "endpoint": "ticker/tFAKEUSD",
            "timeout": 5,
        }
    ]
    assert signed_calls[0]["body"]["amount"] == "4.0"
    assert signed_calls[1]["body"]["amount"] == "-3.0"


def test_paper_submit_http_status_error_shape(monkeypatch) -> None:
    import core.server as srv

    class DummyEC:
        async def signed_request(self, **_kwargs):
            request = httpx.Request("POST", "https://example.test/auth/w/order/submit")
            response = httpx.Response(429, request=request, text="rate limited")
            raise httpx.HTTPStatusError("boom", request=request, response=response)

    monkeypatch.setattr(srv, "get_exchange_client", lambda: DummyEC())

    client = TestClient(app)
    payload = {"symbol": "tTESTBTC:TESTUSD", "side": "LONG", "size": 1.0, "type": "MARKET"}
    direct_json = asyncio.run(srv.paper_submit(payload))
    route_json = client.post("/paper/submit", json=payload).json()

    for data in (direct_json, route_json):
        assert data["ok"] is False
        assert data["error"] == "bitfinex_http_error"
        assert data["status"] == 429
        assert isinstance(data["error_id"], str)
        assert len(data["error_id"]) == 12


def test_paper_submit_internal_error_shape(monkeypatch) -> None:
    import core.server as srv

    class DummyEC:
        async def signed_request(self, **_kwargs):
            raise RuntimeError("boom")

    monkeypatch.setattr(srv, "get_exchange_client", lambda: DummyEC())

    client = TestClient(app)
    payload = {"symbol": "tTESTBTC:TESTUSD", "side": "LONG", "size": 1.0, "type": "MARKET"}
    direct_json = asyncio.run(srv.paper_submit(payload))
    route_json = client.post("/paper/submit", json=payload).json()

    for data in (direct_json, route_json):
        assert data["ok"] is False
        assert data["error"] == "internal_error"
        assert isinstance(data["error_id"], str)
        assert len(data["error_id"]) == 12
        assert "status" not in data
