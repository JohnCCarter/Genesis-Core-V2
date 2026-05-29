from __future__ import annotations

import os
from pathlib import Path

import pytest
import yaml

from core.pipeline import GenesisPipeline


def test_pipeline_uses_backtest_defaults_for_costs(monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    defaults = yaml.safe_load((repo_root / "config" / "backtest_defaults.yaml").read_text(encoding="utf-8"))

    assert defaults["commission"] == pytest.approx(0.0)
    assert defaults["slippage"] == pytest.approx(0.0005)

    monkeypatch.setenv("GENESIS_PRECOMPUTE_FEATURES", "1")
    monkeypatch.setenv("GENESIS_FAST_WINDOW", "1")

    pipeline = GenesisPipeline()
    engine = pipeline.create_engine(symbol="tBTCUSD", timeframe="3h")

    assert engine.position_tracker.commission_rate == pytest.approx(0.0)
    assert engine.position_tracker.slippage_rate == pytest.approx(0.0005)


def test_pipeline_setup_environment_sets_seed_and_canonical_env(monkeypatch: pytest.MonkeyPatch) -> None:
    original_env = os.environ.copy()

    try:
        for key in (
            "GENESIS_RANDOM_SEED",
            "GENESIS_FAST_WINDOW",
            "GENESIS_PRECOMPUTE_FEATURES",
            "GENESIS_MODE_EXPLICIT",
            "GENESIS_FAST_HASH",
            "PYTHONHASHSEED",
        ):
            os.environ.pop(key, None)

        pipeline = GenesisPipeline()
        pipeline.setup_environment(seed=123)

        assert os.environ["GENESIS_RANDOM_SEED"] == "123"
        assert os.environ["PYTHONHASHSEED"] == "123"
        assert os.environ["GENESIS_FAST_WINDOW"] == "1"
        assert os.environ["GENESIS_PRECOMPUTE_FEATURES"] == "1"
        assert os.environ["GENESIS_FAST_HASH"] == "0"
    finally:
        os.environ.clear()
        os.environ.update(original_env)
