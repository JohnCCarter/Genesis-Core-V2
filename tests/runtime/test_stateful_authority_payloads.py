from __future__ import annotations

import json
from pathlib import Path

import core.config.authority as authority_mod
from core.config.authority import ConfigAuthority
from core.strategy.champion_loader import ChampionLoader


def test_runtime_seed_baseline_is_admitted_and_loaded_when_runtime_override_is_absent(
    monkeypatch, tmp_path: Path
) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    seed_source = repo_root / "config" / "runtime.seed.json"
    runtime_path = tmp_path / "runtime.json"
    seed_path = tmp_path / "runtime.seed.json"
    audit_path = tmp_path / "config_audit.jsonl"

    assert seed_source.exists()
    assert not (repo_root / "config" / "runtime.json").exists()

    seed_payload = json.loads(seed_source.read_text(encoding="utf-8"))
    seed_path.write_text(json.dumps(seed_payload), encoding="utf-8")

    monkeypatch.setattr(authority_mod, "SEED_PATH", seed_path)
    monkeypatch.setattr(authority_mod, "AUDIT_LOG", audit_path)

    snapshot = ConfigAuthority(path=runtime_path).load()
    cfg = snapshot.cfg.model_dump_canonical()

    assert snapshot.version == int(seed_payload.get("version") or 0)
    assert cfg["strategy_family"] == (seed_payload.get("cfg", {}).get("strategy_family") or "ri")
    assert cfg["multi_timeframe"]["regime_intelligence"]["authority_mode"] == "regime_module"
    assert (
        cfg["thresholds"]["entry_conf_overall"]
        == seed_payload["cfg"]["thresholds"]["entry_conf_overall"]
    )


def test_runtime_json_override_precedence_stays_ahead_of_seed(monkeypatch, tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    seed_source = repo_root / "config" / "runtime.seed.json"
    base_payload = json.loads(seed_source.read_text(encoding="utf-8"))

    runtime_path = tmp_path / "runtime.json"
    seed_path = tmp_path / "runtime.seed.json"
    audit_path = tmp_path / "config_audit.jsonl"

    seed_payload = json.loads(json.dumps(base_payload))
    seed_payload["version"] = 3
    seed_payload["cfg"]["exit"]["enabled"] = False

    runtime_payload = json.loads(json.dumps(base_payload))
    runtime_payload["version"] = 9
    runtime_payload["cfg"]["exit"]["enabled"] = True
    runtime_payload["cfg"]["ev"]["R_default"] = 2.1

    seed_path.write_text(json.dumps(seed_payload), encoding="utf-8")
    runtime_path.write_text(json.dumps(runtime_payload), encoding="utf-8")

    monkeypatch.setattr(authority_mod, "SEED_PATH", seed_path)
    monkeypatch.setattr(authority_mod, "AUDIT_LOG", audit_path)

    snapshot = ConfigAuthority(path=runtime_path).load()
    cfg = snapshot.cfg.model_dump_canonical()

    assert snapshot.version == 9
    assert cfg["exit"]["enabled"] is True
    assert cfg["ev"]["R_default"] == 2.1


def test_verified_champion_subset_is_admitted_and_missing_symbols_still_fallback() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    champions_dir = repo_root / "config" / "strategy" / "champions"
    loader = ChampionLoader(champions_dir=champions_dir)

    assert {path.name for path in champions_dir.glob("*.json")} == {
        "tBTCUSD_1h.json",
        "tBTCUSD_3h.json",
    }
    assert not (champions_dir / "backup").exists()

    cfg_1h = loader.load("tBTCUSD", "1h")
    cfg_3h = loader.load("tBTCUSD", "3h")
    fallback = loader.load("tTEST", "1h")

    assert cfg_1h.source.replace("\\", "/").endswith("config/strategy/champions/tBTCUSD_1h.json")
    assert cfg_3h.source.replace("\\", "/").endswith("config/strategy/champions/tBTCUSD_3h.json")
    assert not cfg_1h.source.startswith("baseline")
    assert not cfg_3h.source.startswith("baseline")
    assert fallback.source == "baseline:runtime_seed"
    assert fallback.config["strategy_family"] == "ri"
    assert (
        fallback.config["multi_timeframe"]["regime_intelligence"]["authority_mode"]
        == "regime_module"
    )
