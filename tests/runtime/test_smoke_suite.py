from __future__ import annotations

from core.bootstrap.smoke_suite import run_smoke_suite


def test_runtime_smoke_suite_runs_all_smokes() -> None:
    result = run_smoke_suite()

    assert result["suite"] == "runtime_smoke_suite_v1"
    assert result["checks"] == {
        "fixture_smoke": "passed",
        "champion_smoke": "passed",
        "evaluate_champion_smoke": "passed",
        "model_smoke": "passed",
        "backtest_smoke": "passed",
    }
    assert result["fixture_smoke"]["action"] == "NONE"
    assert result["champion_smoke"]["threshold_entry_conf_overall"] == 0.7
    assert (
        result["evaluate_champion_smoke"]["champion_source"]
        == "registry/fixtures/champions/tBTCUSD_1h.json"
    )
    assert result["evaluate_champion_smoke"]["prob_model_version"] == "seed_model_fixture_v1"
    assert result["model_smoke"]["versions"]["prob_model_version"] == "seed_model_fixture_v1"
    assert result["backtest_smoke"]["deterministic"] is True
    assert result["backtest_smoke"]["trade_count"] == 1
