from __future__ import annotations

import asyncio
import json

import core.io.bitfinex.ws_auth as ws_auth


class _DummyMetrics:
    def inc(self, *_args, **_kwargs) -> None:
        return None

    def event(self, *_args, **_kwargs) -> None:
        return None


class _DummySettings:
    BITFINEX_WS_API_KEY = "ws-key"
    BITFINEX_API_KEY = ""
    BITFINEX_WS_API_SECRET = "ws-secret"
    BITFINEX_API_SECRET = ""


def test_auth_ping_sends_auth_message_and_returns_ok(monkeypatch) -> None:
    sent_messages: list[dict[str, str]] = []

    class DummyWS:
        async def __aenter__(self):
            return self

        async def __aexit__(self, _exc_type, _exc, _tb):
            return False

        async def send(self, payload: str) -> None:
            sent_messages.append(json.loads(payload))

        async def recv(self) -> str:
            return json.dumps({"event": "auth", "status": "OK"})

    monkeypatch.setattr(ws_auth, "get_settings", lambda: _DummySettings())
    monkeypatch.setattr(ws_auth, "get_nonce", lambda _key: "123456000")
    monkeypatch.setattr(
        ws_auth,
        "build_hmac_signature",
        lambda secret, payload: f"sig:{secret}:{payload}",
    )
    monkeypatch.setattr(ws_auth, "metrics", _DummyMetrics())
    monkeypatch.setattr(ws_auth.websockets, "connect", lambda *args, **kwargs: DummyWS())

    result = asyncio.run(ws_auth.auth_ping(timeout=0.01))

    assert result == {"ok": True}
    assert sent_messages == [
        {
            "event": "auth",
            "apiKey": "ws-key",
            "authSig": "sig:ws-secret:AUTH123456",
            "authPayload": "AUTH123456",
            "authNonce": "123456",
        }
    ]
