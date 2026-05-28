from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.strategy.champion_loader import ChampionLoader

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CHAMPION_FIXTURE_PATH = (
    REPO_ROOT / "registry" / "fixtures" / "champions" / "tBTCUSD_1h.json"
)


def load_champion_fixture(path: Path | None = None) -> dict[str, Any]:
    fixture_path = Path(path) if path is not None else DEFAULT_CHAMPION_FIXTURE_PATH
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError("Champion fixture payload must be a JSON object")
    return payload


def run_champion_smoke(path: Path | None = None) -> dict[str, Any]:
    fixture_path = Path(path) if path is not None else DEFAULT_CHAMPION_FIXTURE_PATH
    payload = load_champion_fixture(fixture_path)
    loader = ChampionLoader(champions_dir=fixture_path.parent)

    first = loader.load("tBTCUSD", "1h")
    second = loader.load_cached("tBTCUSD", "1h")
    normalized_source = str(first.source).replace("\\", "/")

    return {
        "fixture_path": str(fixture_path.resolve()),
        "source": normalized_source,
        "version": first.version,
        "checksum": first.checksum,
        "cache_reused": first.checksum == second.checksum,
        "threshold_entry_conf_overall": (first.config.get("thresholds") or {}).get(
            "entry_conf_overall"
        ),
        "risk_map_rows": len((first.config.get("risk") or {}).get("risk_map") or []),
    }


def main() -> int:
    print(json.dumps(run_champion_smoke(), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
