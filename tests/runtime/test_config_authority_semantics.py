from __future__ import annotations

import importlib
import json
from pathlib import Path

from fastapi.testclient import TestClient

import core.api.config as api
import core.config.authority as authority_mod
from core.server import app


def _ri_authority_patch() -> dict[str, object]:
    return {
        "strategy_family": "ri",
        "thresholds": {
            "entry_conf_overall": 0.25,
            "regime_proba": {"balanced": 0.36},
            "signal_adaptation": {
                "atr_period": 14,
                "zones": {
                    "low": {"entry_conf_overall": 0.16, "regime_proba": 0.33},
                    "mid": {"entry_conf_overall": 0.40, "regime_proba": 0.51},
                    "high": {"entry_conf_overall": 0.32, "regime_proba": 0.57},
                },
            },
        },
        "gates": {"hysteresis_steps": 3, "cooldown_bars": 2},
        "regime_unified": {"authority_mode": "regime_module"},
    }


def _legacy_runtime_patch(*, entry_conf_overall: float = 0.64) -> dict[str, object]:
    return {
        "strategy_family": "legacy",
        "thresholds": {
            "entry_conf_overall": entry_conf_overall,
            "regime_proba": {"balanced": 0.5},
            "signal_adaptation": {
                "atr_period": 28,
                "zones": {
                    "low": {"entry_conf_overall": 0.24, "regime_proba": 0.36},
                    "mid": {"entry_conf_overall": 0.30, "regime_proba": 0.44},
                    "high": {"entry_conf_overall": 0.36, "regime_proba": 0.56},
                },
            },
        },
        "gates": {"hysteresis_steps": 2, "cooldown_bars": 0},
        "multi_timeframe": {"regime_intelligence": {"authority_mode": "legacy"}},
    }


def _snapshot_file(path: Path) -> tuple[bool, str | None]:
    return path.exists(), path.read_text(encoding="utf-8") if path.exists() else None


def _assert_file_unchanged(path: Path, before_exists: bool, before_text: str | None) -> None:
    assert path.exists() is before_exists
    if before_exists:
        assert path.read_text(encoding="utf-8") == before_text


def test_config_authority_paths_do_not_depend_on_cwd(tmp_path, monkeypatch) -> None:
    other_cwd = tmp_path / "other"
    other_cwd.mkdir()

    monkeypatch.chdir(tmp_path)
    importlib.reload(authority_mod)
    p1 = authority_mod.RUNTIME_PATH
    a1 = authority_mod.AUDIT_LOG
    s1 = authority_mod.SEED_PATH

    monkeypatch.chdir(other_cwd)
    importlib.reload(authority_mod)
    p2 = authority_mod.RUNTIME_PATH
    a2 = authority_mod.AUDIT_LOG
    s2 = authority_mod.SEED_PATH

    assert p1 == p2
    assert a1 == a2
    assert s1 == s2

    expected_repo_root = Path(authority_mod.__file__).resolve().parents[3]
    assert p1 == expected_repo_root / "config" / "runtime.json"
    assert a1 == expected_repo_root / "logs" / "config_audit.jsonl"
    assert s1 == expected_repo_root / "config" / "runtime.seed.json"


def test_config_authority_api_semantics_are_tmp_path_isolated(monkeypatch, tmp_path: Path) -> None:
    repo_runtime_path = authority_mod.RUNTIME_PATH
    repo_audit_path = authority_mod.AUDIT_LOG
    repo_seed_path = authority_mod.SEED_PATH

    runtime_before = _snapshot_file(repo_runtime_path)
    audit_before = _snapshot_file(repo_audit_path)
    seed_before = _snapshot_file(repo_seed_path)

    tmp_runtime_path = tmp_path / "runtime.json"
    tmp_audit_path = tmp_path / "config_audit.jsonl"
    tmp_seed_path = tmp_path / "runtime.seed.json"

    monkeypatch.setattr(authority_mod, "RUNTIME_PATH", tmp_runtime_path)
    monkeypatch.setattr(authority_mod, "AUDIT_LOG", tmp_audit_path)
    monkeypatch.setattr(authority_mod, "SEED_PATH", tmp_seed_path)
    monkeypatch.setattr(api, "authority", authority_mod.ConfigAuthority(tmp_runtime_path))

    client = TestClient(app)

    baseline = client.get("/config/runtime")
    assert baseline.status_code == 200
    baseline_body = baseline.json()
    assert int(baseline_body.get("version") or 0) == 0
    assert baseline_body.get("cfg", {}).get("strategy_family") == "legacy"
    assert baseline_body.get("cfg", {}).get("multi_timeframe", {}).get("regime_intelligence", {}).get(
        "authority_mode"
    ) == "legacy"
    assert not tmp_runtime_path.exists()

    validate = client.post("/config/runtime/validate", json=_ri_authority_patch())
    assert validate.status_code == 200
    validate_body = validate.json()
    assert validate_body.get("valid") is True
    assert (
        validate_body.get("cfg", {})
        .get("multi_timeframe", {})
        .get("regime_intelligence", {})
        .get("authority_mode")
        == "regime_module"
    )
    assert "regime_unified" not in (validate_body.get("cfg", {}) or {})

    monkeypatch.setenv("BEARER_TOKEN", "test-secret")

    unauthorized = client.post(
        "/config/runtime/propose",
        json={
            "patch": _ri_authority_patch(),
            "actor": "test",
            "expected_version": 0,
        },
    )
    assert unauthorized.status_code == 401

    accepted = client.post(
        "/config/runtime/propose",
        headers={"Authorization": "Bearer test-secret"},
        json={
            "patch": _ri_authority_patch(),
            "actor": "test",
            "expected_version": 0,
        },
    )
    assert accepted.status_code == 200
    accepted_body = accepted.json()
    assert int(accepted_body.get("version") or -1) == 1
    assert accepted_body.get("cfg", {}).get("strategy_family") == "ri"
    assert (
        accepted_body.get("cfg", {})
        .get("multi_timeframe", {})
        .get("regime_intelligence", {})
        .get("authority_mode")
        == "regime_module"
    )
    assert "regime_unified" not in (accepted_body.get("cfg", {}) or {})

    persisted = json.loads(tmp_runtime_path.read_text(encoding="utf-8"))
    assert persisted["cfg"]["strategy_family"] == "ri"
    assert persisted["cfg"]["multi_timeframe"]["regime_intelligence"]["authority_mode"] == "regime_module"
    assert "regime_unified" not in persisted["cfg"]
    assert tmp_audit_path.exists()

    rejected = client.post(
        "/config/runtime/propose",
        headers={"Authorization": "Bearer test-secret"},
        json={
            "patch": {"warmup_bars": 12},
            "actor": "test",
            "expected_version": 1,
        },
    )
    assert rejected.status_code == 400
    assert rejected.json() == {"detail": "non_whitelisted_field"}

    conflict = client.post(
        "/config/runtime/propose",
        headers={"Authorization": "Bearer test-secret"},
        json={
            "patch": _legacy_runtime_patch(),
            "actor": "test",
            "expected_version": 0,
        },
    )
    assert conflict.status_code == 409
    assert conflict.json() == {"detail": "version_conflict"}

    _assert_file_unchanged(repo_runtime_path, *runtime_before)
    _assert_file_unchanged(repo_audit_path, *audit_before)
    _assert_file_unchanged(repo_seed_path, *seed_before)
