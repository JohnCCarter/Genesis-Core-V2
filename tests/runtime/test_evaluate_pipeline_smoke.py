from __future__ import annotations

from types import SimpleNamespace


def _synthetic_candles(n: int = 80) -> dict[str, list[float]]:
    close = [100.0 + (i * 0.5) for i in range(n)]
    open_ = [close[0]] + close[:-1]
    high = [max(o, c) + 0.5 for o, c in zip(open_, close, strict=False)]
    low = [min(o, c) - 0.5 for o, c in zip(open_, close, strict=False)]
    volume = [100.0] * n
    timestamp = [float(i * 3600) for i in range(n)]
    return {
        "timestamp": timestamp,
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
    }


def test_runtime_seed_evaluate_pipeline_smoke(monkeypatch) -> None:
    monkeypatch.setenv("GENESIS_DISABLE_METRICS", "1")

    from core.strategy import evaluate as evaluate_mod

    dummy_champion = SimpleNamespace(config={}, source="seed_dummy")
    monkeypatch.setattr(
        evaluate_mod.champion_loader,
        "load_cached",
        lambda *_args, **_kwargs: dummy_champion,
    )
    monkeypatch.setattr(
        evaluate_mod,
        "predict_proba_for",
        lambda *_args, **_kwargs: (
            {"buy": 0.55, "sell": 0.45},
            {"schema": [], "versions": {}},
        ),
    )
    monkeypatch.setattr(
        evaluate_mod,
        "compute_confidence",
        lambda *_args, **_kwargs: (
            {"buy": 0.55, "sell": 0.45, "overall": 0.55},
            {"versions": {}},
        ),
    )
    monkeypatch.setattr(
        evaluate_mod,
        "decide",
        lambda *_args, **_kwargs: (
            "NONE",
            {"versions": {}, "reasons": [], "state_out": {}, "size": 0.0},
        ),
    )

    candles = _synthetic_candles()
    configs = {
        "_global_index": len(candles["close"]) - 1,
        "thresholds": {
            "entry_conf_overall": 0.5,
            "regime_proba": {"balanced": 0.55},
        },
        "gates": {"hysteresis_steps": 2, "cooldown_bars": 0},
        "risk": {"risk_map": [[0.5, 0.01], [0.6, 0.02]]},
        "ev": {"R_default": 1.5},
        "precomputed_features": {"ema_50": list(candles["close"])},
    }

    result, meta = evaluate_mod.evaluate_pipeline(
        candles,
        policy={"symbol": "tBTCUSD", "timeframe": "1h"},
        configs=configs,
        state={},
    )

    assert result["action"] == "NONE"
    assert isinstance(result.get("features"), dict)
    assert result.get("regime") in {"bull", "bear", "ranging", "balanced"}
    assert meta.get("decision", {}).get("size") == 0.0
    assert meta.get("champion", {}).get("source") == "explicit_backtest_config"
