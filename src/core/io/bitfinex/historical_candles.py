from __future__ import annotations

import json
from collections.abc import Callable, Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
import pandera.pandas as pa
from pandera import Check

from core.io.bitfinex.exchange_client import get_exchange_client
from core.utils import raw_candles_dir, raw_frozen_candles_path, timeframe_filename_suffix

DEFAULT_LIMIT = 1000
DEFAULT_TIMEOUT = 20.0
DEFAULT_SOURCE = "bitfinex_v2_rest_hist"
DEFAULT_TIMEFRAMES = ["1m", "5m", "15m", "30m", "1h", "3h", "6h", "12h", "1D", "7D", "14D"]

ClientFactory = Callable[[], Any]

_UTC_TIMESTAMP_DTYPE = pd.DatetimeTZDtype(tz="UTC")
_FLOAT_DTYPE = "float64"

_CANDLES_FRAME_SCHEMA = pa.DataFrameSchema(
    {
        "timestamp": pa.Column(
            _UTC_TIMESTAMP_DTYPE,
            nullable=False,
            checks=Check(
                lambda series: bool(series.dt.tz is not None),
                error="timestamp must be timezone-aware",
            ),
        ),
        "open": pa.Column(float, nullable=False),
        "high": pa.Column(float, nullable=False),
        "low": pa.Column(float, nullable=False),
        "close": pa.Column(float, nullable=False),
        "volume": pa.Column(float, nullable=False, checks=Check.ge(0.0)),
    },
    checks=[
        Check(lambda frame: frame["timestamp"].is_monotonic_increasing, error="timestamps must be sorted"),
        Check(lambda frame: not frame["timestamp"].duplicated().any(), error="timestamps must be unique"),
        Check(lambda frame: (frame["high"] >= frame["low"]).all(), error="high must be >= low"),
        Check(lambda frame: (frame["high"] >= frame["open"]).all(), error="high must be >= open"),
        Check(lambda frame: (frame["high"] >= frame["close"]).all(), error="high must be >= close"),
        Check(lambda frame: (frame["low"] <= frame["open"]).all(), error="low must be <= open"),
        Check(lambda frame: (frame["low"] <= frame["close"]).all(), error="low must be <= close"),
    ],
    strict=True,
    ordered=True,
)


def _empty_candles_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "timestamp": pd.Series(dtype=_UTC_TIMESTAMP_DTYPE),
            "open": pd.Series(dtype=_FLOAT_DTYPE),
            "high": pd.Series(dtype=_FLOAT_DTYPE),
            "low": pd.Series(dtype=_FLOAT_DTYPE),
            "close": pd.Series(dtype=_FLOAT_DTYPE),
            "volume": pd.Series(dtype=_FLOAT_DTYPE),
        }
    )


def validate_candles_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return _CANDLES_FRAME_SCHEMA.validate(frame)


def normalize_timeframes(timeframes: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    for value in timeframes:
        for item in str(value).split(","):
            timeframe = item.strip()
            if timeframe and timeframe not in normalized:
                normalized.append(timeframe)

    if not normalized:
        raise ValueError("At least one timeframe is required")

    return normalized


def raw_json_candles_path(symbol: str, timeframe: str) -> Path:
    suffix = timeframe_filename_suffix(timeframe)
    return raw_candles_dir() / f"{symbol}_{suffix}.json"


def raw_candles_manifest_path(symbol: str) -> Path:
    return raw_candles_dir() / f"{symbol}_manifest.json"


def _timestamp_iso_from_ms(timestamp_ms: int) -> str:
    return datetime.fromtimestamp(timestamp_ms / 1000, tz=UTC).isoformat()


def _normalize_candle_record(record: dict[str, Any]) -> dict[str, object]:
    timestamp_ms_raw = record.get("timestamp_ms")
    if timestamp_ms_raw is None:
        timestamp_utc = record.get("timestamp_utc")
        if timestamp_utc is None:
            raise ValueError("Candle record must include timestamp_ms or timestamp_utc")
        timestamp_ms = int(datetime.fromisoformat(str(timestamp_utc)).timestamp() * 1000)
    else:
        timestamp_ms = int(timestamp_ms_raw)

    return {
        "timestamp_ms": timestamp_ms,
        "timestamp_utc": _timestamp_iso_from_ms(timestamp_ms),
        "open": float(record["open"]),
        "high": float(record["high"]),
        "low": float(record["low"]),
        "close": float(record["close"]),
        "volume": float(record["volume"]),
    }


def normalize_historical_rows(rows: list[Any]) -> list[dict[str, object]]:
    normalized: list[dict[str, object]] = []
    for row in rows:
        if not isinstance(row, list) or len(row) < 6:
            continue
        timestamp_ms = int(row[0])
        normalized.append(
            {
                "timestamp_ms": timestamp_ms,
                "timestamp_utc": _timestamp_iso_from_ms(timestamp_ms),
                "open": float(row[1]),
                "high": float(row[3]),
                "low": float(row[4]),
                "close": float(row[2]),
                "volume": float(row[5]),
            }
        )

    normalized.sort(key=lambda item: int(item["timestamp_ms"]))
    return normalized


def build_candles_frame(candles: list[dict[str, object]]) -> pd.DataFrame:
    if not candles:
        return validate_candles_frame(_empty_candles_frame())

    frame = pd.DataFrame.from_records(candles)
    frame["timestamp"] = pd.to_datetime(frame["timestamp_ms"], unit="ms", utc=True)
    frame = frame[["timestamp", "open", "high", "low", "close", "volume"]]
    frame = frame.astype(
        {
            "open": _FLOAT_DTYPE,
            "high": _FLOAT_DTYPE,
            "low": _FLOAT_DTYPE,
            "close": _FLOAT_DTYPE,
            "volume": _FLOAT_DTYPE,
        }
    )
    frame = frame.sort_values("timestamp").drop_duplicates(subset=["timestamp"], keep="last")
    frame = frame.reset_index(drop=True)
    return validate_candles_frame(frame)


def load_raw_candle_payload(repo_root: Path, symbol: str, timeframe: str) -> dict[str, Any]:
    raw_path = repo_root / raw_json_candles_path(symbol, timeframe)
    payload = json.loads(raw_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected dict payload in {raw_path}")
    return payload


def load_raw_candles(
    repo_root: Path, symbol: str, timeframe: str
) -> tuple[list[dict[str, object]], dict[str, Any]]:
    payload = load_raw_candle_payload(repo_root, symbol, timeframe)
    candles = payload.get("candles")
    if isinstance(candles, list):
        normalized = [_normalize_candle_record(item) for item in candles if isinstance(item, dict)]
        normalized.sort(key=lambda item: int(item["timestamp_ms"]))
        if normalized:
            return normalized, payload

    if all(key in payload for key in ("open", "high", "low", "close", "volume")):
        raise ValueError(
            "Raw candle payload is missing timestamps; re-fetch with scripts/data/fetch_historical.py"
        )

    raise ValueError(
        f"Unsupported raw candle payload for {symbol} {timeframe}: expected payload['candles'] list"
    )


def _relative_path(path: Path, repo_root: Path) -> str:
    return str(path.relative_to(repo_root)).replace("\\", "/")


def write_candle_artifacts(
    *,
    repo_root: Path,
    symbol: str,
    timeframe: str,
    candles: list[dict[str, object]],
    limit: int,
    source: str,
    retrieved_at_utc: str | None = None,
    write_raw_json: bool = True,
) -> dict[str, object]:
    repo_root = repo_root.resolve()
    raw_path = repo_root / raw_json_candles_path(symbol, timeframe)
    parquet_path = repo_root / raw_frozen_candles_path(symbol, timeframe)
    retrieved_at = retrieved_at_utc or datetime.now(UTC).isoformat()

    raw_path.parent.mkdir(parents=True, exist_ok=True)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)

    if write_raw_json:
        payload = {
            "symbol": symbol,
            "timeframe": timeframe,
            "limit": int(limit),
            "retrieved_at_utc": retrieved_at,
            "source": source,
            "candles": candles,
        }
        raw_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    frame = build_candles_frame(candles)
    frame.to_parquet(parquet_path, index=False, engine="pyarrow")

    first = candles[0] if candles else {}
    last = candles[-1] if candles else {}
    return {
        "json_path": _relative_path(raw_path, repo_root),
        "parquet_path": _relative_path(parquet_path, repo_root),
        "rows": len(candles),
        "first_timestamp_utc": first.get("timestamp_utc"),
        "last_timestamp_utc": last.get("timestamp_utc"),
        "first_close": first.get("close"),
        "last_close": last.get("close"),
        "source": source,
    }


def write_manifest(repo_root: Path, symbol: str, manifest: dict[str, Any]) -> Path:
    repo_root = repo_root.resolve()
    manifest_path = repo_root / raw_candles_manifest_path(symbol)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def summarize_candle_parquet_with_duckdb(
    *,
    repo_root: Path,
    symbol: str,
    timeframes: Iterable[str],
) -> dict[str, Any]:
    import duckdb

    normalized_timeframes = normalize_timeframes(timeframes)
    repo_root = repo_root.resolve()
    manifest: dict[str, Any] = {
        "symbol": symbol,
        "mode": "duckdb_summary",
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
        "files": {},
    }

    connection = duckdb.connect(database=":memory:")
    try:
        for timeframe in normalized_timeframes:
            parquet_path = repo_root / raw_frozen_candles_path(symbol, timeframe)
            if not parquet_path.exists():
                raise FileNotFoundError(f"Missing candle parquet for {symbol} {timeframe}: {parquet_path}")

            summary = connection.execute(
                """
                SELECT
                    COUNT(*) AS rows,
                    MIN(timestamp) AS first_timestamp,
                    MAX(timestamp) AS last_timestamp,
                    MIN(close) AS min_close,
                    MAX(close) AS max_close,
                    AVG(close) AS avg_close,
                    SUM(volume) AS total_volume
                FROM read_parquet(?)
                """,
                [str(parquet_path)],
            ).fetchone()
            assert summary is not None

            manifest["files"][timeframe] = {
                "parquet_path": _relative_path(parquet_path, repo_root),
                "rows": int(summary[0]),
                "first_timestamp_utc": summary[1].isoformat() if summary[1] is not None else None,
                "last_timestamp_utc": summary[2].isoformat() if summary[2] is not None else None,
                "min_close": float(summary[3]) if summary[3] is not None else None,
                "max_close": float(summary[4]) if summary[4] is not None else None,
                "avg_close": float(summary[5]) if summary[5] is not None else None,
                "total_volume": float(summary[6]) if summary[6] is not None else None,
            }
    finally:
        connection.close()

    return manifest


async def fetch_historical_candles(
    *,
    symbol: str,
    timeframe: str,
    limit: int = DEFAULT_LIMIT,
    timeout: float = DEFAULT_TIMEOUT,
    client_factory: ClientFactory | None = None,
) -> list[dict[str, object]]:
    safe_limit = max(1, min(int(limit), DEFAULT_LIMIT))
    endpoint = f"candles/trade:{timeframe}:{symbol}/hist"
    response = await (client_factory or get_exchange_client)().public_request(
        method="GET",
        endpoint=endpoint,
        params={"limit": safe_limit, "sort": -1},
        timeout=timeout,
    )
    payload = response.json()
    if not isinstance(payload, list):
        raise TypeError(f"Unexpected Bitfinex candles payload: {type(payload).__name__}")
    return normalize_historical_rows(payload)


async def fetch_and_store_historical_candles(
    *,
    repo_root: Path,
    symbol: str,
    timeframes: Iterable[str],
    limit: int = DEFAULT_LIMIT,
    timeout: float = DEFAULT_TIMEOUT,
    client_factory: ClientFactory | None = None,
) -> dict[str, Any]:
    normalized_timeframes = normalize_timeframes(timeframes)
    safe_limit = max(1, min(int(limit), DEFAULT_LIMIT))
    manifest: dict[str, Any] = {
        "symbol": symbol,
        "limit": safe_limit,
        "mode": "fetch",
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
        "files": {},
    }

    for timeframe in normalized_timeframes:
        candles = await fetch_historical_candles(
            symbol=symbol,
            timeframe=timeframe,
            limit=safe_limit,
            timeout=timeout,
            client_factory=client_factory,
        )
        manifest["files"][timeframe] = write_candle_artifacts(
            repo_root=repo_root,
            symbol=symbol,
            timeframe=timeframe,
            candles=candles,
            limit=safe_limit,
            source=DEFAULT_SOURCE,
        )

    write_manifest(repo_root, symbol, manifest)
    return manifest


def convert_raw_json_dumps_to_parquet(
    *,
    repo_root: Path,
    symbol: str,
    timeframes: Iterable[str],
) -> dict[str, Any]:
    normalized_timeframes = normalize_timeframes(timeframes)
    manifest: dict[str, Any] = {
        "symbol": symbol,
        "mode": "from_raw_json",
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
        "files": {},
    }

    for timeframe in normalized_timeframes:
        candles, payload = load_raw_candles(repo_root, symbol, timeframe)
        limit = int(payload.get("limit") or len(candles))
        source = str(payload.get("source") or "raw_json_conversion")
        manifest["files"][timeframe] = write_candle_artifacts(
            repo_root=repo_root,
            symbol=symbol,
            timeframe=timeframe,
            candles=candles,
            limit=limit,
            source=source,
            retrieved_at_utc=str(payload.get("retrieved_at_utc") or manifest["retrieved_at_utc"]),
            write_raw_json=False,
        )

    write_manifest(repo_root, symbol, manifest)
    return manifest
