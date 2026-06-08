from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from core.decision.comparison import PROMOTION_MARGIN_PF, compare_families
from core.decision.models import (
    ComparisonDecision,
    ComparisonResult,
    MetricSnapshot,
    PromotionResult,
    StrategyFamily,
)
from core.decision.premortem import PremortemDecision, PremortemReport, run_premortem
from core.decision.promotion import apply_promotion
from core.decision.validation import DEFAULT_TRADE_THRESHOLD
from core.strategy.run_intent import (
    RUN_INTENT_CANDIDATE,
    RUN_INTENT_PROMOTION_COMPARE,
    RunIntent,
)


def _coerce_optional_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def metric_snapshot_from_mapping(
    payload: Mapping[str, Any],
    *,
    default_strategy_family: StrategyFamily | None = None,
) -> MetricSnapshot:
    strategy_family_raw = payload.get("strategy_family", default_strategy_family)
    strategy_family: StrategyFamily | None
    if strategy_family_raw in {"ri", "legacy"}:
        strategy_family = strategy_family_raw
    else:
        strategy_family = None

    metadata_raw = payload.get("metadata")
    metadata = (
        {str(k): str(v) for k, v in metadata_raw.items()}
        if isinstance(metadata_raw, Mapping)
        else {}
    )

    return MetricSnapshot(
        strategy_family=strategy_family,
        profit_factor=_coerce_optional_float(payload.get("profit_factor")),
        max_drawdown=_coerce_optional_float(payload.get("max_drawdown")),
        trades_per_year=_coerce_optional_float(payload.get("trades_per_year")),
        stability=_coerce_optional_float(payload.get("stability")),
        winrate=_coerce_optional_float(payload.get("winrate")),
        metadata=metadata,
    )


@dataclass(frozen=True, slots=True)
class CandidateBuildPacket:
    comparison: ComparisonResult
    premortem_validate: PremortemReport
    premortem_promote: PremortemReport
    promotion: PromotionResult
    ready_for_promotion: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "comparison": self.comparison.to_dict(),
            "premortem_validate": self.premortem_validate.to_dict(),
            "premortem_promote": self.premortem_promote.to_dict(),
            "promotion": self.promotion.to_dict(),
            "ready_for_promotion": self.ready_for_promotion,
        }


def build_candidate_packet(
    incumbent_metrics: MetricSnapshot,
    candidate_metrics: MetricSnapshot,
    *,
    validate_run_intent: RunIntent | str = RUN_INTENT_CANDIDATE,
    promotion_run_intent: RunIntent | str = RUN_INTENT_PROMOTION_COMPARE,
    promotion_override_flag: bool = False,
    promotion_signoff_flag: bool = False,
    promotion_margin: float = PROMOTION_MARGIN_PF,
    minimum_trade_threshold: float = DEFAULT_TRADE_THRESHOLD,
) -> CandidateBuildPacket:
    comparison = compare_families(
        incumbent_metrics,
        candidate_metrics,
        promotion_margin=promotion_margin,
        minimum_trade_threshold=minimum_trade_threshold,
    )

    premortem_validate = run_premortem(
        incumbent_metrics,
        candidate_metrics,
        override_flag=True,
        signoff_flag=True,
        run_intent=validate_run_intent,
        phase="validate",
        promotion_margin=promotion_margin,
        minimum_trade_threshold=minimum_trade_threshold,
    )

    premortem_promote = run_premortem(
        incumbent_metrics,
        candidate_metrics,
        override_flag=promotion_override_flag,
        signoff_flag=promotion_signoff_flag,
        run_intent=promotion_run_intent,
        phase="promote",
        promotion_margin=promotion_margin,
        minimum_trade_threshold=minimum_trade_threshold,
    )

    promotion = apply_promotion(
        comparison,
        override_flag=promotion_override_flag,
        signoff_flag=promotion_signoff_flag,
    )

    ready_for_promotion = bool(
        comparison.decision is ComparisonDecision.PROMOTE
        and premortem_promote.decision is PremortemDecision.PROCEED
        and promotion.decision is ComparisonDecision.PROMOTE
    )

    return CandidateBuildPacket(
        comparison=comparison,
        premortem_validate=premortem_validate,
        premortem_promote=premortem_promote,
        promotion=promotion,
        ready_for_promotion=ready_for_promotion,
    )


__all__ = [
    "CandidateBuildPacket",
    "build_candidate_packet",
    "metric_snapshot_from_mapping",
]
