from __future__ import annotations

import asyncio

import core.io.bitfinex.rest_public as rest_public


def test_get_platform_status_uses_public_endpoint_and_parses_status(monkeypatch) -> None:
    calls: list[str] = []

    class DummyResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> list[int]:
            return [1]

    class DummyClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, _exc_type, _exc, _tb):
            return False

        async def get(self, url: str):
            calls.append(url)
            return DummyResponse()

    monkeypatch.setattr(rest_public.httpx, "AsyncClient", lambda *args, **kwargs: DummyClient())

    status = asyncio.run(rest_public.get_platform_status())

    assert status == 1
    assert calls == [f"{rest_public.BASE_PUB}/platform/status"]
