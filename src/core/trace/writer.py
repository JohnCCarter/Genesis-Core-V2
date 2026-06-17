"""Run-trace writer (ADR 0002).

One writer owns one run. It writes:
- ``<run_id>/run.json``: authoritative ``RunRecord`` (atomic replace).
- ``<run_id>/events.jsonl``: append-only, one packet payload per line.
- ``index.jsonl``: append-only, rebuildable cache (one line per ``run.json`` update).

The writer is the single source of run context: it stamps each emitted packet's envelope with the
run's ``run_id``/``trace_id``/``actor``, a monotonic ``sequence_number``, and a ``created_at``
timestamp. ``content_hash`` is unaffected (it hashes the body only), so identity stays reproducible.

A clock callable is injectable so tests stay deterministic.
"""

from __future__ import annotations

import dataclasses
import json
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from core.packets.models import (
    Actor,
    DecisionPacket,
    EvidencePacket,
    GateResult,
    PacketEnvelope,
    RunRecord,
)
from core.trace._atomic import append_line, atomic_write_text, compact_json_line
from core.trace.paths import events_path, index_path, run_json_path, trace_root
from core.trace.paths import run_dir as _run_dir_path
from core.utils.json_stable import json_dumps_stable

Packet = EvidencePacket | DecisionPacket | GateResult


def _default_clock() -> str:
    return datetime.now(UTC).isoformat()


class TraceWriter:
    """Append-only writer for a single run."""

    def __init__(
        self,
        *,
        run_id: str,
        actor: Actor,
        intent: str,
        trace_id: str | None = None,
        symbol: str | None = None,
        timeframe: str | None = None,
        parent_run_id: str | None = None,
        started_at: str | None = None,
        root: Path | None = None,
        clock: Callable[[], str] | None = None,
    ) -> None:
        self._clock = clock or _default_clock
        self._root = Path(root) if root is not None else trace_root()
        self._run_id = str(run_id)
        self._trace_id = str(trace_id) if trace_id else self._run_id
        self._actor = actor
        self._intent = str(intent)
        self._symbol = symbol
        self._timeframe = timeframe
        self._parent_run_id = parent_run_id
        self._started_at = str(started_at) if started_at else self._clock()
        self._seq = 0
        self._event_count = 0
        self._outcome: str | None = None
        self._ended_at: str | None = None
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self._write_run_json()

    @property
    def run_id(self) -> str:
        return self._run_id

    @property
    def run_dir(self) -> Path:
        return _run_dir_path(self._run_id, root=self._root)

    def _record(self) -> RunRecord:
        return RunRecord(
            run_id=self._run_id,
            trace_id=self._trace_id,
            actor=self._actor,
            intent=self._intent,
            started_at=self._started_at,
            parent_run_id=self._parent_run_id,
            symbol=self._symbol,
            timeframe=self._timeframe,
            ended_at=self._ended_at,
            outcome=self._outcome,
            event_count=self._event_count,
            dir=str(self.run_dir),
        )

    def _write_run_json(self) -> RunRecord:
        record = self._record()
        atomic_write_text(
            run_json_path(self._run_id, root=self._root),
            json_dumps_stable(record.to_payload()),
        )
        append_line(index_path(root=self._root), compact_json_line(record.to_payload()))
        return record

    def emit(self, packet: Packet) -> str:
        """Stamp the packet with run context + next sequence number, persist it, return content_hash."""

        seq = self._seq
        self._seq += 1
        envelope = PacketEnvelope(
            run_id=self._run_id,
            trace_id=self._trace_id,
            actor=self._actor,
            created_at=self._clock(),
            sequence_number=seq,
            parent_run_id=self._parent_run_id,
        )
        stamped = dataclasses.replace(packet, envelope=envelope)
        payload = stamped.to_payload()
        append_line(events_path(self._run_id, root=self._root), compact_json_line(payload))
        self._event_count += 1
        if isinstance(stamped, GateResult):
            self._outcome = stamped.status
        self._write_run_json()
        return str(payload["content_hash"])

    def _context_envelope(self) -> PacketEnvelope:
        # Placeholder envelope for the record_* convenience builders; emit() re-stamps it
        # with the authoritative sequence number, so callers never construct envelopes.
        return PacketEnvelope(
            run_id=self._run_id,
            trace_id=self._trace_id,
            actor=self._actor,
            created_at=self._clock(),
            sequence_number=self._seq,
            parent_run_id=self._parent_run_id,
        )

    def record_evidence(
        self,
        *,
        subject_hash: str,
        kind: str,
        environment_hash: str,
        inputs: dict | None = None,
        metrics: dict[str, float] | None = None,
        dataset_refs: tuple[str, ...] = (),
        artifact_refs: tuple[str, ...] = (),
        summary: str = "",
    ) -> str:
        return self.emit(
            EvidencePacket(
                envelope=self._context_envelope(),
                subject_hash=subject_hash,
                kind=kind,
                environment_hash=environment_hash,
                inputs=dict(inputs or {}),
                metrics=dict(metrics or {}),
                dataset_refs=tuple(dataset_refs),
                artifact_refs=tuple(artifact_refs),
                summary=summary,
            )
        )

    def record_decision(
        self,
        *,
        decision_kind: str,
        result: dict | None = None,
        input_evidence_refs: tuple[str, ...] = (),
        reasons: tuple[str, ...] = (),
    ) -> str:
        return self.emit(
            DecisionPacket(
                envelope=self._context_envelope(),
                decision_kind=decision_kind,
                result=dict(result or {}),
                input_evidence_refs=tuple(input_evidence_refs),
                reasons=tuple(reasons),
            )
        )

    def record_gate(
        self,
        *,
        stage: str,
        status: str,
        criteria_snapshot: dict | None = None,
        blocking_evidence_refs: tuple[str, ...] = (),
        signoff_ref: str | None = None,
        issued_by: str = "",
    ) -> str:
        return self.emit(
            GateResult(
                envelope=self._context_envelope(),
                stage=stage,
                status=status,
                criteria_snapshot=dict(criteria_snapshot or {}),
                blocking_evidence_refs=tuple(blocking_evidence_refs),
                signoff_ref=signoff_ref,
                issued_by=issued_by,
            )
        )

    def close(self, *, outcome: str | None = None, ended_at: str | None = None) -> RunRecord:
        if outcome is not None:
            self._outcome = str(outcome)
        self._ended_at = str(ended_at) if ended_at else self._clock()
        return self._write_run_json()


def rebuild_index(*, root: Path | None = None) -> int:
    """Rebuild ``index.jsonl`` from the authoritative per-run ``run.json`` files.

    The index is a cache; ``run.json`` is the source of truth. Returns the number of runs indexed.
    """

    base = Path(root) if root is not None else trace_root()
    if not base.exists():
        return 0

    lines: list[str] = []
    for child in sorted(base.iterdir()):
        candidate = child / "run.json"
        if not (child.is_dir() and candidate.exists()):
            continue
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(payload, dict):
            lines.append(compact_json_line(payload))

    atomic_write_text(index_path(root=base), ("\n".join(lines) + "\n") if lines else "")
    return len(lines)
