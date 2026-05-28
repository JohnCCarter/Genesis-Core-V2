from __future__ import annotations

from core.bootstrap.fixture_smoke import DEFAULT_FIXTURE_PATH, load_fixture, run_fixture_smoke


def test_runtime_fixture_file_exists_with_expected_shape() -> None:
    payload = load_fixture()

    assert DEFAULT_FIXTURE_PATH.exists()
    assert payload["policy"] == {"symbol": "tBTCUSD", "timeframe": "1h"}
    assert payload["name"] == "runtime_fixture_smoke_minimal"
    assert len(payload["candles"]["close"]) == 120


def test_runtime_fixture_smoke_runs_end_to_end() -> None:
    result = run_fixture_smoke()

    assert result["bar_count"] == 120
    assert result["features_count"] > 0
    assert result["regime"] in {"bull", "bear", "ranging", "balanced"}
    assert result["probas"]["buy"] > result["probas"]["sell"]
    assert result["confidence"]["overall"] < 0.7
    assert result["action"] == "NONE"
    assert result["versions"] == {
        "prob_model": "seed_model_fixture_v1",
        "calibration": "seed_model_fixture_v1",
        "confidence": "v1",
        "decision": "v1",
    }
