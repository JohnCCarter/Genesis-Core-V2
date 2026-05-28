from __future__ import annotations

import json
from typing import Any

from core.bootstrap.backtest_smoke import run_backtest_fixture_smoke
from core.bootstrap.champion_smoke import run_champion_smoke
from core.bootstrap.evaluate_champion_smoke import run_evaluate_champion_smoke
from core.bootstrap.fixture_smoke import run_fixture_smoke
from core.bootstrap.model_smoke import run_model_smoke


def run_smoke_suite() -> dict[str, Any]:
    fixture = run_fixture_smoke()
    champion = run_champion_smoke()
    evaluate_champion = run_evaluate_champion_smoke()
    model = run_model_smoke()
    backtest = run_backtest_fixture_smoke()
    return {
        "suite": "runtime_smoke_suite_v1",
        "checks": {
            "fixture_smoke": "passed",
            "champion_smoke": "passed",
            "evaluate_champion_smoke": "passed",
            "model_smoke": "passed",
            "backtest_smoke": "passed",
        },
        "fixture_smoke": fixture,
        "champion_smoke": champion,
        "evaluate_champion_smoke": evaluate_champion,
        "model_smoke": model,
        "backtest_smoke": backtest,
    }


def main() -> int:
    print(json.dumps(run_smoke_suite(), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
