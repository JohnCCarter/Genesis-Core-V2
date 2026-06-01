from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from core.bootstrap.champion_smoke import DEFAULT_CHAMPION_FIXTURE_PATH
from core.bootstrap.fixture_smoke import load_fixture
from core.strategy import evaluate as evaluate_mod
from core.strategy.champion_loader import ChampionLoader
from core.strategy.model_registry import ModelRegistry
from core.strategy.prob_model import predict_proba_for

REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_MODEL_ROOT = REPO_ROOT / "registry" / "fixtures" / "model_registry"


def run_evaluate_champion_smoke(path: Path | None = None) -> dict[str, object]:
    fixture_path = Path(path) if path is not None else DEFAULT_CHAMPION_FIXTURE_PATH
    runtime_fixture = load_fixture()
    candles = dict(runtime_fixture.get("candles") or {})
    policy = dict(runtime_fixture.get("policy") or {})
    configs = {
        "precomputed_features": {"ema_50": list(candles.get("close") or [])},
    }
    captured: dict[str, object] = {}

    def _fake_extract_features_live(candles, *, config, timeframe, symbol):
        _ = candles
        captured["config"] = config
        captured["timeframe"] = timeframe
        captured["symbol"] = symbol
        return {"ema_50": 1.0}, {"reasons": [], "htf_fibonacci": {}, "ltf_fibonacci": {}}

    previous_registry = getattr(predict_proba_for, "_registry", None)
    predict_proba_for._registry = ModelRegistry(root=FIXTURE_MODEL_ROOT)
    try:
        with (
            patch.object(
                evaluate_mod,
                "champion_loader",
                ChampionLoader(champions_dir=fixture_path.parent),
            ),
            patch.object(
                evaluate_mod,
                "extract_features_live",
                new=_fake_extract_features_live,
            ),
            patch.object(
                evaluate_mod,
                "_detect_authoritative_regime",
                lambda *_args, **_kwargs: "balanced",
            ),
            patch.object(
                evaluate_mod,
                "_detect_shadow_regime_from_regime_module",
                lambda *_args, **_kwargs: "balanced",
            ),
            patch.object(
                evaluate_mod,
                "compute_confidence",
                lambda *_args, **_kwargs: (
                    {"buy": 0.55, "sell": 0.45, "overall": 0.55},
                    {"versions": {"confidence": "v1"}},
                ),
            ),
            patch.object(
                evaluate_mod,
                "compute_htf_regime",
                lambda *_args, **_kwargs: "balanced",
            ),
            patch.object(
                evaluate_mod,
                "decide",
                lambda *_args, **_kwargs: (
                    "NONE",
                    {"versions": {"decision": "v1"}, "reasons": [], "state_out": {}, "size": 0.0},
                ),
            ),
        ):
            result, meta = evaluate_mod.evaluate_pipeline(
                candles,
                policy=policy,
                configs=configs,
                state={},
            )
    finally:
        if previous_registry is None:
            delattr(predict_proba_for, "_registry")
        else:
            predict_proba_for._registry = previous_registry

    effective_config = dict(captured.get("config") or {})
    normalized_source = str(meta.get("champion", {}).get("source") or "").replace("\\", "/")
    proba_versions = dict((meta.get("proba") or {}).get("versions") or {})

    return {
        "fixture_path": str(fixture_path.resolve()),
        "symbol": captured.get("symbol"),
        "timeframe": captured.get("timeframe"),
        "action": result.get("action"),
        "buy_proba": (result.get("probas") or {}).get("buy"),
        "sell_proba": (result.get("probas") or {}).get("sell"),
        "champion_source": normalized_source,
        "prob_model_version": proba_versions.get("prob_model_version"),
        "calibration_version": proba_versions.get("calibration_version"),
        "regime_aware_calibration": proba_versions.get("regime_aware_calibration"),
        "model_schema": list((meta.get("proba") or {}).get("schema") or []),
        "threshold_entry_conf_overall": (effective_config.get("thresholds") or {}).get(
            "entry_conf_overall"
        ),
        "risk_map_rows": len((effective_config.get("risk") or {}).get("risk_map") or []),
        "meta_note": (effective_config.get("meta") or {}).get("note"),
        "precomputed_feature_keys": sorted(
            (effective_config.get("precomputed_features") or {}).keys()
        ),
    }


def main() -> int:
    print(json.dumps(run_evaluate_champion_smoke(), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
