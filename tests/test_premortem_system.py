from __future__ import annotations

from core.decision.models import MetricSnapshot
from core.decision.premortem import PremortemDecision, run_premortem


def _metrics(
    strategy_family: str | None,
    *,
    profit_factor: float | None,
    max_drawdown: float | None,
    trades_per_year: float | None,
    stability: float | None,
    winrate: float = 0.55,
) -> MetricSnapshot:
    return MetricSnapshot(
        strategy_family=strategy_family,
        profit_factor=profit_factor,
        max_drawdown=max_drawdown,
        trades_per_year=trades_per_year,
        stability=stability,
        winrate=winrate,
    )


def test_premortem_blocks_on_missing_candidate_metrics() -> None:
    incumbent = _metrics(
        "ri",
        profit_factor=1.20,
        max_drawdown=0.12,
        trades_per_year=90.0,
        stability=0.84,
    )
    candidate = _metrics(
        "ri",
        profit_factor=None,
        max_drawdown=0.11,
        trades_per_year=85.0,
        stability=None,
    )

    report = run_premortem(
        incumbent,
        candidate,
        override_flag=True,
        signoff_flag=True,
    )
    payload = report.to_dict()

    assert report.decision is PremortemDecision.BLOCK
    assert report.risk_score == 30
    assert payload["decision"] == "block"
    assert set(payload["triggered_codes"]) == {"PM-001"}


def test_premortem_blocks_on_missing_incumbent_metrics_fail_closed() -> None:
    incumbent = _metrics(
        "ri",
        profit_factor=None,
        max_drawdown=0.12,
        trades_per_year=90.0,
        stability=None,
    )
    candidate = _metrics(
        "ri",
        profit_factor=1.32,
        max_drawdown=0.11,
        trades_per_year=95.0,
        stability=0.90,
    )

    report = run_premortem(
        incumbent,
        candidate,
        override_flag=True,
        signoff_flag=True,
    )

    assert report.decision is PremortemDecision.BLOCK
    assert any(risk.code == "PM-000" and risk.triggered for risk in report.risks)


def test_premortem_blocks_when_governance_controls_missing() -> None:
    incumbent = _metrics(
        "ri",
        profit_factor=1.20,
        max_drawdown=0.12,
        trades_per_year=90.0,
        stability=0.84,
    )
    candidate = _metrics(
        "ri",
        profit_factor=1.32,
        max_drawdown=0.10,
        trades_per_year=98.0,
        stability=0.90,
    )

    report = run_premortem(
        incumbent,
        candidate,
        override_flag=False,
        signoff_flag=True,
        run_intent="promotion_compare",
        phase="promote",
    )

    assert report.decision is PremortemDecision.BLOCK
    assert any(risk.code == "PM-006" and risk.triggered for risk in report.risks)


def test_premortem_mitigate_when_risk_stack_is_elevated() -> None:
    incumbent = _metrics(
        "ri",
        profit_factor=1.20,
        max_drawdown=0.12,
        trades_per_year=90.0,
        stability=0.84,
    )
    candidate = _metrics(
        "ri",
        profit_factor=1.255,
        max_drawdown=0.115,
        trades_per_year=55.0,
        stability=0.80,
    )

    report = run_premortem(
        incumbent,
        candidate,
        override_flag=True,
        signoff_flag=True,
        run_intent="promotion_compare",
        phase="validate",
    )

    assert report.decision is PremortemDecision.MITIGATE
    assert report.risk_score >= 40
    assert any(risk.code == "PM-002" and risk.triggered for risk in report.risks)
    assert any(risk.code == "PM-003" and risk.triggered for risk in report.risks)
    assert any(risk.code == "PM-004" and risk.triggered for risk in report.risks)


def test_premortem_proceeds_for_healthy_candidate() -> None:
    incumbent = _metrics(
        "ri",
        profit_factor=1.20,
        max_drawdown=0.12,
        trades_per_year=90.0,
        stability=0.84,
    )
    candidate = _metrics(
        "ri",
        profit_factor=1.30,
        max_drawdown=0.08,
        trades_per_year=110.0,
        stability=0.90,
    )

    report = run_premortem(
        incumbent,
        candidate,
        override_flag=True,
        signoff_flag=True,
        run_intent="promotion_compare",
        phase="validate",
    )

    assert report.decision is PremortemDecision.PROCEED
    assert report.risk_score == 0
    assert all(not risk.triggered for risk in report.risks)


def test_premortem_blocks_promote_phase_for_non_promotion_run_intent() -> None:
    incumbent = _metrics(
        "ri",
        profit_factor=1.20,
        max_drawdown=0.12,
        trades_per_year=90.0,
        stability=0.84,
    )
    candidate = _metrics(
        "ri",
        profit_factor=1.30,
        max_drawdown=0.08,
        trades_per_year=110.0,
        stability=0.90,
    )

    report = run_premortem(
        incumbent,
        candidate,
        override_flag=True,
        signoff_flag=True,
        run_intent="research_slice",
        phase="promote",
    )

    assert report.decision is PremortemDecision.BLOCK
    assert any(risk.code == "PM-007" and risk.triggered for risk in report.risks)
