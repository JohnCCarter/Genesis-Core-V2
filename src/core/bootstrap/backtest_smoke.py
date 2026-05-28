from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pandas as pd

from core.backtest.engine import BacktestEngine
from core.bootstrap.fixture_smoke import DEFAULT_FIXTURE_PATH, load_fixture


class _DummyChampionCfg:
    def __init__(self) -> None:
        self.config: dict = {}
        self.source = "seed_dummy"
        self.version = "0"
        self.checksum = "seed_dummy"
        self.loaded_at = "now"


class _QuietProgress:
    def update(self, *_args, **_kwargs) -> None:
        return None

    def close(self) -> None:
        return None


def _quiet_tqdm(*_args, **_kwargs) -> _QuietProgress:
    return _QuietProgress()


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


def _fixture_frame(payload: dict[str, Any]) -> pd.DataFrame:
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


def run_backtest_fixture_smoke(path: Path | None = None) -> dict[str, Any]:
    fixture_path = Path(path) if path is not None else DEFAULT_FIXTURE_PATH
    payload = load_fixture(fixture_path)
    policy = dict(payload["policy"])
    configs = dict(payload["configs"])
    configs["exit"] = {"enabled": False}

    engine = BacktestEngine(
        symbol=str(policy["symbol"]),
        timeframe=str(policy["timeframe"]),
        warmup_bars=0,
        fast_window=False,
    )
    engine.candles_df = _fixture_frame(payload)

    with patch.object(
        engine.champion_loader,
        "load_cached",
        return_value=_DummyChampionCfg(),
    ), patch(
        "core.backtest.engine.evaluate_pipeline",
        new=_fake_evaluate_pipeline,
    ), patch(
        "core.backtest.engine_results.shutil.which",
        return_value=None,
    ), patch(
        "core.backtest.engine.tqdm",
        new=_quiet_tqdm,
    ):
        first = engine.run(configs=configs)
        second = engine.run(configs=configs)

    if first.get("error") is not None or second.get("error") is not None:
        raise RuntimeError(
            "Backtest fixture smoke failed: "
            f"first={first.get('error')} second={second.get('error')}"
        )

    first_trades = first.get("trades") or []
    second_trades = second.get("trades") or []
    first_summary = first.get("summary") or {}
    second_summary = second.get("summary") or {}
    first_metrics = first.get("metrics") or {}
    second_metrics = second.get("metrics") or {}

    deterministic = (
        first_trades == second_trades
        and first_summary == second_summary
        and first_metrics == second_metrics
    )
    if not deterministic:
        raise AssertionError("Backtest fixture smoke must be deterministic across two runs")

    return {
        "fixture_path": str(fixture_path.resolve()),
        "bar_count": len(engine.candles_df),
        "trade_count": len(first_trades),
        "entry_reasons": list(first_trades[0].get("entry_reasons") or []) if first_trades else [],
        "deterministic": deterministic,
        "git_hash": (first.get("backtest_info") or {}).get("git_hash"),
        "final_capital": first_summary.get("final_capital"),
        "total_return_pct": first_summary.get("total_return"),
    }


def main() -> int:
    print(json.dumps(run_backtest_fixture_smoke(), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
