from __future__ import annotations

from core.bootstrap.backtest_smoke import run_backtest_fixture_smoke


def test_runtime_backtest_fixture_bootstrap_smoke_runs_end_to_end() -> None:
    result = run_backtest_fixture_smoke()

    assert result["bar_count"] == 120
    assert result["trade_count"] == 1
    assert result["entry_reasons"] == ["FIXTURE_ENTRY"]
    assert result["deterministic"] is True
    assert result["git_hash"] == "unknown"
    assert result["final_capital"] is not None
