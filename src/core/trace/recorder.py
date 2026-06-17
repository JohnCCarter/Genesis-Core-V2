"""External run-trace recorders (Slice 4a/4b, ADR 0002).

Emit a run-trace from the *returned* result of an existing flow, without touching the pure surfaces
that produced it:

- ``record_candidate_build`` (4a) consumes a returned ``CandidateBuildPacket`` + its input snapshots —
  ``decision/*`` (STRICT) stays unedited. This is the "option A" pattern from
  ``tests/governance/test_trace_integration.py`` lifted into a reusable helper.
- ``record_backtest_run`` (4b) consumes a returned ``BacktestEngine.run()`` dict — it never touches
  ``configs``/``champion_cfg`` (records from the read-only results only).

Both recorders are pure consumers (never mutate their input), fail-open (any trace/disk error is
swallowed so the caller's primary output is never blocked), and deep-redact recorded structures.
Authority separation: recorded ``GateResult``s only *mirror* an outcome; the recorders issue no
promotion authority.
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


def _finite_metric_map(mapping: dict | None) -> dict[str, float]:
    """Coerce a metrics mapping to finite floats, dropping non-numeric/non-finite entries.

    The ``EvidencePacket`` validator rejects non-finite metric values; ``profit_factor`` is ``inf``
    when a backtest has no losing trades, so it must be filtered out rather than recorded raw.
    """

    out: dict[str, float] = {}
    for key, value in (mapping or {}).items():
        if value is None or isinstance(value, bool):
            continue
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(numeric):
            out[str(key)] = numeric
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


def record_backtest_run(
    results: dict,
    *,
    writer: TraceWriter | None = None,
    run_id: str | None = None,
    actor: Actor | None = None,
    intent: str = "backtest",
    symbol: str | None = None,
    timeframe: str | None = None,
    root=None,
) -> str | None:
    """Record one backtest as ``kind="backtest"`` evidence (+ a gate when this call owns the run).

    Pure consumer of the returned ``BacktestEngine.run()`` dict: it reads ``backtest_info``/``metrics``/
    ``error`` and never mutates ``results`` (or the ``configs``/``champion_cfg`` that produced them).

    Ownership follows who creates the writer (same rule as ``record_candidate_build``):
    - ``writer`` provided → caller owns the run lifecycle; this call emits **evidence only** (no gate,
      no close), so it can append to a shared run mid-loop without terminating it.
    - ``writer is None`` → this call owns the run: it emits evidence + a ``backtest`` gate
      (``PASS``/``FAIL`` from ``results["error"]``) and closes the run.

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

        backtest_info = results.get("backtest_info") or {}
        environment_hash = fingerprint_config(backtest_info)
        subject_hash = str(
            backtest_info.get("effective_config_fingerprint") or ""
        ) or fingerprint_config(backtest_info)
        error = results.get("error")
        num_trades = (results.get("metrics") or {}).get("num_trades")

        run_writer.record_evidence(
            subject_hash=subject_hash,
            kind="backtest",
            environment_hash=environment_hash,
            metrics=_finite_metric_map(results.get("metrics")),
            summary=redact_text(
                f"backtest {symbol or backtest_info.get('symbol')} "
                f"{timeframe or backtest_info.get('timeframe')} "
                f"trades={num_trades} error={error}".strip()
            ),
        )

        if own_writer:
            status = "FAIL" if error else "PASS"
            run_writer.record_gate(
                stage="backtest",
                status=status,
                criteria_snapshot=_redact_deep(
                    {
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "num_trades": num_trades,
                        "error": error,
                    }
                ),
                issued_by="backtest-engine",
            )
            run_writer.close(outcome=status)

        return run_writer.run_id
    except Exception:  # fail-open: never block the caller's primary output
        logger.warning(
            "backtest run-trace recording failed; continuing without trace", exc_info=True
        )
        return None


__all__ = [
    "new_run_id",
    "record_backtest_run",
    "record_candidate_build",
    "resolve_actor_from_env",
]
