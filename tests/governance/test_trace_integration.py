"""End-to-end proof of the run-trace foundation (ADR 0002), additive (Slice 4, option A).

Demonstrates the inter-agent loop with the *real* decision kernel, without editing any
decision/* or pipeline.py surface: one writer ("agent A") records a comparison flow; a separate
reader ("agent B") reconstructs exactly what A did and fetches the referenced evidence.
"""

from __future__ import annotations

from pathlib import Path

from core.decision.comparison import compare_families
from core.decision.models import MetricSnapshot
from core.decision.premortem import run_premortem
from core.packets import Actor
from core.trace import TraceWriter, read_events, read_evidence, read_run

_TS = "2026-06-17T12:00:00+00:00"


def _snapshot(pf: float, dd: float, tpy: float, stab: float) -> MetricSnapshot:
    return MetricSnapshot(
        strategy_family="ri",
        profit_factor=pf,
        max_drawdown=dd,
        trades_per_year=tpy,
        stability=stab,
    )


def test_agent_a_writes_real_decision_agent_b_reads(tmp_path: Path) -> None:
    incumbent = _snapshot(1.2, 0.20, 120, 0.80)
    candidate = _snapshot(1.4, 0.15, 130, 0.85)
    comparison = compare_families(incumbent, candidate)
    assert comparison.decision.value == "promote"  # sanity: real kernel said promote

    # --- agent A records the flow (no decision/* or pipeline.py edits) ---
    writer = TraceWriter(
        run_id="run_validate_1",
        actor=Actor(type="agent", id="agent-A"),
        intent="validate",
        symbol="tBTCUSD",
        timeframe="1h",
        root=tmp_path,
        clock=lambda: _TS,
    )
    evidence_hash = writer.record_evidence(
        subject_hash="candidate-1",
        kind="comparison",
        environment_hash="env-1",
        metrics={"candidate_pf": 1.4, "incumbent_pf": 1.2},
    )
    writer.record_decision(
        decision_kind="comparison",
        result=comparison.to_dict(),
        input_evidence_refs=(evidence_hash,),
        reasons=tuple(str(reason) for reason in comparison.reasons),
    )
    writer.record_gate(
        stage="validate",
        status="PASS",
        criteria_snapshot={"promotion_margin_pf": 0.05},
        issued_by="governance-kernel",
    )
    writer.close(outcome="PASS")

    # --- agent B reads it back ---
    record = read_run("run_validate_1", root=tmp_path)
    assert record.actor.id == "agent-A"
    assert record.outcome == "PASS"

    events = read_events("run_validate_1", root=tmp_path)
    assert [type(event).__name__ for event in events] == [
        "EvidencePacket",
        "DecisionPacket",
        "GateResult",
    ]

    decision_packet = events[1]
    assert decision_packet.result["decision"] == "promote"
    assert decision_packet.input_evidence_refs == (evidence_hash,)

    # B can fetch, content-addressed, exactly the evidence A's decision referenced.
    evidence = read_evidence(evidence_hash, root=tmp_path)
    assert evidence is not None
    assert evidence.kind == "comparison"


def test_premortem_block_is_recorded_and_readable(tmp_path: Path) -> None:
    incumbent = _snapshot(1.2, 0.20, 120, 0.80)
    candidate = _snapshot(1.4, 0.15, 130, 0.85)
    report = run_premortem(incumbent, candidate, override_flag=False, signoff_flag=False)
    # Governance controls absent -> the real premortem blocks.
    assert report.decision.value == "block"

    writer = TraceWriter(
        run_id="run_premortem_1",
        actor=Actor(type="agent", id="agent-A"),
        intent="validate",
        root=tmp_path,
        clock=lambda: _TS,
    )
    writer.record_decision(decision_kind="premortem", result=report.to_dict())
    writer.record_gate(stage="validate", status="HALT", issued_by="governance-kernel")
    writer.close(outcome="HALT")

    events = read_events("run_premortem_1", root=tmp_path)
    assert events[0].result["decision"] == "block"
    assert read_run("run_premortem_1", root=tmp_path).outcome == "HALT"


def test_same_decision_inputs_yield_same_evidence_identity(tmp_path: Path) -> None:
    first = TraceWriter(
        run_id="r1",
        actor=Actor(type="agent", id="A"),
        intent="validate",
        root=tmp_path,
        clock=lambda: _TS,
    )
    second = TraceWriter(
        run_id="r2",
        actor=Actor(type="human", id="kingpin"),
        intent="validate",
        root=tmp_path,
        clock=lambda: "2027-01-01T00:00:00+00:00",
    )
    hash_a = first.record_evidence(
        subject_hash="s", kind="comparison", environment_hash="e", metrics={"pf": 1.4}
    )
    hash_b = second.record_evidence(
        subject_hash="s", kind="comparison", environment_hash="e", metrics={"pf": 1.4}
    )
    assert hash_a == hash_b  # identity independent of run/actor/clock
