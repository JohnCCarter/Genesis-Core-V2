"""Slice 4a: the external decision-trace recorder (no decision/* edits, fail-open, side-effect-free).

Proves the recorder turns a returned ``CandidateBuildPacket`` + its inputs into a readable trace
without mutating the packet, with deterministic content identity, redacted free text, and a gate that
only mirrors readiness.
"""

from __future__ import annotations

from pathlib import Path

from core.decision.candidate_builder import build_candidate_packet
from core.decision.models import MetricSnapshot
from core.packets import Actor, DecisionPacket, EvidencePacket, GateResult
from core.trace import (
    TraceWriter,
    read_events,
    read_run,
    record_candidate_build,
    resolve_actor_from_env,
)

_ACTOR = Actor(type="agent", id="agent-A")


def _snapshot(pf: float, dd: float, tpy: float, stab: float, **meta: str) -> MetricSnapshot:
    return MetricSnapshot(
        strategy_family="ri",
        profit_factor=pf,
        max_drawdown=dd,
        trades_per_year=tpy,
        stability=stab,
        metadata=dict(meta),
    )


def _promote_ready_inputs() -> tuple[MetricSnapshot, MetricSnapshot]:
    incumbent = _snapshot(1.2, 0.20, 120, 0.80)
    candidate = _snapshot(1.4, 0.15, 130, 0.85)
    return incumbent, candidate


def _build(incumbent: MetricSnapshot, candidate: MetricSnapshot):
    return build_candidate_packet(
        incumbent,
        candidate,
        promotion_override_flag=True,
        promotion_signoff_flag=True,
    )


def test_records_evidence_decisions_and_gate_in_order(tmp_path: Path) -> None:
    incumbent, candidate = _promote_ready_inputs()
    packet = _build(incumbent, candidate)
    assert packet.ready_for_promotion is True  # sanity: real kernel is promote-ready

    run_id = record_candidate_build(
        packet,
        incumbent=incumbent,
        candidate=candidate,
        run_id="run_rec_1",
        actor=_ACTOR,
        root=tmp_path,
    )
    assert run_id == "run_rec_1"

    events = read_events("run_rec_1", root=tmp_path)
    assert [type(e).__name__ for e in events] == [
        "EvidencePacket",
        "EvidencePacket",
        "DecisionPacket",
        "DecisionPacket",
        "DecisionPacket",
        "DecisionPacket",
        "GateResult",
    ]

    decisions = [e for e in events if isinstance(e, DecisionPacket)]
    assert [d.decision_kind for d in decisions] == [
        "comparison",
        "premortem",
        "premortem",
        "promotion",
    ]
    assert decisions[0].result["decision"] == "promote"

    # Decisions are causally linked to exactly the two evidence packets the recorder emitted.
    evidence = [e for e in events if isinstance(e, EvidencePacket)]
    evidence_hashes = tuple(e.content_hash() for e in evidence)
    for decision in decisions:
        assert decision.input_evidence_refs == evidence_hashes

    gate = events[-1]
    assert isinstance(gate, GateResult)
    assert gate.stage == "promotion_readiness"
    assert gate.status == "PASS"
    assert gate.criteria_snapshot["ready_for_promotion"] is True
    assert read_run("run_rec_1", root=tmp_path).outcome == "PASS"


def test_premortem_phases_both_recorded(tmp_path: Path) -> None:
    # The two premortem phases (validate, promote) both surface as decisions.
    incumbent, candidate = _promote_ready_inputs()
    packet = _build(incumbent, candidate)
    record_candidate_build(
        packet, incumbent=incumbent, candidate=candidate, run_id="run_pm", root=tmp_path
    )
    kinds = [
        e.decision_kind
        for e in read_events("run_pm", root=tmp_path)
        if isinstance(e, DecisionPacket)
    ]
    assert kinds.count("premortem") == 2


def test_content_hash_is_deterministic_across_runs(tmp_path: Path) -> None:
    incumbent, candidate = _promote_ready_inputs()
    packet = _build(incumbent, candidate)

    record_candidate_build(
        packet,
        incumbent=incumbent,
        candidate=candidate,
        run_id="run_a",
        actor=Actor(type="agent", id="A"),
        root=tmp_path / "a",
    )
    record_candidate_build(
        packet,
        incumbent=incumbent,
        candidate=candidate,
        run_id="run_b",
        actor=Actor(type="human", id="kingpin"),
        root=tmp_path / "b",
    )

    hashes_a = [e.content_hash() for e in read_events("run_a", root=tmp_path / "a")]
    hashes_b = [e.content_hash() for e in read_events("run_b", root=tmp_path / "b")]
    assert hashes_a == hashes_b  # identity independent of run_id/actor/clock


def test_recorder_does_not_mutate_packet_parity(tmp_path: Path) -> None:
    incumbent, candidate = _promote_ready_inputs()
    packet = _build(incumbent, candidate)
    before = packet.to_dict()

    record_candidate_build(
        packet, incumbent=incumbent, candidate=candidate, run_id="run_parity", root=tmp_path
    )

    assert packet.to_dict() == before  # recorder is a pure consumer
    # A fresh build from the same inputs is byte-identical (decision kernel unaffected).
    assert _build(incumbent, candidate).to_dict() == before


def test_recording_is_fail_open_on_writer_error(tmp_path: Path) -> None:
    incumbent, candidate = _promote_ready_inputs()
    packet = _build(incumbent, candidate)

    class _ExplodingWriter:
        run_id = "boom"

        def record_evidence(self, **_kwargs):
            raise RuntimeError("disk is on fire")

    # Must swallow the error and return None rather than propagate.
    result = record_candidate_build(
        packet,
        incumbent=incumbent,
        candidate=candidate,
        writer=_ExplodingWriter(),
    )
    assert result is None


def test_secret_in_metadata_is_redacted_on_disk(tmp_path: Path) -> None:
    # A planted secret flows into both the evidence summary AND the decision result (which echoes
    # candidate_metrics.metadata). The recorder must mask it everywhere it lands on disk.
    incumbent = _snapshot(1.2, 0.20, 120, 0.80)
    candidate = _snapshot(1.4, 0.15, 130, 0.85, note="apiKey=SUPERSECRET")
    packet = _build(incumbent, candidate)

    record_candidate_build(
        packet, incumbent=incumbent, candidate=candidate, run_id="run_secret", root=tmp_path
    )

    raw = (tmp_path / "run_secret" / "events.jsonl").read_text(encoding="utf-8")
    assert "SUPERSECRET" not in raw  # nowhere on disk, including the decision result
    assert "apiKey=***" in raw  # and the mask is present where the secret was

    events = read_events("run_secret", root=tmp_path)
    evidence_summaries = " ".join(e.summary for e in events if isinstance(e, EvidencePacket))
    assert "SUPERSECRET" not in evidence_summaries
    comparison = next(
        e for e in events if isinstance(e, DecisionPacket) and e.decision_kind == "comparison"
    )
    assert comparison.result["candidate_metrics"]["metadata"]["note"] == "apiKey=***"


def test_shared_writer_defers_gate_and_close_to_caller(tmp_path: Path) -> None:
    # When the caller owns the writer, the recorder emits only evidence + decisions.
    incumbent, candidate = _promote_ready_inputs()
    packet = _build(incumbent, candidate)
    writer = TraceWriter(
        run_id="run_shared",
        actor=_ACTOR,
        intent="candidate_search",
        root=tmp_path,
        clock=lambda: "2026-06-17T12:00:00+00:00",
    )

    record_candidate_build(packet, incumbent=incumbent, candidate=candidate, writer=writer)

    events = read_events("run_shared", root=tmp_path)
    assert [type(e).__name__ for e in events] == [
        "EvidencePacket",
        "EvidencePacket",
        "DecisionPacket",
        "DecisionPacket",
        "DecisionPacket",
        "DecisionPacket",
    ]
    assert read_run("run_shared", root=tmp_path).outcome is None  # caller has not closed yet

    writer.record_gate(stage="promotion_readiness", status="PASS", issued_by="governance-kernel")
    writer.close(outcome="PASS")
    assert read_run("run_shared", root=tmp_path).outcome == "PASS"


def test_resolve_actor_from_env_defaults_and_override(monkeypatch) -> None:
    monkeypatch.delenv("GENESIS_ACTOR_ID", raising=False)
    monkeypatch.delenv("GENESIS_ACTOR_TYPE", raising=False)
    default = resolve_actor_from_env()
    assert default.type == "agent"
    assert default.id == "unknown-agent"

    monkeypatch.setenv("GENESIS_ACTOR_ID", "claude-opus")
    monkeypatch.setenv("GENESIS_ACTOR_TYPE", "human")
    overridden = resolve_actor_from_env()
    assert overridden.type == "human"
    assert overridden.id == "claude-opus"
