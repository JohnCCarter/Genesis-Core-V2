"""Deterministic premortem reflection for Validate -> Promote flows.

This module is a structured, fail-closed reflection layer. It does not create evidence,
replace validation, or authorize promotion by itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from core.decision.comparison import PROMOTION_MARGIN_PF
from core.decision.models import MetricSnapshot
from core.decision.validation import DEFAULT_TRADE_THRESHOLD
from core.strategy.run_intent import (
    RUN_INTENT_CHAMPION_FREEZE,
    RUN_INTENT_PROMOTION_COMPARE,
    RunIntent,
    RunIntentValidationError,
    validate_run_intent_name,
)


class PremortemSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PremortemDecision(StrEnum):
    PROCEED = "proceed"
    MITIGATE = "mitigate"
    BLOCK = "block"


_SEVERITY_WEIGHT: dict[PremortemSeverity, int] = {
    PremortemSeverity.LOW: 5,
    PremortemSeverity.MEDIUM: 10,
    PremortemSeverity.HIGH: 20,
    PremortemSeverity.CRITICAL: 30,
}


@dataclass(frozen=True, slots=True)
class PremortemRisk:
    code: str
    title: str
    severity: PremortemSeverity
    triggered: bool
    evidence: str
    mitigation: str

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "title": self.title,
            "severity": str(self.severity),
            "triggered": self.triggered,
            "evidence": self.evidence,
            "mitigation": self.mitigation,
        }


@dataclass(frozen=True, slots=True)
class PremortemReport:
    decision: PremortemDecision
    risk_score: int
    risks: tuple[PremortemRisk, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "decision": str(self.decision),
            "risk_score": self.risk_score,
            "risks": [risk.to_dict() for risk in self.risks],
            "triggered_codes": [risk.code for risk in self.risks if risk.triggered],
        }


def _missing_metrics(snapshot: MetricSnapshot, *, scope: str) -> list[str]:
    missing: list[str] = []
    if snapshot.profit_factor is None:
        missing.append(f"{scope}.profit_factor")
    if snapshot.max_drawdown is None:
        missing.append(f"{scope}.max_drawdown")
    if snapshot.trades_per_year is None:
        missing.append(f"{scope}.trades_per_year")
    if snapshot.stability is None:
        missing.append(f"{scope}.stability")
    return missing


def _resolve_run_intent(value: str | RunIntent | None) -> tuple[RunIntent | None, str | None]:
    try:
        return validate_run_intent_name(value), None
    except RunIntentValidationError as exc:
        return None, str(exc)


def run_premortem(
    incumbent_metrics: MetricSnapshot,
    candidate_metrics: MetricSnapshot,
    *,
    override_flag: bool,
    signoff_flag: bool,
    run_intent: str | RunIntent | None = None,
    phase: Literal["validate", "promote"] = "validate",
    promotion_margin: float = PROMOTION_MARGIN_PF,
    minimum_trade_threshold: float = DEFAULT_TRADE_THRESHOLD,
) -> PremortemReport:
    """Evaluate pre-promotion failure modes before candidate admission.

    This is intentionally deterministic and side-effect free so it can be used in
    CI/governance checks and local review loops without introducing runtime drift.
    """

    missing_incumbent = _missing_metrics(incumbent_metrics, scope="incumbent")
    missing_candidate = _missing_metrics(candidate_metrics, scope="candidate")
    run_intent_resolved, run_intent_error = _resolve_run_intent(run_intent)
    promote_intent_allowed = {
        RUN_INTENT_PROMOTION_COMPARE,
        RUN_INTENT_CHAMPION_FREEZE,
    }
    validate_intent_enforced = run_intent is not None
    run_intent_invalid_for_phase = bool(
        (phase == "promote" and run_intent_error)
        or (phase == "validate" and validate_intent_enforced and run_intent_error)
    )
    run_intent_phase_mismatch = bool(
        phase == "promote" and run_intent_resolved not in promote_intent_allowed
    )

    risks: list[PremortemRisk] = [
        PremortemRisk(
            code="PM-000",
            title="Incumbent metrics are incomplete",
            severity=PremortemSeverity.CRITICAL,
            triggered=bool(missing_incumbent),
            evidence=(
                "missing=" + ",".join(sorted(missing_incumbent))
                if missing_incumbent
                else "all required incumbent metrics present"
            ),
            mitigation="Populate incumbent baseline metrics before any comparative decision.",
        ),
        PremortemRisk(
            code="PM-001",
            title="Candidate metrics are incomplete",
            severity=PremortemSeverity.CRITICAL,
            triggered=bool(missing_candidate),
            evidence=(
                "missing=" + ",".join(sorted(missing_candidate))
                if missing_candidate
                else "all required candidate metrics present"
            ),
            mitigation="Populate required candidate metrics before promotion review.",
        ),
        PremortemRisk(
            code="PM-007",
            title="Run-intent is not compatible with requested phase",
            severity=PremortemSeverity.CRITICAL,
            triggered=run_intent_invalid_for_phase or run_intent_phase_mismatch,
            evidence=(
                f"run_intent_error={run_intent_error}"
                if run_intent_invalid_for_phase
                else (
                    f"phase={phase}, run_intent={run_intent_resolved}, allowed_for_promote={sorted(promote_intent_allowed)}"
                    if run_intent_phase_mismatch
                    else f"phase={phase}, run_intent={run_intent_resolved}"
                )
            ),
            mitigation="Use a valid run-intent and only allow promote-phase for promotion/freeze intents.",
        ),
    ]

    if (
        missing_incumbent
        or missing_candidate
        or run_intent_invalid_for_phase
        or run_intent_phase_mismatch
    ):
        risk_score = min(
            100,
            sum(_SEVERITY_WEIGHT[risk.severity] for risk in risks if risk.triggered),
        )
        return PremortemReport(
            decision=PremortemDecision.BLOCK,
            risk_score=risk_score,
            risks=tuple(risks),
        )

    # Safe local aliases after explicit fail-closed checks above.
    candidate_trades_per_year = float(candidate_metrics.trades_per_year or 0.0)
    candidate_profit_factor = float(candidate_metrics.profit_factor or 0.0)
    candidate_max_drawdown = float(candidate_metrics.max_drawdown or 0.0)
    candidate_stability = float(candidate_metrics.stability or 0.0)
    incumbent_profit_factor = float(incumbent_metrics.profit_factor or 0.0)
    incumbent_max_drawdown = float(incumbent_metrics.max_drawdown or 0.0)
    incumbent_stability = float(incumbent_metrics.stability or 0.0)

    min_safe_trade_density = minimum_trade_threshold * 1.20
    trades_thin = candidate_trades_per_year < min_safe_trade_density

    thin_margin_buffer = max(0.01, promotion_margin * 0.50)
    pf_margin = candidate_profit_factor - incumbent_profit_factor
    pf_margin_thin = pf_margin < (promotion_margin + thin_margin_buffer)

    drawdown_buffer_limit = incumbent_max_drawdown * 0.90
    drawdown_fragile = candidate_max_drawdown >= drawdown_buffer_limit

    min_stability_floor = max(0.75, incumbent_stability)
    stability_fragile = candidate_stability < min_stability_floor

    governance_unready = (not override_flag) or (not signoff_flag)

    risks.extend(
        [
            PremortemRisk(
                code="PM-002",
                title="Trade density may be too thin under stress",
                severity=PremortemSeverity.HIGH,
                triggered=trades_thin,
                evidence=(
                    f"trades_per_year={candidate_trades_per_year:.2f} < "
                    f"safe_floor={min_safe_trade_density:.2f}"
                    if trades_thin
                    else (
                        f"trades_per_year={candidate_trades_per_year:.2f} >= "
                        f"safe_floor={min_safe_trade_density:.2f}"
                    )
                ),
                mitigation="Increase sample size or widen validation horizon before promotion.",
            ),
            PremortemRisk(
                code="PM-003",
                title="Profit-factor margin may be too fragile",
                severity=PremortemSeverity.MEDIUM,
                triggered=pf_margin_thin,
                evidence=(
                    f"pf_margin={pf_margin:.4f} < required_with_buffer={promotion_margin + thin_margin_buffer:.4f}"
                    if pf_margin_thin
                    else (
                        f"pf_margin={pf_margin:.4f} >= required_with_buffer={promotion_margin + thin_margin_buffer:.4f}"
                    )
                ),
                mitigation="Require stronger PF delta or additional out-of-sample confirmation.",
            ),
            PremortemRisk(
                code="PM-004",
                title="Drawdown buffer may be too small",
                severity=PremortemSeverity.HIGH,
                triggered=drawdown_fragile,
                evidence=(
                    f"candidate_dd={candidate_max_drawdown:.4f} >= buffer_limit={drawdown_buffer_limit:.4f}"
                    if drawdown_fragile
                    else (
                        f"candidate_dd={candidate_max_drawdown:.4f} < buffer_limit={drawdown_buffer_limit:.4f}"
                    )
                ),
                mitigation="Reduce drawdown profile or keep incumbent until risk envelope improves.",
            ),
            PremortemRisk(
                code="PM-005",
                title="Stability may regress under regime shifts",
                severity=PremortemSeverity.MEDIUM,
                triggered=stability_fragile,
                evidence=(
                    f"candidate_stability={candidate_stability:.4f} < floor={min_stability_floor:.4f}"
                    if stability_fragile
                    else (
                        f"candidate_stability={candidate_stability:.4f} >= floor={min_stability_floor:.4f}"
                    )
                ),
                mitigation="Run additional regime-segment validation before promotion.",
            ),
            PremortemRisk(
                code="PM-006",
                title="Governance controls not ready",
                severity=PremortemSeverity.CRITICAL,
                triggered=governance_unready,
                evidence=(
                    f"override_flag={override_flag}, signoff_flag={signoff_flag}"
                    if governance_unready
                    else "override and signoff controls present"
                ),
                mitigation="Collect explicit override + signoff before any promotion action.",
            ),
        ]
    )

    triggered = [risk for risk in risks if risk.triggered]
    risk_score = min(100, sum(_SEVERITY_WEIGHT[risk.severity] for risk in triggered))

    if any(risk.severity is PremortemSeverity.CRITICAL for risk in triggered):
        decision = PremortemDecision.BLOCK
    elif risk_score >= 40:
        decision = PremortemDecision.MITIGATE
    else:
        decision = PremortemDecision.PROCEED

    return PremortemReport(
        decision=decision,
        risk_score=risk_score,
        risks=tuple(risks),
    )


__all__ = [
    "PremortemDecision",
    "PremortemReport",
    "PremortemRisk",
    "PremortemSeverity",
    "run_premortem",
]
