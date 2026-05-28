from __future__ import annotations

from core.bootstrap.model_smoke import run_model_smoke


def test_runtime_model_smoke_uses_local_registry_and_model_fixture() -> None:
    result = run_model_smoke()

    assert result["schema"] == ["ema_50"]
    assert result["probas"]["buy"] > result["probas"]["sell"]
    assert abs(result["probas"]["hold"]) < 1e-12
    assert result["versions"] == {
        "prob_model_version": "seed_model_fixture_v1",
        "calibration_version": "seed_model_fixture_v1",
        "regime_aware_calibration": True,
    }
    assert result["calibration_used"]["regime"] == "balanced"
    assert result["calibration_used"]["buy_calib"] == {"a": 1.0, "b": 0.1}
    assert result["calibration_used"]["sell_calib"] == {"a": 1.0, "b": -0.1}
