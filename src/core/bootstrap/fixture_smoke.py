from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.strategy.confidence import compute_confidence
from core.strategy.decision import decide
from core.strategy.features_asof import extract_features_backtest
from core.strategy.model_registry import ModelRegistry
from core.strategy.prob_model import predict_proba_for
from core.strategy.regime import detect_regime_from_candles

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FIXTURE_PATH = REPO_ROOT / "registry" / "fixtures" / "runtime_fixture_smoke_minimal.json"
FIXTURE_MODEL_ROOT = REPO_ROOT / "registry" / "fixtures" / "model_registry"


def load_fixture(path: Path | None = None) -> dict[str, Any]:
    fixture_path = Path(path) if path is not None else DEFAULT_FIXTURE_PATH
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError("Runtime fixture payload must be a JSON object")
    return payload


def run_fixture_smoke(path: Path | None = None) -> dict[str, Any]:
    fixture_path = Path(path) if path is not None else DEFAULT_FIXTURE_PATH
    payload = load_fixture(fixture_path)
    candles = dict(payload.get("candles") or {})
    policy = dict(payload.get("policy") or {})
    configs = dict(payload.get("configs") or {})

    timeframe = str(policy.get("timeframe") or "1h")
    symbol = str(policy.get("symbol") or "tBTCUSD")
    asof_bar = len(candles.get("close") or []) - 1
    if asof_bar < 0:
        raise ValueError("Runtime fixture must contain at least one close bar")

    features, features_meta = extract_features_backtest(
        candles,
        asof_bar,
        config=configs,
        timeframe=timeframe,
        symbol=symbol,
    )
    regime = detect_regime_from_candles(candles, config=configs)
    previous_registry = getattr(predict_proba_for, "_registry", None)
    predict_proba_for._registry = ModelRegistry(root=FIXTURE_MODEL_ROOT)
    try:
        probas, proba_meta = predict_proba_for(
            symbol,
            timeframe,
            features,
            regime=regime,
        )
    finally:
        if previous_registry is None:
            delattr(predict_proba_for, "_registry")
        else:
            predict_proba_for._registry = previous_registry
    confidence, confidence_meta = compute_confidence(probas, config=configs.get("quality"))
    action, decision_meta = decide(
        policy,
        probas=probas,
        confidence=confidence,
        regime=regime,
        state={},
        risk_ctx=configs.get("risk"),
        cfg=configs,
    )

    return {
        "fixture_path": str(fixture_path.resolve()),
        "bar_count": len(candles.get("close") or []),
        "features_count": len(features),
        "feature_reasons": list(features_meta.get("reasons", [])),
        "regime": regime,
        "probas": probas,
        "confidence": confidence,
        "action": action,
        "decision_reasons": list(decision_meta.get("reasons", [])),
        "versions": {
            "prob_model": proba_meta.get("versions", {}).get("prob_model_version"),
            "calibration": proba_meta.get("versions", {}).get("calibration_version"),
            "confidence": confidence_meta.get("versions", {}).get("confidence"),
            "decision": decision_meta.get("versions", {}).get("decision"),
        },
    }


def main() -> int:
    print(json.dumps(run_fixture_smoke(), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
