"""Run-trace reader/query API (ADR 0002).

This is the inter-agent read surface: it lets one agent (or the human) reconstruct exactly what
another agent did. All functions are read-only, deterministic, and fail-closed — malformed records
raise a typed error rather than being silently skipped.

``run.json`` is authoritative for a single run; ``index.jsonl`` is used for discovery and is
rebuildable. When the index is absent, discovery falls back to scanning the per-run ``run.json``
files so reads stay correct.
"""

from __future__ import annotations

import json
from pathlib import Path

from core.packets.models import DecisionPacket, EvidencePacket, GateResult, RunRecord
from core.trace.paths import events_path, index_path, run_dir, run_json_path, trace_root

Packet = EvidencePacket | DecisionPacket | GateResult

_PACKET_BY_TYPE: dict[str, type[Packet]] = {
    "evidence": EvidencePacket,
    "decision": DecisionPacket,
    "gate_result": GateResult,
}


class TraceError(Exception):
    """Base class for run-trace read errors."""


class TraceNotFoundError(TraceError):
    """Raised when a requested run does not exist."""


class TraceReadError(TraceError):
    """Raised when a trace record cannot be parsed (fail-closed, never silently skipped)."""


def parse_packet(payload: dict) -> Packet:
    packet_type = payload.get("packet_type")
    cls = _PACKET_BY_TYPE.get(str(packet_type))
    if cls is None:
        raise TraceReadError(f"unknown packet_type: {packet_type!r}")
    return cls.from_payload(payload)


def _load_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise TraceReadError(f"unreadable trace record: {path}") from exc
    if not isinstance(payload, dict):
        raise TraceReadError(f"trace record is not an object: {path}")
    return payload


def _latest_index_records(*, root: Path | None = None) -> list[dict]:
    """Return the latest record per run_id, from the index cache or a run.json scan fallback."""

    base = Path(root) if root is not None else trace_root()
    folded: dict[str, dict] = {}

    index_file = index_path(root=base)
    if index_file.exists():
        for line in index_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            try:
                record = json.loads(stripped)
            except ValueError as exc:
                raise TraceReadError("corrupt index.jsonl line") from exc
            if isinstance(record, dict) and record.get("run_id"):
                folded[str(record["run_id"])] = record
        return list(folded.values())

    if base.exists():
        for child in sorted(base.iterdir()):
            candidate = child / "run.json"
            if child.is_dir() and candidate.exists():
                record = _load_json(candidate)
                if record.get("run_id"):
                    folded[str(record["run_id"])] = record
    return list(folded.values())


def read_run(run_id: str, *, root: Path | None = None) -> RunRecord:
    path = run_json_path(run_id, root=root)
    if not path.exists():
        raise TraceNotFoundError(f"no run: {run_id}")
    return RunRecord.from_payload(_load_json(path))


def read_events(run_id: str, *, root: Path | None = None) -> list[Packet]:
    directory = run_dir(run_id, root=root)
    if not directory.exists():
        raise TraceNotFoundError(f"no run: {run_id}")
    path = events_path(run_id, root=root)
    if not path.exists():
        return []
    packets: list[Packet] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            payload = json.loads(stripped)
        except ValueError as exc:
            raise TraceReadError(f"corrupt events.jsonl line in run {run_id}") from exc
        packets.append(parse_packet(payload))
    return packets


def find_runs(
    *,
    intent: str | None = None,
    symbol: str | None = None,
    timeframe: str | None = None,
    outcome: str | None = None,
    actor_id: str | None = None,
    root: Path | None = None,
) -> list[RunRecord]:
    records = [RunRecord.from_payload(record) for record in _latest_index_records(root=root)]

    def _keep(record: RunRecord) -> bool:
        if intent is not None and record.intent != intent:
            return False
        if symbol is not None and record.symbol != symbol:
            return False
        if timeframe is not None and record.timeframe != timeframe:
            return False
        if outcome is not None and record.outcome != outcome:
            return False
        if actor_id is not None and record.actor.id != actor_id:
            return False
        return True

    matches = [record for record in records if _keep(record)]
    matches.sort(key=lambda record: record.started_at)
    return matches


def latest_run(
    *,
    intent: str | None = None,
    symbol: str | None = None,
    timeframe: str | None = None,
    outcome: str | None = None,
    actor_id: str | None = None,
    root: Path | None = None,
) -> RunRecord | None:
    matches = find_runs(
        intent=intent,
        symbol=symbol,
        timeframe=timeframe,
        outcome=outcome,
        actor_id=actor_id,
        root=root,
    )
    return matches[-1] if matches else None


def follow_parents(run_id: str, *, root: Path | None = None) -> list[RunRecord]:
    """Return the causal chain [run, parent, grandparent, ...]; best-effort, cycle-safe."""

    chain: list[RunRecord] = []
    seen: set[str] = set()
    current: str | None = run_id
    while current and current not in seen:
        seen.add(current)
        try:
            record = read_run(current, root=root)
        except TraceNotFoundError:
            break
        chain.append(record)
        current = record.parent_run_id
    return chain


def read_evidence(content_hash: str, *, root: Path | None = None) -> EvidencePacket | None:
    """Content-addressed lookup of an evidence packet across all runs."""

    for record in _latest_index_records(root=root):
        run_id = str(record.get("run_id", ""))
        if not run_id:
            continue
        try:
            packets = read_events(run_id, root=root)
        except TraceNotFoundError:
            continue
        for packet in packets:
            if isinstance(packet, EvidencePacket) and packet.content_hash() == content_hash:
                return packet
    return None
