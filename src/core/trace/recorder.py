"""External decision-trace recorder (Slice 4a, ADR 0002).

Emits a run-trace from the *returned* ``CandidateBuildPacket`` plus its input snapshots, without
touching the pure decision kernel (``decision/*`` stays unedited — STRICT surface). This is the
"option A" pattern from ``tests/governance/test_trace_integration.py`` lifted into a reusable helper:
the recorder is a pure consumer of the packet and never mutates it.

Authority separation: the recorded ``GateResult`` only *mirrors* ``ready_for_promotion``; the recorder
issues no promotion authority. Recording is fail-open — any trace/disk error is swallowed so the
caller's primary output is never blocked.
"""

from __future__ import annotations

import json
import logging
import math
import os
from datetime import UTC, datetime

from core.decision.candidate_builder import CandidateBuildPacket
from core.decision.comparison import PROMOTION_MARGIN_PF
from core.decision.models import MetricSnapshot
from core.decision.validation import DEFAULT_TRADE_THRESHOLD
from core.packets import Actor
from core.trace.writer import TraceWriter
from core.utils.diffing.canonical import fingerprint_config
from core.utils.logging_redaction import SENSITIVE_KEYS, redact_text

logger = logging.getLogger(__name__)

_METRIC_FIELDS = ("profit_factor", "max_drawdown", "trades_per_year", "stability", "winrate")


def _redact_deep(value):
    """Recursively mask secrets in a recorded structure.

    Decision results echo input ``to_dict()``s, which can carry free-text ``metadata`` — so the
    recorder scrubs it before persisting (``DecisionPacket``/``GateResult`` bodies are not redacted
    by the packet layer). String leaves run through ``redact_text``; values under known-sensitive
    keys are masked outright. Governance-relevant numeric fields pass through unchanged.
    """

    if isinstance(value, dict):
        return {
            key: ("***" if key in SENSITIVE_KEYS else _redact_deep(item))
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact_deep(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


def resolve_actor_from_env() -> Actor:
    """Resolve the recording actor from the environment (read-only; never writes ``os.environ``)."""

    actor_type = os.environ.get("GENESIS_ACTOR_TYPE", "agent")
    actor_id = os.environ.get("GENESIS_ACTOR_ID", "unknown-agent")
    return Actor(type=actor_type, id=actor_id)


def new_run_id() -> str:
    """Mint a locator run_id, mirroring ``optimizer/runner.py::_create_run_id``."""

    return datetime.now(UTC).strftime("run_%Y%m%d_%H%M%S")


def _finite_metrics(snapshot: MetricSnapshot) -> dict[str, float]:
    out: dict[str, float] = {}
    for field_name in _METRIC_FIELDS:
        value = getattr(snapshot, field_name)
        if value is None:
            continue
        numeric = float(value)
        if math.isfinite(numeric):
            out[field_name] = numeric
    return out


def _summary(role: str, snapshot: MetricSnapshot) -> str:
    meta = json.dumps(snapshot.metadata, sort_keys=True) if snapshot.metadata else ""
    return redact_text(f"{role} family={snapshot.strategy_family} meta={meta}".strip())


def _triggered_codes(report) -> tuple[str, ...]:
    return tuple(risk.code for risk in report.risks if risk.triggered)


def record_candidate_build(
    packet: CandidateBuildPacket,
    *,
    incumbent: MetricSnapshot,
    candidate: MetricSnapshot,
    writer: TraceWriter | None = None,
    run_id: str | None = None,
    actor: Actor | None = None,
    intent: str = "promotion_compare",
    symbol: str | None = None,
    timeframe: str | None = None,
    root=None,
    promotion_margin: float = PROMOTION_MARGIN_PF,
    minimum_trade_threshold: float = DEFAULT_TRADE_THRESHOLD,
) -> str | None:
    """Record one candidate-build decision flow as a run-trace.

    Ownership follows who creates the writer:
    - ``writer is None`` → this call owns the run: it emits the readiness gate and closes the run.
    - ``writer`` provided → the caller owns the run lifecycle (gate + close); this call only emits the
      two evidence packets and the four decision packets, so multiple builds can share one run.

    Returns the run_id, or ``None`` if recording failed (fail-open).
    """

    try:
        own_writer = writer is None
        run_writer = writer or TraceWriter(
            run_id=run_id or new_run_id(),
            actor=actor or resolve_actor_from_env(),
            intent=intent,
            symbol=symbol,
            timeframe=timeframe,
            root=root,
        )

        environment_hash = fingerprint_config(
            {
                "promotion_margin": promotion_margin,
                "minimum_trade_threshold": minimum_trade_threshold,
            }
        )

        incumbent_ref = run_writer.record_evidence(
            subject_hash=fingerprint_config(incumbent.to_dict()),
            kind="metrics",
            environment_hash=environment_hash,
            metrics=_finite_metrics(incumbent),
            summary=_summary("incumbent", incumbent),
        )
        candidate_ref = run_writer.record_evidence(
            subject_hash=fingerprint_config(candidate.to_dict()),
            kind="metrics",
            environment_hash=environment_hash,
            metrics=_finite_metrics(candidate),
            summary=_summary("candidate", candidate),
        )
        evidence_refs = (incumbent_ref, candidate_ref)

        run_writer.record_decision(
            decision_kind="comparison",
            result=_redact_deep(packet.comparison.to_dict()),
            input_evidence_refs=evidence_refs,
            reasons=tuple(str(reason) for reason in packet.comparison.reasons),
        )
        run_writer.record_decision(
            decision_kind="premortem",
            result=_redact_deep(packet.premortem_validate.to_dict()),
            input_evidence_refs=evidence_refs,
            reasons=_triggered_codes(packet.premortem_validate),
        )
        run_writer.record_decision(
            decision_kind="premortem",
            result=_redact_deep(packet.premortem_promote.to_dict()),
            input_evidence_refs=evidence_refs,
            reasons=_triggered_codes(packet.premortem_promote),
        )
        run_writer.record_decision(
            decision_kind="promotion",
            result=_redact_deep(packet.promotion.to_dict()),
            input_evidence_refs=evidence_refs,
            reasons=tuple(str(reason) for reason in packet.promotion.reasons),
        )

        if own_writer:
            status = "PASS" if packet.ready_for_promotion else "WAIT"
            run_writer.record_gate(
                stage="promotion_readiness",
                status=status,
                criteria_snapshot=_redact_deep(
                    {
                        "promotion_margin": promotion_margin,
                        "minimum_trade_threshold": minimum_trade_threshold,
                        "ready_for_promotion": packet.ready_for_promotion,
                    }
                ),
                issued_by="governance-kernel",
            )
            run_writer.close(outcome=status)

        return run_writer.run_id
    except Exception:  # fail-open: never block the caller's primary output
        logger.warning("run-trace recording failed; continuing without trace", exc_info=True)
        return None


__all__ = ["new_run_id", "record_candidate_build", "resolve_actor_from_env"]
