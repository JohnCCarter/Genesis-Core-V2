from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.strategy.model_registry import ModelRegistry
from core.strategy.prob_model import predict_proba_for

REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_MODEL_ROOT = REPO_ROOT / "registry" / "fixtures" / "model_registry"
DEFAULT_MODEL_REGISTRY_PATH = FIXTURE_MODEL_ROOT / "config" / "models" / "registry.json"
DEFAULT_MODEL_FIXTURE_PATH = FIXTURE_MODEL_ROOT / "config" / "models" / "tBTCUSD_1h.json"


def run_model_smoke() -> dict[str, Any]:
    registry = ModelRegistry(root=FIXTURE_MODEL_ROOT)
    model_meta = registry.get_meta("tBTCUSD", "1h") or {}
    schema = list(model_meta.get("schema") or [])
    if not schema:
        raise AssertionError("Expected local V2 model fixture to expose a non-empty schema")

    features = {schema[0]: 1.0}
    previous_registry = getattr(predict_proba_for, "_registry", None)
    predict_proba_for._registry = registry
    try:
        probas, meta = predict_proba_for("tBTCUSD", "1h", features, regime="balanced")
    finally:
        if previous_registry is None:
            delattr(predict_proba_for, "_registry")
        else:
            predict_proba_for._registry = previous_registry

    return {
        "registry_path": str(DEFAULT_MODEL_REGISTRY_PATH.resolve()),
        "model_path": str(DEFAULT_MODEL_FIXTURE_PATH.resolve()),
        "schema": schema,
        "probas": probas,
        "versions": dict(meta.get("versions") or {}),
        "calibration_used": dict(meta.get("calibration_used") or {}),
    }


def main() -> int:
    print(json.dumps(run_model_smoke(), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
