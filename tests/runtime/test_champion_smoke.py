from __future__ import annotations

from core.bootstrap.champion_smoke import run_champion_smoke


def test_runtime_champion_smoke_loads_local_fixture() -> None:
    result = run_champion_smoke()

    assert result["source"] == "registry/fixtures/champions/tBTCUSD_1h.json"
    assert result["version"] == "seed_champion_fixture_v1"
    assert result["cache_reused"] is True
    assert result["threshold_entry_conf_overall"] == 0.7
    assert result["risk_map_rows"] == 2
