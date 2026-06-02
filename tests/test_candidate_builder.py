from __future__ import annotations

from core.decision.candidate_builder import (
    build_candidate_packet,
    metric_snapshot_from_mapping,
)
from core.decision.models import ComparisonDecision
from core.decision.premortem import PremortemDecision


def _snapshot(
    *,
    pf: float,
    dd: float,
    tpy: float,
    stability: float,
) -> dict[str, object]:
    return {
        "strategy_family": "ri",
        "profit_factor": pf,
        "max_drawdown": dd,
        "trades_per_year": tpy,
        "stability": stability,
        "winrate": 0.55,
        "metadata": {"source": "test"},
    }


def test_build_candidate_packet_marks_ready_when_all_gates_pass() -> None:
    incumbent = metric_snapshot_from_mapping(_snapshot(pf=1.20, dd=0.12, tpy=85.0, stability=0.80))
    candidate = metric_snapshot_from_mapping(_snapshot(pf=1.31, dd=0.10, tpy=90.0, stability=0.90))

    packet = build_candidate_packet(
        incumbent,
        candidate,
        promotion_override_flag=True,
        promotion_signoff_flag=True,
    )

    assert packet.comparison.decision is ComparisonDecision.PROMOTE
    assert packet.premortem_validate.decision in {
        PremortemDecision.PROCEED,
        PremortemDecision.MITIGATE,
    }
    assert packet.premortem_promote.decision is PremortemDecision.PROCEED
    assert packet.promotion.decision is ComparisonDecision.PROMOTE
    assert packet.ready_for_promotion is True


def test_build_candidate_packet_not_ready_without_signoff_controls() -> None:
    incumbent = metric_snapshot_from_mapping(_snapshot(pf=1.20, dd=0.12, tpy=85.0, stability=0.80))
    candidate = metric_snapshot_from_mapping(_snapshot(pf=1.31, dd=0.10, tpy=90.0, stability=0.90))

    packet = build_candidate_packet(
        incumbent,
        candidate,
        promotion_override_flag=False,
        promotion_signoff_flag=False,
    )

    assert packet.comparison.decision is ComparisonDecision.PROMOTE
    assert packet.premortem_promote.decision is PremortemDecision.BLOCK
    assert packet.promotion.decision is ComparisonDecision.NO_PROMOTION
    assert packet.ready_for_promotion is False


def test_metric_snapshot_from_mapping_coerces_string_numbers() -> None:
    snapshot = metric_snapshot_from_mapping(
        {
            "strategy_family": "ri",
            "profit_factor": "1.25",
            "max_drawdown": "0.11",
            "trades_per_year": "72",
            "stability": "0.84",
            "winrate": "0.58",
            "metadata": {"tag": "coerce"},
        }
    )

    assert snapshot.profit_factor == 1.25
    assert snapshot.max_drawdown == 0.11
    assert snapshot.trades_per_year == 72.0
    assert snapshot.stability == 0.84
    assert snapshot.winrate == 0.58
    assert snapshot.strategy_family == "ri"
    assert snapshot.metadata == {"tag": "coerce"}
