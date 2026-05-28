from __future__ import annotations

from core.bootstrap.evaluate_champion_smoke import run_evaluate_champion_smoke


def test_runtime_evaluate_champion_smoke_uses_local_champion_fixture() -> None:
    result = run_evaluate_champion_smoke()

    assert result["symbol"] == "tBTCUSD"
    assert result["timeframe"] == "1h"
    assert result["action"] == "NONE"
    assert result["buy_proba"] > result["sell_proba"]
    assert result["champion_source"] == "registry/fixtures/champions/tBTCUSD_1h.json"
    assert result["prob_model_version"] == "seed_model_fixture_v1"
    assert result["calibration_version"] == "seed_model_fixture_v1"
    assert result["regime_aware_calibration"] is True
    assert result["model_schema"] == ["ema_50"]
    assert result["threshold_entry_conf_overall"] == 0.7
    assert result["risk_map_rows"] == 2
    assert result["meta_note"] == "seed_fixture_champion"
    assert result["precomputed_feature_keys"] == ["ema_50"]
