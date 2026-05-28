from __future__ import annotations

import pandas as pd

from core.backtest.engine import BacktestEngine
from core.bootstrap.fixture_smoke import load_fixture


class _DummyChampionCfg:
    def __init__(self) -> None:
        self.config: dict = {}
        self.source = "seed_dummy"
        self.version = "0"
        self.checksum = "seed_dummy"
        self.loaded_at = "now"


def _fixture_frame() -> pd.DataFrame:
    payload = load_fixture()
    candles = payload["candles"]
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(candles["timestamp"], unit="s"),
            "open": candles["open"],
            "high": candles["high"],
            "low": candles["low"],
            "close": candles["close"],
            "volume": candles["volume"],
        }
    )


def test_backtest_engine_fixture_smoke_is_deterministic(monkeypatch) -> None:
    monkeypatch.setenv("GENESIS_DISABLE_METRICS", "1")
    monkeypatch.setattr("core.backtest.engine_results.shutil.which", lambda *_args, **_kwargs: None)

    class _QuietProgress:
        def update(self, *_args, **_kwargs) -> None:
            return None

        def close(self) -> None:
            return None

    monkeypatch.setattr("core.backtest.engine.tqdm", lambda *_args, **_kwargs: _QuietProgress())

    def _fake_evaluate_pipeline(*, candles, policy, configs, state):
        _ = (candles, policy, configs)
        already_entered = bool((state or {}).get("entered"))
        if already_entered:
            result = {"action": "NONE", "confidence": 0.5, "regime": "BALANCED"}
            meta = {
                "decision": {"size": 0.0, "reasons": [], "state_out": {"entered": True}},
                "features": {},
            }
            return result, meta

        result = {"action": "LONG", "confidence": {"overall": 0.6}, "regime": {"name": "BALANCED"}}
        meta = {
            "decision": {
                "size": 0.01,
                "reasons": ["FIXTURE_ENTRY"],
                "state_out": {"entered": True},
            },
            "features": {},
        }
        return result, meta

    monkeypatch.setattr("core.backtest.engine.evaluate_pipeline", _fake_evaluate_pipeline)

    payload = load_fixture()
    policy = dict(payload["policy"])
    configs = dict(payload["configs"])
    configs["exit"] = {"enabled": False}

    engine = BacktestEngine(
        symbol=str(policy["symbol"]),
        timeframe=str(policy["timeframe"]),
        warmup_bars=0,
        fast_window=False,
    )
    engine.champion_loader.load_cached = lambda *_args, **_kwargs: _DummyChampionCfg()
    engine.candles_df = _fixture_frame()

    first = engine.run(configs=configs)
    second = engine.run(configs=configs)

    first_trades = first.get("trades") or []
    second_trades = second.get("trades") or []

    assert first.get("error") is None
    assert second.get("error") is None
    assert len(first_trades) == 1
    assert first_trades == second_trades
    assert first_trades[0].get("entry_reasons") == ["FIXTURE_ENTRY"]
    assert (first.get("summary") or {}) == (second.get("summary") or {})
    assert (first.get("metrics") or {}) == (second.get("metrics") or {})
