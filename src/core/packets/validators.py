"""Fail-closed validation for the minimal packet contract (ADR 0002).

Every validator raises ``PacketValidationError`` on the first violation and returns the validated
packet otherwise. Validation never silently permits a malformed record.
"""

from __future__ import annotations

import math
from datetime import datetime

from core.packets.models import (
    DecisionPacket,
    EvidencePacket,
    GateResult,
    PacketEnvelope,
    RunRecord,
)

ALLOWED_ACTOR_TYPES = frozenset({"human", "agent"})
ALLOWED_GATE_STATUS = frozenset({"PASS", "FAIL", "WAIT", "HALT"})


class PacketValidationError(ValueError):
    """Raised when a packet violates the canonical packet schema."""


def _require_non_empty(value: str | None, *, field_name: str) -> None:
    if value is None or not str(value).strip():
        raise PacketValidationError(f"{field_name} must be non-empty")


def _validate_iso_timestamp(value: str, *, field_name: str) -> None:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise PacketValidationError(f"{field_name} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise PacketValidationError(f"{field_name} must include timezone information")


def _validate_envelope(envelope: PacketEnvelope) -> None:
    _require_non_empty(envelope.run_id, field_name="run_id")
    _require_non_empty(envelope.trace_id, field_name="trace_id")
    _require_non_empty(envelope.actor.id, field_name="actor.id")
    if envelope.actor.type not in ALLOWED_ACTOR_TYPES:
        raise PacketValidationError(f"actor.type must be one of {sorted(ALLOWED_ACTOR_TYPES)}")
    _validate_iso_timestamp(envelope.created_at, field_name="created_at")
    if envelope.sequence_number < 0:
        raise PacketValidationError("sequence_number must be >= 0")
    if envelope.parent_run_id is not None:
        _require_non_empty(envelope.parent_run_id, field_name="parent_run_id")


def validate_evidence_packet(packet: EvidencePacket) -> EvidencePacket:
    _validate_envelope(packet.envelope)
    _require_non_empty(packet.subject_hash, field_name="subject_hash")
    _require_non_empty(packet.kind, field_name="kind")
    _require_non_empty(packet.environment_hash, field_name="environment_hash")
    for name, value in packet.metrics.items():
        if not math.isfinite(float(value)):
            raise PacketValidationError(f"metrics[{name}] must be finite")
    return packet


def validate_decision_packet(packet: DecisionPacket) -> DecisionPacket:
    _validate_envelope(packet.envelope)
    _require_non_empty(packet.decision_kind, field_name="decision_kind")
    if not isinstance(packet.result, dict):
        raise PacketValidationError("result must be a mapping")
    return packet


def validate_gate_result(packet: GateResult) -> GateResult:
    _validate_envelope(packet.envelope)
    _require_non_empty(packet.stage, field_name="stage")
    if packet.status not in ALLOWED_GATE_STATUS:
        raise PacketValidationError(f"status must be one of {sorted(ALLOWED_GATE_STATUS)}")
    return packet


def validate_run_record(record: RunRecord) -> RunRecord:
    _require_non_empty(record.run_id, field_name="run_id")
    _require_non_empty(record.trace_id, field_name="trace_id")
    _require_non_empty(record.actor.id, field_name="actor.id")
    if record.actor.type not in ALLOWED_ACTOR_TYPES:
        raise PacketValidationError(f"actor.type must be one of {sorted(ALLOWED_ACTOR_TYPES)}")
    _require_non_empty(record.intent, field_name="intent")
    _validate_iso_timestamp(record.started_at, field_name="started_at")
    if record.event_count < 0:
        raise PacketValidationError("event_count must be >= 0")
    return record
