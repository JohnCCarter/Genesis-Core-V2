from __future__ import annotations

import argparse
import asyncio
import importlib
import json
import os
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
DEFAULT_SYMBOL = "tBTCUSD"

_prefer_local_src_called = False


def _reload_local_core_package() -> None:
    for name in list(sys.modules):
        if name == "core" or name.startswith("core."):
            sys.modules.pop(name, None)
    importlib.invalidate_caches()


def _prefer_local_src() -> None:
    global _prefer_local_src_called
    if _prefer_local_src_called:
        return

    normalized_src = str(SRC_ROOT)
    normalized_repo = str(REPO_ROOT)

    if normalized_repo not in sys.path:
        sys.path.insert(0, normalized_repo)
    if normalized_src not in sys.path:
        sys.path.insert(0, normalized_src)

    existing = [entry for entry in os.environ.get("PYTHONPATH", "").split(os.pathsep) if entry]
    desired_prefix = [normalized_src, normalized_repo]
    filtered_existing = [entry for entry in existing if entry not in desired_prefix]
    os.environ["PYTHONPATH"] = os.pathsep.join([*desired_prefix, *filtered_existing])
    _reload_local_core_package()
    _prefer_local_src_called = True


def _resolve_historical_candles_module():
    _prefer_local_src()
    from core.io.bitfinex import historical_candles as historical_candles_mod

    return historical_candles_mod


def _resolve_aclose_http_client():
    _prefer_local_src()
    from core.io.bitfinex.exchange_client import aclose_http_client

    return aclose_http_client


def _resolve_raw_json_dir(output_root: Path) -> Path:
    _prefer_local_src()
    from core.utils import raw_candles_dir

    return output_root / raw_candles_dir()


def _resolve_raw_frozen_dir(output_root: Path) -> Path:
    _prefer_local_src()
    from core.utils import raw_frozen_candles_path

    return (output_root / raw_frozen_candles_path(DEFAULT_SYMBOL, "1h")).parent


def build_parser() -> argparse.ArgumentParser:
    historical_candles_mod = _resolve_historical_candles_module()
    parser = argparse.ArgumentParser(
        description="Fetch Bitfinex public candles and store local raw JSON plus raw-frozen parquet"
    )
    parser.add_argument("--symbol", default=DEFAULT_SYMBOL)
    parser.add_argument(
        "--timeframes", nargs="+", default=list(historical_candles_mod.DEFAULT_TIMEFRAMES)
    )
    parser.add_argument("--limit", type=int, default=historical_candles_mod.DEFAULT_LIMIT)
    parser.add_argument("--timeout", type=float, default=historical_candles_mod.DEFAULT_TIMEOUT)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--from-raw-json", action="store_true")
    mode_group.add_argument("--duckdb-summary", action="store_true")
    parser.add_argument("--print-config", action="store_true")
    return parser


def build_runtime_config(
    *,
    symbol: str,
    timeframes: Sequence[str],
    limit: int,
    timeout: float,
    from_raw_json: bool,
    duckdb_summary: bool,
    output_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    historical_candles_mod = _resolve_historical_candles_module()
    normalized_timeframes = historical_candles_mod.normalize_timeframes(timeframes)
    mode = "duckdb_summary" if duckdb_summary else ("from_raw_json" if from_raw_json else "fetch")
    return {
        "cwd": str(output_root.resolve()),
        "repo_root": str(output_root.resolve()),
        "src_root": str(SRC_ROOT.resolve()),
        "mode": mode,
        "symbol": symbol,
        "timeframes": normalized_timeframes,
        "limit": max(1, min(int(limit), historical_candles_mod.DEFAULT_LIMIT)),
        "timeout": float(timeout),
        "raw_json_dir": str(_resolve_raw_json_dir(output_root).resolve()),
        "raw_frozen_dir": str(_resolve_raw_frozen_dir(output_root).resolve()),
    }


def main(argv: list[str] | None = None) -> int:
    _prefer_local_src()
    historical_candles_mod = _resolve_historical_candles_module()
    args = build_parser().parse_args(argv)
    config = build_runtime_config(
        symbol=args.symbol,
        timeframes=args.timeframes,
        limit=args.limit,
        timeout=args.timeout,
        from_raw_json=bool(args.from_raw_json),
        duckdb_summary=bool(args.duckdb_summary),
    )
    if args.print_config:
        print(json.dumps(config, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    if args.duckdb_summary:
        manifest = historical_candles_mod.summarize_candle_parquet_with_duckdb(
            repo_root=REPO_ROOT,
            symbol=args.symbol,
            timeframes=args.timeframes,
        )
    elif args.from_raw_json:
        manifest = historical_candles_mod.convert_raw_json_dumps_to_parquet(
            repo_root=REPO_ROOT,
            symbol=args.symbol,
            timeframes=args.timeframes,
        )
    else:
        try:
            manifest = asyncio.run(
                historical_candles_mod.fetch_and_store_historical_candles(
                    repo_root=REPO_ROOT,
                    symbol=args.symbol,
                    timeframes=args.timeframes,
                    limit=args.limit,
                    timeout=args.timeout,
                )
            )
        finally:
            asyncio.run(_resolve_aclose_http_client()())

    print(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
