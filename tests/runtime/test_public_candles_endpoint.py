# ruff: noqa: I001
from __future__ import annotations

import asyncio

from fastapi.testclient import TestClient

from core.server import app, public_candles as pc


def test_server_binds_transport_defaults_to_admitted_modules() -> None:
    import core.server as srv
    from core.io.bitfinex import read_helpers
    from core.io.bitfinex.exchange_client import aclose_http_client as real_aclose_http_client
    from core.io.bitfinex.exchange_client import get_exchange_client as real_get_exchange_client

    assert srv.get_exchange_client is real_get_exchange_client
    assert srv.aclose_http_client is real_aclose_http_client
    assert srv.bfx_read is read_helpers


def test_public_candles_endpoint_uses_injected_exchange_client(monkeypatch) -> None:
    class DummyResp:
        def __init__(self):
            self._json = [[0, 1, 1.5, 2, 0.5, 10]]

        def raise_for_status(self):
            return None

        def json(self):
            return self._json

    class DummyEC:
        async def public_request(self, **kwargs):
            calls.append(kwargs)
            return DummyResp()

    def unexpected_get_exchange_client():
        raise AssertionError("unexpected direct exchange client bootstrap")

    import core.api.public as public_api
    import core.io.bitfinex.exchange_client as exchange_client_mod
    import core.server as srv

    calls: list[dict[str, object]] = []
    original_cache = dict(srv._CANDLES_CACHE)

    monkeypatch.setattr(exchange_client_mod, "get_exchange_client", unexpected_get_exchange_client)
    monkeypatch.setattr(srv, "get_exchange_client", lambda: DummyEC())
    try:
        srv._CANDLES_CACHE.clear()
        client = TestClient(app)
        out = asyncio.run(pc(symbol="tBTCUSD", timeframe="1m", limit=1001))
        route = client.get(
            "/public/candles",
            params={"symbol": "tBTCUSD", "timeframe": "1m", "limit": 1001},
        )

        assert route.status_code == 200
        assert out == route.json()
        assert set(out.keys()) == {"open", "high", "low", "close", "volume"}
        assert out["open"] and out["close"]
        assert srv.public_candles is public_api.public_candles
        assert srv.public_router is public_api.router
        assert srv._CANDLES_CACHE is public_api._CANDLES_CACHE
        assert srv._CANDLES_TTL == public_api._CANDLES_TTL
        assert "tBTCUSD:1m:1001" in srv._CANDLES_CACHE
        assert len(calls) == 1
        assert calls[0]["params"] == {"limit": 1000, "sort": 1}
        candle_routes = [
            route for route in srv.app.routes if getattr(route, "path", None) == "/public/candles"
        ]
        assert len(candle_routes) == 1
    finally:
        srv._CANDLES_CACHE.clear()
        srv._CANDLES_CACHE.update(original_cache)


def test_server_lifespan_closes_http_client(monkeypatch) -> None:
    import core.server as srv

    closed = {"ok": False}

    async def fake_aclose_http_client() -> None:
        closed["ok"] = True

    monkeypatch.setattr(srv, "aclose_http_client", fake_aclose_http_client)

    with TestClient(srv.app):
        pass

    assert closed["ok"] is True
