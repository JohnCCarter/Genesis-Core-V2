from __future__ import annotations

import asyncio


def test_exchange_client_public_request_smoke(monkeypatch) -> None:
    from core.io.bitfinex import exchange_client as mod

    class DummySettings:
        BITFINEX_API_KEY = "key"  # pragma: allowlist secret
        BITFINEX_API_SECRET = "secret"  # pragma: allowlist secret
        symbol_mode = "realistic"

    class DummyResponse:
        def __init__(self, status_code: int, json_payload=None):
            self.status_code = status_code
            self._json_payload = json_payload if json_payload is not None else {}
            self.text = "{}"

        def raise_for_status(self):
            if self.status_code >= 400:
                import httpx

                raise httpx.HTTPStatusError("err", request=None, response=self)

        def json(self):
            return self._json_payload

    async def dummy_get(url, params=None, timeout=None):
        _ = (url, params, timeout)
        return DummyResponse(200, json_payload=[[0, 1, 2, 3, 4, 5]])

    class DummyClient:
        async def aclose(self):
            return None

        get = staticmethod(dummy_get)

    orig_http_client = mod._HTTP_CLIENT
    orig_exchange_client = mod._EXCHANGE_CLIENT
    monkeypatch.setattr(mod, "get_settings", lambda: DummySettings())
    try:
        mod._HTTP_CLIENT = DummyClient()
        mod._EXCHANGE_CLIENT = None
        response = asyncio.run(
            mod.get_exchange_client().public_request(
                method="GET",
                endpoint="candles/trade:1m:tBTCUSD/hist",
                params={"limit": 5, "sort": 1},
                timeout=10,
            )
        )
        assert response.status_code == 200
        assert response.json() == [[0, 1, 2, 3, 4, 5]]
    finally:
        mod._HTTP_CLIENT = orig_http_client
        mod._EXCHANGE_CLIENT = orig_exchange_client


def test_exchange_client_signed_request_smoke(monkeypatch) -> None:
    from core.io.bitfinex import exchange_client as mod

    metric_events: list[tuple[str, tuple, dict]] = []

    class DummyMetrics:
        def inc(self, *args, **kwargs):
            metric_events.append(("inc", args, kwargs))

        def event(self, *args, **kwargs):
            metric_events.append(("event", args, kwargs))

    class DummySettings:
        BITFINEX_API_KEY = "key"  # pragma: allowlist secret
        BITFINEX_API_SECRET = "secret"  # pragma: allowlist secret
        symbol_mode = "realistic"

    class DummyResponse:
        def __init__(self, status_code: int, text: str = "{}", json_payload=None):
            self.status_code = status_code
            self._text = text
            self._json_payload = json_payload if json_payload is not None else {}

        def raise_for_status(self):
            if self.status_code >= 400:
                import httpx

                raise httpx.HTTPStatusError("err", request=None, response=self)

        @property
        def text(self):
            return self._text

        def json(self):
            return self._json_payload

    async def dummy_post(url, headers=None, content=None, timeout=None):
        _ = (url, headers, content, timeout)
        return DummyResponse(200, text="{}", json_payload={})

    class DummyClient:
        async def aclose(self):
            return None

        post = staticmethod(dummy_post)

    orig_http_client = mod._HTTP_CLIENT
    orig_exchange_client = mod._EXCHANGE_CLIENT
    monkeypatch.setattr(mod, "get_settings", lambda: DummySettings())
    monkeypatch.setattr(mod, "get_nonce", lambda _key: "1")
    monkeypatch.setattr(mod, "build_hmac_signature", lambda _secret, _message: "sig")
    monkeypatch.setattr(mod, "metrics", DummyMetrics())
    try:
        mod._HTTP_CLIENT = DummyClient()
        mod._EXCHANGE_CLIENT = None
        response = asyncio.run(
            mod.get_exchange_client().signed_request(
                method="POST",
                endpoint="auth/r/wallets",
                body={},
                timeout=10,
            )
        )
        assert response.status_code == 200
        assert any(
            event[0] == "inc" and event[1] and event[1][0] == "rest_auth_request"
            for event in metric_events
        )
    finally:
        mod._HTTP_CLIENT = orig_http_client
        mod._EXCHANGE_CLIENT = orig_exchange_client


def test_exchange_client_aclose_http_client_resets_global_client() -> None:
    from core.io.bitfinex import exchange_client as mod

    closed = {"ok": False}

    class DummyClient:
        async def aclose(self):
            closed["ok"] = True

    orig = mod._HTTP_CLIENT
    try:
        mod._HTTP_CLIENT = DummyClient()  # type: ignore[assignment]
        asyncio.run(mod.aclose_http_client())
        assert closed["ok"] is True
        assert mod._HTTP_CLIENT is None
    finally:
        mod._HTTP_CLIENT = orig


def test_read_helpers_decode_wallets_positions_and_orders(monkeypatch) -> None:
    from core.io.bitfinex import read_helpers as rh

    calls: list[dict] = []

    class DummyResp:
        text = "[]"

        def json(self):
            return []

    class DummyEC:
        async def signed_request(self, **kwargs):
            calls.append(dict(kwargs))
            return DummyResp()

    monkeypatch.setattr(rh, "get_exchange_client", lambda: DummyEC())

    wallets = asyncio.run(rh.get_wallets())
    positions = asyncio.run(rh.get_positions())
    orders = asyncio.run(rh.get_orders())

    assert isinstance(wallets, list)
    assert isinstance(positions, list)
    assert isinstance(orders, list)
    assert [call.get("endpoint") for call in calls] == [
        "auth/r/wallets",
        "auth/r/positions",
        "auth/r/orders",
    ]
    assert all(call.get("method") == "POST" for call in calls)
    assert all(call.get("body") == {} for call in calls)
