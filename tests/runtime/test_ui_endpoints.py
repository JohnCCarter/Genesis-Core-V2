from __future__ import annotations

from fastapi.testclient import TestClient

from core.server import app


def test_ui_get_and_evaluate_post() -> None:
    import core.api.ui as ui_api
    import core.server as srv

    client = TestClient(app)
    response = client.get("/ui")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Minimal test" in response.text
    assert srv.ui_page is ui_api.ui_page
    assert response.text == srv.ui_page() == ui_api.ui_page()

    payload = {
        "policy": {"symbol": "tBTCUSD", "timeframe": "1m"},
        "configs": {
            "features": {
                "percentiles": {"ema": [-10, 10], "rsi": [-10, 10]},
                "versions": {"feature_set": "v1"},
            },
            "thresholds": {
                "entry_conf_overall": 0.7,
                "regime_proba": {"balanced": 0.55},
            },
            "gates": {"hysteresis_steps": 2, "cooldown_bars": 0},
            "risk": {"risk_map": [[0.6, 0.005], [0.7, 0.01]]},
            "ev": {"R_default": 1.5},
        },
        "candles": {
            "open": [1, 2, 3, 4],
            "high": [2, 3, 4, 5],
            "low": [0.5, 1.5, 2.5, 3.5],
            "close": [1.5, 2.5, 3.5, 4.5],
            "volume": [10, 11, 12, 13],
        },
        "state": {},
    }
    evaluate_response = client.post("/strategy/evaluate", json=payload)

    assert evaluate_response.status_code == 200
    data = evaluate_response.json()
    assert set(data.keys()) == {"result", "meta"}
    meta = data["meta"]
    assert isinstance(meta, dict)
    observability = meta.get("observability")
    assert isinstance(observability, dict)
    shadow_regime = observability.get("shadow_regime")
    assert isinstance(shadow_regime, dict)
    assert "authority_mode" in shadow_regime
    assert "authority_mode_source" in shadow_regime
    assert "scpe_ri_v1" not in observability


def test_ui_page_contains_default_off_ri_runtime_observability_consumer_controls() -> None:
    client = TestClient(app)

    response = client.get("/ui")

    assert response.status_code == 200
    assert 'id="ri_observability_opt_in"' in response.text
    assert "SCPE RI runtime-observability (opt-in)" in response.text
    assert "function buildRuntimeObservabilityState()" in response.text
    assert "const state = {};" in response.text
    assert "if (el('ri_observability_opt_in')?.checked)" in response.text
    assert "state: buildRuntimeObservabilityState()" in response.text
    assert "scpe_ri_v1: true" in response.text
    assert 'id="ri_observability_opt_in" checked' not in response.text


def test_ui_route_server_and_canonical_identity() -> None:
    import core.api.ui as ui_api
    import core.server as srv

    assert srv.ui_page is ui_api.ui_page
    assert srv.ui_router is ui_api.router
    ui_routes = [route for route in srv.app.routes if getattr(route, "path", None) == "/ui"]
    assert len(ui_routes) == 1
