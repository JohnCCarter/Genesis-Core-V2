from __future__ import annotations

import asyncio
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest


def _load_fetch_script_module():
    repo_root = Path(__file__).resolve().parents[2]
    script_path = repo_root / "scripts" / "data" / "fetch_historical.py"
    spec = importlib.util.spec_from_file_location("genesis_v2_fetch_historical_script", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_local_fetch_historical_script_prints_runtime_config() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "data" / "fetch_historical.py"),
            "--print-config",
            "--from-raw-json",
            "--symbol",
            "tBTCUSD",
            "--timeframes",
            "1m",
            "1D",
            "--limit",
            "250",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["symbol"] == "tBTCUSD"
    assert payload["timeframes"] == ["1m", "1D"]
    assert payload["limit"] == 250
    assert payload["timeout"] == 20.0
    assert payload["mode"] == "from_raw_json"
    assert (
        payload["raw_json_dir"]
        .replace("\\", "/")
        .endswith("/Genesis-Core-V2/data/raw/bitfinex/candles")
    )
    assert payload["raw_frozen_dir"].replace("\\", "/").endswith("/Genesis-Core-V2/data/raw")


def test_local_fetch_historical_script_writes_json_and_parquet(tmp_path: Path) -> None:
    module = _load_fetch_script_module()
    historical_candles_mod = module._resolve_historical_candles_module()
    calls: list[dict[str, object]] = []

    class DummyResponse:
        def json(self):
            return [
                [1717203600000, 11.0, 12.5, 13.0, 10.5, 101.0],
                [1717200000000, 10.0, 11.5, 12.0, 9.5, 100.0],
            ]

    class DummyClient:
        async def public_request(self, **kwargs):
            calls.append(kwargs)
            return DummyResponse()

    manifest = asyncio.run(
        historical_candles_mod.fetch_and_store_historical_candles(
            repo_root=tmp_path,
            symbol="tBTCUSD",
            timeframes=["1h", "1D"],
            limit=5,
            timeout=7.5,
            client_factory=lambda: DummyClient(),
        )
    )

    json_path = tmp_path / "data" / "raw" / "bitfinex" / "candles" / "tBTCUSD_1h.json"
    parquet_path = tmp_path / "data" / "raw" / "tBTCUSD_1h_frozen.parquet"
    manifest_path = tmp_path / "data" / "raw" / "bitfinex" / "candles" / "tBTCUSD_manifest.json"

    assert json_path.exists()
    assert parquet_path.exists()
    assert manifest_path.exists()
    assert [call["endpoint"] for call in calls] == [
        "candles/trade:1h:tBTCUSD/hist",
        "candles/trade:1D:tBTCUSD/hist",
    ]
    assert all(call["params"] == {"limit": 5, "sort": -1} for call in calls)
    assert all(call["timeout"] == 7.5 for call in calls)

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["symbol"] == "tBTCUSD"
    assert payload["timeframe"] == "1h"
    assert payload["candles"][0]["timestamp_ms"] == 1717200000000
    assert payload["candles"][1]["timestamp_ms"] == 1717203600000

    frame = pd.read_parquet(parquet_path, engine="pyarrow")
    assert list(frame.columns) == ["timestamp", "open", "high", "low", "close", "volume"]
    assert frame["close"].tolist() == [11.5, 12.5]
    assert manifest["files"]["1h"]["rows"] == 2
    assert manifest["files"]["1h"]["json_path"] == "data/raw/bitfinex/candles/tBTCUSD_1h.json"
    assert manifest["files"]["1h"]["parquet_path"] == "data/raw/tBTCUSD_1h_frozen.parquet"


def test_local_fetch_historical_script_converts_existing_raw_json_to_parquet(
    tmp_path: Path,
) -> None:
    module = _load_fetch_script_module()
    historical_candles_mod = module._resolve_historical_candles_module()
    raw_dir = tmp_path / "data" / "raw" / "bitfinex" / "candles"
    raw_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "symbol": "tBTCUSD",
        "timeframe": "1D",
        "limit": 2,
        "retrieved_at_utc": "2026-06-01T00:00:00+00:00",
        "source": "bitfinex_v2_rest_hist",
        "candles": [
            {
                "timestamp_ms": 1717200000000,
                "timestamp_utc": "2024-06-01T00:00:00+00:00",
                "open": 10.0,
                "high": 12.0,
                "low": 9.5,
                "close": 11.5,
                "volume": 100.0,
            },
            {
                "timestamp_ms": 1717286400000,
                "timestamp_utc": "2024-06-02T00:00:00+00:00",
                "open": 11.5,
                "high": 13.0,
                "low": 10.5,
                "close": 12.5,
                "volume": 101.0,
            },
        ],
    }
    (raw_dir / "tBTCUSD_1D.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    manifest = historical_candles_mod.convert_raw_json_dumps_to_parquet(
        repo_root=tmp_path,
        symbol="tBTCUSD",
        timeframes=["1D"],
    )

    parquet_path = tmp_path / "data" / "raw" / "tBTCUSD_1D_frozen.parquet"
    assert parquet_path.exists()
    frame = pd.read_parquet(parquet_path, engine="pyarrow")
    assert frame["close"].tolist() == [11.5, 12.5]
    assert manifest["mode"] == "from_raw_json"
    assert manifest["files"]["1D"]["rows"] == 2


def test_build_candles_frame_rejects_invalid_candle_ranges() -> None:
    module = _load_fetch_script_module()
    historical_candles_mod = module._resolve_historical_candles_module()

    invalid_candles = [
        {
            "timestamp_ms": 1717200000000,
            "timestamp_utc": "2024-06-01T00:00:00+00:00",
            "open": 10.0,
            "high": 9.0,
            "low": 9.5,
            "close": 9.75,
            "volume": 100.0,
        }
    ]

    with pytest.raises(Exception, match="high must be >= low|high must be >= open"):
        historical_candles_mod.build_candles_frame(invalid_candles)


def test_local_fetch_historical_script_prints_duckdb_runtime_config() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "data" / "fetch_historical.py"),
            "--print-config",
            "--duckdb-summary",
            "--symbol",
            "tBTCUSD",
            "--timeframes",
            "1h",
            "1D",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["mode"] == "duckdb_summary"
    assert payload["timeframes"] == ["1h", "1D"]


def test_local_fetch_historical_script_duckdb_summary_reads_existing_parquet(
    tmp_path: Path,
) -> None:
    pytest.importorskip("duckdb")

    module = _load_fetch_script_module()
    historical_candles_mod = module._resolve_historical_candles_module()
    candles = [
        {
            "timestamp_ms": 1717200000000,
            "timestamp_utc": "2024-06-01T00:00:00+00:00",
            "open": 10.0,
            "high": 12.0,
            "low": 9.5,
            "close": 11.5,
            "volume": 100.0,
        },
        {
            "timestamp_ms": 1717286400000,
            "timestamp_utc": "2024-06-02T00:00:00+00:00",
            "open": 11.5,
            "high": 13.0,
            "low": 10.5,
            "close": 12.5,
            "volume": 101.0,
        },
    ]

    historical_candles_mod.write_candle_artifacts(
        repo_root=tmp_path,
        symbol="tBTCUSD",
        timeframe="1h",
        candles=candles,
        limit=2,
        source="test_fixture",
    )

    manifest = historical_candles_mod.summarize_candle_parquet_with_duckdb(
        repo_root=tmp_path,
        symbol="tBTCUSD",
        timeframes=["1h"],
    )

    assert manifest["mode"] == "duckdb_summary"
    assert manifest["files"]["1h"]["rows"] == 2
    assert manifest["files"]["1h"]["parquet_path"] == "data/raw/tBTCUSD_1h_frozen.parquet"
    assert manifest["files"]["1h"]["min_close"] == 11.5
    assert manifest["files"]["1h"]["max_close"] == 12.5
    assert manifest["files"]["1h"]["avg_close"] == 12.0
    assert manifest["files"]["1h"]["total_volume"] == 201.0
