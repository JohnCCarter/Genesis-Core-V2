from __future__ import annotations

import sys
from pathlib import Path

LOCAL_SRC_ROOT = Path(__file__).resolve().parents[1]


def _prefer_local_src() -> None:
    normalized_local = str(LOCAL_SRC_ROOT.resolve())
    filtered: list[str] = []
    for entry in sys.path:
        try:
            normalized_entry = str(Path(entry).resolve())
        except Exception:
            normalized_entry = entry
        if normalized_entry == normalized_local:
            continue
        filtered.append(entry)
    sys.path[:] = [str(LOCAL_SRC_ROOT), *filtered]


_prefer_local_src()

from core.bootstrap.backtest_smoke import main as backtest_smoke_main
from core.bootstrap.champion_smoke import main as champion_smoke_main
from core.bootstrap.evaluate_champion_smoke import main as evaluate_champion_smoke_main
from core.bootstrap.fixture_smoke import main as fixture_smoke_main
from core.bootstrap.model_smoke import main as model_smoke_main
from core.bootstrap.smoke_suite import main as smoke_suite_main

__all__ = [
    "champion_smoke_main",
    "evaluate_champion_smoke_main",
    "fixture_smoke_main",
    "backtest_smoke_main",
    "model_smoke_main",
    "smoke_suite_main",
]
