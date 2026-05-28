from __future__ import annotations

from fastapi.testclient import TestClient

from core.server import TEST_SPOT_WHITELIST, app


def test_local_info_routes_expose_whitelist_and_dashboard() -> None:
    client = TestClient(app)

    whitelist_response = client.get("/paper/whitelist")
    assert whitelist_response.status_code == 200
    assert whitelist_response.json() == {"symbols": sorted(TEST_SPOT_WHITELIST)}

    dashboard_response = client.get("/observability/dashboard")
    assert dashboard_response.status_code == 200
    payload = dashboard_response.json()

    assert "counters" in payload and isinstance(payload["counters"], dict)
    assert "gauges" in payload and isinstance(payload["gauges"], dict)
    assert "events" in payload and isinstance(payload["events"], list)


def test_local_observability_dashboard_passthrough(monkeypatch) -> None:
    import core.api.info as info_api

    sentinel = {
        "counters": {"route_calls": 7},
        "gauges": {"latency_ms": 12.5},
        "events": [{"kind": "sentinel"}],
        "extra": {"source": "patched"},
    }

    monkeypatch.setattr(info_api, "get_dashboard", lambda: sentinel)

    client = TestClient(app)
    response = client.get("/observability/dashboard")

    assert response.status_code == 200
    assert response.json() == sentinel
