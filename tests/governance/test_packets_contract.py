from __future__ import annotations

import json

import pytest

from core.packets import (
    Actor,
    DecisionPacket,
    EvidencePacket,
    GateResult,
    PacketEnvelope,
    PacketValidationError,
    RunRecord,
    validate_decision_packet,
    validate_evidence_packet,
    validate_gate_result,
    validate_run_record,
)

_TS = "2026-06-17T12:00:00+00:00"


def _envelope(**overrides) -> PacketEnvelope:
    base = {
        "run_id": "run_20260617_120000",
        "trace_id": "trace-abc",
        "actor": Actor(type="agent", id="claude"),
        "created_at": _TS,
        "sequence_number": 0,
        "parent_run_id": None,
    }
    base.update(overrides)
    return PacketEnvelope(**base)


def _evidence(envelope: PacketEnvelope | None = None, **overrides) -> EvidencePacket:
    base = {
        "envelope": envelope or _envelope(),
        "subject_hash": "subj-1",
        "kind": "backtest",
        "environment_hash": "env-1",
        "inputs": {"symbol": "tBTCUSD"},
        "metrics": {"profit_factor": 1.25},
        "dataset_refs": ("dataset://a",),
        "artifact_refs": ("artifact://b",),
        "summary": "clean run",
    }
    base.update(overrides)
    return EvidencePacket(**base)


# --- round-trip -------------------------------------------------------------------


def test_evidence_packet_round_trip() -> None:
    packet = _evidence()
    assert EvidencePacket.from_payload(packet.to_payload()) == packet
    assert packet.content_hash() == EvidencePacket.from_payload(packet.to_payload()).content_hash()


def test_decision_packet_round_trip() -> None:
    packet = DecisionPacket(
        envelope=_envelope(),
        decision_kind="comparison",
        result={"decision": "promote", "reasons": ["promotion_approved"]},
        input_evidence_refs=("hash-1",),
        reasons=("promotion_approved",),
    )
    assert DecisionPacket.from_payload(packet.to_payload()) == packet


def test_gate_result_round_trip() -> None:
    packet = GateResult(
        envelope=_envelope(),
        stage="validate",
        status="PASS",
        criteria_snapshot={"pf_margin": 0.05},
        blocking_evidence_refs=(),
        signoff_ref=None,
        issued_by="governance-kernel",
    )
    assert GateResult.from_payload(packet.to_payload()) == packet


def test_run_record_round_trip() -> None:
    record = RunRecord(
        run_id="run_20260617_120000",
        trace_id="trace-abc",
        actor=Actor(type="agent", id="claude"),
        intent="backtest",
        started_at=_TS,
        symbol="tBTCUSD",
        timeframe="1h",
        event_count=3,
        dir="results/trace/run_20260617_120000",
    )
    assert RunRecord.from_payload(record.to_payload()) == record


# --- content-hash determinism ----------------------------------------------------


def test_content_hash_excludes_volatile_envelope() -> None:
    a = _evidence(_envelope(run_id="run_A", created_at=_TS, sequence_number=0))
    b = _evidence(
        _envelope(
            run_id="run_B",
            created_at="2027-01-01T00:00:00+00:00",
            sequence_number=99,
            actor=Actor(type="human", id="kingpin"),
            parent_run_id="run_A",
        )
    )
    # Same body, different envelope -> identical identity.
    assert a.content_hash() == b.content_hash()


def test_content_hash_changes_with_body() -> None:
    a = _evidence()
    b = _evidence(metrics={"profit_factor": 1.26})
    assert a.content_hash() != b.content_hash()


# --- fail-closed validation ------------------------------------------------------


def test_validate_evidence_happy_path_returns_packet() -> None:
    packet = _evidence()
    assert validate_evidence_packet(packet) is packet


@pytest.mark.parametrize(
    "overrides",
    [
        {"subject_hash": ""},
        {"kind": ""},
        {"environment_hash": ""},
        {"metrics": {"x": float("inf")}},
    ],
)
def test_validate_evidence_rejects_bad_fields(overrides) -> None:
    with pytest.raises(PacketValidationError):
        validate_evidence_packet(_evidence(**overrides))


@pytest.mark.parametrize(
    "envelope_overrides",
    [
        {"run_id": ""},
        {"trace_id": ""},
        {"actor": Actor(type="robot", id="x")},
        {"actor": Actor(type="agent", id="")},
        {"created_at": "not-a-timestamp"},
        {"created_at": "2026-06-17T12:00:00"},  # no timezone
        {"sequence_number": -1},
    ],
)
def test_validate_envelope_rejects_bad_fields(envelope_overrides) -> None:
    with pytest.raises(PacketValidationError):
        validate_evidence_packet(_evidence(_envelope(**envelope_overrides)))


def test_validate_gate_rejects_unknown_status() -> None:
    packet = GateResult(envelope=_envelope(), stage="validate", status="MAYBE")
    with pytest.raises(PacketValidationError):
        validate_gate_result(packet)


def test_validate_decision_rejects_empty_kind() -> None:
    packet = DecisionPacket(envelope=_envelope(), decision_kind="")
    with pytest.raises(PacketValidationError):
        validate_decision_packet(packet)


def test_validate_run_record_rejects_empty_intent() -> None:
    record = RunRecord(
        run_id="r",
        trace_id="t",
        actor=Actor(type="agent", id="claude"),
        intent="",
        started_at=_TS,
    )
    with pytest.raises(PacketValidationError):
        validate_run_record(record)


# --- redaction -------------------------------------------------------------------


def test_secrets_are_redacted_before_serialization_and_hash() -> None:
    secret = "SUPERSECRETVALUE"
    packet = _evidence(
        summary=f"call used apiKey={secret} once",
        inputs={"apiKey": secret, "note": "ok"},
    )
    payload = packet.to_payload()
    serialized = json.dumps(payload, sort_keys=True)

    assert secret not in serialized
    assert payload["summary"] == "call used apiKey=*** once"
    assert payload["inputs"]["apiKey"] != secret
    # The content hash is computed over the redacted body, so the secret never enters it.
    assert secret not in packet.content_hash()
