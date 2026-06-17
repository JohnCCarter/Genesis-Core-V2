"""Minimal typed packet contract for the agent-readable run-trace.

This is the V2-local, contract-clean inter-agent schema described in ADR 0002. Packets are
pure, serializable, content-addressed records. They carry evidence/decisions; they never issue
promotion authority.

Two distinct identities (ADR 0002):
- ``run_id``: *which execution* (locator; supplied by the writer, non-deterministic).
- ``content_hash``: *what the record is* (identity; a deterministic fingerprint of the body only,
  excluding every volatile envelope field). This is what another agent trusts and reproduces.

These models are pure and side-effect free: ``created_at``/``run_id`` are passed in, never sampled
here, so the layer stays deterministic and testable. Disk I/O and emit wiring live elsewhere.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar

from core.utils.diffing.canonical import fingerprint_config
from core.utils.json_stable import JsonObject
from core.utils.logging_redaction import redact_mapping, redact_text

ENVELOPE_SCHEMA_VERSION = "genesis_packet.v1"
EVIDENCE_PACKET_VERSION = "evidence_packet.v1"
DECISION_PACKET_VERSION = "decision_packet.v1"
GATE_RESULT_VERSION = "gate_result.v1"
RUN_RECORD_VERSION = "run_record.v1"


def compute_content_hash(body: JsonObject) -> str:
    """Deterministic content fingerprint of a packet body (envelope excluded)."""

    return fingerprint_config(body)


@dataclass(frozen=True, slots=True)
class Actor:
    """Who produced a record: a human or an agent."""

    type: str  # "human" | "agent"
    id: str

    def to_payload(self) -> JsonObject:
        return {"id": str(self.id), "type": str(self.type)}

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> Actor:
        return cls(type=str(payload.get("type", "")), id=str(payload.get("id", "")))


@dataclass(frozen=True, slots=True)
class PacketEnvelope:
    """Common, metadata-only envelope shared by every packet.

    None of these fields enter ``content_hash`` — they locate and order a record, they do not
    define its identity.
    """

    run_id: str
    trace_id: str
    actor: Actor
    created_at: str  # ISO-8601 UTC; metadata-only
    sequence_number: int = 0
    parent_run_id: str | None = None

    def to_payload(self) -> JsonObject:
        return {
            "actor": self.actor.to_payload(),
            "created_at": str(self.created_at),
            "parent_run_id": (str(self.parent_run_id) if self.parent_run_id is not None else None),
            "run_id": str(self.run_id),
            "schema_version": ENVELOPE_SCHEMA_VERSION,
            "sequence_number": int(self.sequence_number),
            "trace_id": str(self.trace_id),
        }

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> PacketEnvelope:
        return cls(
            run_id=str(payload.get("run_id", "")),
            trace_id=str(payload.get("trace_id", "")),
            actor=Actor.from_payload(payload.get("actor") or {}),
            created_at=str(payload.get("created_at", "")),
            sequence_number=int(payload.get("sequence_number", 0)),
            parent_run_id=(
                str(payload["parent_run_id"]) if payload.get("parent_run_id") is not None else None
            ),
        )


@dataclass(frozen=True, slots=True)
class EvidencePacket:
    """A reproducible unit of evidence another agent can consume."""

    envelope: PacketEnvelope
    subject_hash: str
    kind: str  # backtest | oos | metrics | comparison | ...
    environment_hash: str
    inputs: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, float] = field(default_factory=dict)
    dataset_refs: tuple[str, ...] = ()
    artifact_refs: tuple[str, ...] = ()
    summary: str = ""

    packet_type: ClassVar[str] = "evidence"
    packet_version: ClassVar[str] = EVIDENCE_PACKET_VERSION

    def body(self) -> JsonObject:
        """Hashed, redacted body (no envelope, no secrets)."""

        return {
            "artifact_refs": [str(ref) for ref in self.artifact_refs],
            "dataset_refs": [str(ref) for ref in self.dataset_refs],
            "environment_hash": str(self.environment_hash),
            "inputs": redact_mapping(dict(self.inputs)),
            "kind": str(self.kind),
            "metrics": {str(k): float(v) for k, v in self.metrics.items()},
            "subject_hash": str(self.subject_hash),
            "summary": redact_text(str(self.summary)),
        }

    def content_hash(self) -> str:
        return compute_content_hash(self.body())

    def to_payload(self) -> JsonObject:
        return {
            **self.envelope.to_payload(),
            **self.body(),
            "content_hash": self.content_hash(),
            "packet_type": self.packet_type,
            "packet_version": self.packet_version,
        }

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> EvidencePacket:
        return cls(
            envelope=PacketEnvelope.from_payload(payload),
            subject_hash=str(payload.get("subject_hash", "")),
            kind=str(payload.get("kind", "")),
            environment_hash=str(payload.get("environment_hash", "")),
            inputs=dict(payload.get("inputs") or {}),
            metrics={str(k): float(v) for k, v in (payload.get("metrics") or {}).items()},
            dataset_refs=tuple(str(ref) for ref in (payload.get("dataset_refs") or [])),
            artifact_refs=tuple(str(ref) for ref in (payload.get("artifact_refs") or [])),
            summary=str(payload.get("summary", "")),
        )


@dataclass(frozen=True, slots=True)
class DecisionPacket:
    """A recorded decision; wraps existing decision results, does not replace them."""

    envelope: PacketEnvelope
    decision_kind: str  # comparison | promotion | premortem | route
    result: dict[str, Any] = field(default_factory=dict)
    input_evidence_refs: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()

    packet_type: ClassVar[str] = "decision"
    packet_version: ClassVar[str] = DECISION_PACKET_VERSION

    def body(self) -> JsonObject:
        return {
            "decision_kind": str(self.decision_kind),
            "input_evidence_refs": [str(ref) for ref in self.input_evidence_refs],
            "reasons": [str(reason) for reason in self.reasons],
            "result": dict(self.result),
        }

    def content_hash(self) -> str:
        return compute_content_hash(self.body())

    def to_payload(self) -> JsonObject:
        return {
            **self.envelope.to_payload(),
            **self.body(),
            "content_hash": self.content_hash(),
            "packet_type": self.packet_type,
            "packet_version": self.packet_version,
        }

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> DecisionPacket:
        return cls(
            envelope=PacketEnvelope.from_payload(payload),
            decision_kind=str(payload.get("decision_kind", "")),
            result=dict(payload.get("result") or {}),
            input_evidence_refs=tuple(
                str(ref) for ref in (payload.get("input_evidence_refs") or [])
            ),
            reasons=tuple(str(reason) for reason in (payload.get("reasons") or [])),
        )


@dataclass(frozen=True, slots=True)
class GateResult:
    """A recorded gate outcome. Authority stays in the decision/governance code; this only records."""

    envelope: PacketEnvelope
    stage: str  # research | backtest | validate | paper | shadow | champion | live
    status: str  # PASS | FAIL | WAIT | HALT
    criteria_snapshot: dict[str, Any] = field(default_factory=dict)
    blocking_evidence_refs: tuple[str, ...] = ()
    signoff_ref: str | None = None
    issued_by: str = ""

    packet_type: ClassVar[str] = "gate_result"
    packet_version: ClassVar[str] = GATE_RESULT_VERSION

    def body(self) -> JsonObject:
        return {
            "blocking_evidence_refs": [str(ref) for ref in self.blocking_evidence_refs],
            "criteria_snapshot": dict(self.criteria_snapshot),
            "issued_by": str(self.issued_by),
            "signoff_ref": (str(self.signoff_ref) if self.signoff_ref is not None else None),
            "stage": str(self.stage),
            "status": str(self.status),
        }

    def content_hash(self) -> str:
        return compute_content_hash(self.body())

    def to_payload(self) -> JsonObject:
        return {
            **self.envelope.to_payload(),
            **self.body(),
            "content_hash": self.content_hash(),
            "packet_type": self.packet_type,
            "packet_version": self.packet_version,
        }

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> GateResult:
        return cls(
            envelope=PacketEnvelope.from_payload(payload),
            stage=str(payload.get("stage", "")),
            status=str(payload.get("status", "")),
            criteria_snapshot=dict(payload.get("criteria_snapshot") or {}),
            blocking_evidence_refs=tuple(
                str(ref) for ref in (payload.get("blocking_evidence_refs") or [])
            ),
            signoff_ref=(
                str(payload["signoff_ref"]) if payload.get("signoff_ref") is not None else None
            ),
            issued_by=str(payload.get("issued_by", "")),
        )


@dataclass(frozen=True, slots=True)
class RunRecord:
    """Trace envelope + index entry for a run. Mutable run state (authoritative ``run.json``)."""

    run_id: str
    trace_id: str
    actor: Actor
    intent: str
    started_at: str
    parent_run_id: str | None = None
    symbol: str | None = None
    timeframe: str | None = None
    ended_at: str | None = None
    outcome: str | None = None
    event_count: int = 0
    dir: str = ""

    schema_version: ClassVar[str] = RUN_RECORD_VERSION

    def to_payload(self) -> JsonObject:
        return {
            "actor": self.actor.to_payload(),
            "dir": str(self.dir),
            "ended_at": (str(self.ended_at) if self.ended_at is not None else None),
            "event_count": int(self.event_count),
            "intent": str(self.intent),
            "outcome": (str(self.outcome) if self.outcome is not None else None),
            "parent_run_id": (str(self.parent_run_id) if self.parent_run_id is not None else None),
            "run_id": str(self.run_id),
            "schema_version": self.schema_version,
            "started_at": str(self.started_at),
            "symbol": (str(self.symbol) if self.symbol is not None else None),
            "timeframe": (str(self.timeframe) if self.timeframe is not None else None),
            "trace_id": str(self.trace_id),
        }

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> RunRecord:
        def _opt(key: str) -> str | None:
            value = payload.get(key)
            return str(value) if value is not None else None

        return cls(
            run_id=str(payload.get("run_id", "")),
            trace_id=str(payload.get("trace_id", "")),
            actor=Actor.from_payload(payload.get("actor") or {}),
            intent=str(payload.get("intent", "")),
            started_at=str(payload.get("started_at", "")),
            parent_run_id=_opt("parent_run_id"),
            symbol=_opt("symbol"),
            timeframe=_opt("timeframe"),
            ended_at=_opt("ended_at"),
            outcome=_opt("outcome"),
            event_count=int(payload.get("event_count", 0)),
            dir=str(payload.get("dir", "")),
        )
