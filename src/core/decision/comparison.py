from __future__ import annotations

from core.decision.models import (
    ComparisonDecision,
    ComparisonResult,
    DecisionReason,
    MetricSnapshot,
)
from core.decision.validation import (
    DEFAULT_TRADE_THRESHOLD,
    enforce_trade_threshold,
    validate_metrics,
)

PROMOTION_MARGIN_PF = 0.05


def compare_families(
    incumbent_metrics: MetricSnapshot,
    candidate_metrics: MetricSnapshot,
    *,
    promotion_margin: float = PROMOTION_MARGIN_PF,
    minimum_trade_threshold: float = DEFAULT_TRADE_THRESHOLD,
) -> ComparisonResult:
    reasons = list(validate_metrics(incumbent_metrics, expected_family="ri"))
    reasons.extend(validate_metrics(candidate_metrics, expected_family="ri"))

    if reasons:
        return ComparisonResult(
            decision=ComparisonDecision.INVALID,
            reasons=tuple(dict.fromkeys(reasons)),
            incumbent_metrics=incumbent_metrics,
            candidate_metrics=candidate_metrics,
        )

    trade_reasons = list(
        enforce_trade_threshold(candidate_metrics, threshold=minimum_trade_threshold)
    )
    if trade_reasons:
        return ComparisonResult(
            decision=ComparisonDecision.INVALID,
            reasons=tuple(dict.fromkeys(trade_reasons)),
            incumbent_metrics=incumbent_metrics,
            candidate_metrics=candidate_metrics,
        )

    assert incumbent_metrics.profit_factor is not None
    assert candidate_metrics.profit_factor is not None
    assert incumbent_metrics.max_drawdown is not None
    assert candidate_metrics.max_drawdown is not None
    assert incumbent_metrics.stability is not None
    assert candidate_metrics.stability is not None

    comparison_reasons: list[DecisionReason] = []
    if candidate_metrics.profit_factor < incumbent_metrics.profit_factor + promotion_margin:
        comparison_reasons.append(DecisionReason.PROFIT_FACTOR_MARGIN_NOT_MET)
    if candidate_metrics.max_drawdown > incumbent_metrics.max_drawdown:
        comparison_reasons.append(DecisionReason.DRAWDOWN_WORSE_THAN_INCUMBENT)
    if candidate_metrics.stability < incumbent_metrics.stability:
        comparison_reasons.append(DecisionReason.STABILITY_BELOW_INCUMBENT)

    if comparison_reasons:
        comparison_reasons.append(DecisionReason.INCUMBENT_RETAINED)
        return ComparisonResult(
            decision=ComparisonDecision.KEEP_INCUMBENT,
            reasons=tuple(dict.fromkeys(comparison_reasons)),
            incumbent_metrics=incumbent_metrics,
            candidate_metrics=candidate_metrics,
        )

    return ComparisonResult(
        decision=ComparisonDecision.PROMOTE,
        reasons=(DecisionReason.PROMOTION_APPROVED,),
        incumbent_metrics=incumbent_metrics,
        candidate_metrics=candidate_metrics,
    )
