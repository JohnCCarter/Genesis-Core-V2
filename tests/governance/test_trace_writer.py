from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from core.packets import Actor, EvidencePacket, GateResult, PacketEnvelope
from core.trace import (
    TraceWriter,
    events_path,
    index_path,
    rebuild_index,
    run_json_path,
)

_TS = "2026-06-17T12:00:00+00:00"


def _clock() -> str:
    return _TS


def _dummy_env() -> PacketEnvelope:
    # The writer overwrites the envelope on emit, so these values are placeholders.
    return PacketEnvelope(
        run_id="dummy", trace_id="dummy", actor=Actor(type="agent", id="dummy"), created_at=_TS
    )


def _evidence(**overrides) -> EvidencePacket:
    base = {
        "envelope": _dummy_env(),
        "subject_hash": "s1",
        "kind": "backtest",
        "environment_hash": "e1",
        "metrics": {"profit_factor": 1.25},
    }
    base.update(overrides)
    return EvidencePacket(**base)


def _writer(tmp_path: Path, **overrides) -> TraceWriter:
    base = {
        "run_id": "run_X",
        "actor": Actor(type="agent", id="claude"),
        "intent": "backtest",
        "root": tmp_path,
        "clock": _clock,
    }
    base.update(overrides)
    return TraceWriter(**base)


def test_run_json_created_on_init(tmp_path: Path) -> None:
    _writer(tmp_path)
    record = json.loads(run_json_path("run_X", root=tmp_path).read_text(encoding="utf-8"))
    assert record["run_id"] == "run_X"
    assert record["intent"] == "backtest"
    assert record["event_count"] == 0


def test_emit_appends_events_and_stamps_context(tmp_path: Path) -> None:
    writer = _writer(tmp_path)
    writer.emit(_evidence())
    writer.emit(GateResult(envelope=_dummy_env(), stage="validate", status="PASS"))

    lines = events_path("run_X", root=tmp_path).read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    first, second = json.loads(lines[0]), json.loads(lines[1])
    # Envelope is overwritten with run context + monotonic sequence numbers.
    assert first["run_id"] == "run_X"
    assert first["sequence_number"] == 0
    assert second["sequence_number"] == 1
    assert second["status"] == "PASS"

    record = json.loads(run_json_path("run_X", root=tmp_path).read_text(encoding="utf-8"))
    assert record["event_count"] == 2
    assert record["outcome"] == "PASS"  # last gate status becomes the run outcome


def test_index_latest_line_reflects_final_state(tmp_path: Path) -> None:
    writer = _writer(tmp_path)
    writer.emit(_evidence())
    writer.emit(_evidence(subject_hash="s2"))
    writer.close(outcome="PASS")

    lines = index_path(root=tmp_path).read_text(encoding="utf-8").splitlines()
    runs = [json.loads(line) for line in lines]
    assert all(run["run_id"] == "run_X" for run in runs)
    latest = runs[-1]
    assert latest["event_count"] == 2
    assert latest["outcome"] == "PASS"
    assert latest["ended_at"] is not None


def test_rebuild_index_from_run_json(tmp_path: Path) -> None:
    _writer(tmp_path, run_id="run_A").close()
    _writer(tmp_path, run_id="run_B").close()
    index_path(root=tmp_path).unlink()

    count = rebuild_index(root=tmp_path)
    assert count == 2

    ids = sorted(
        json.loads(line)["run_id"]
        for line in index_path(root=tmp_path).read_text(encoding="utf-8").splitlines()
    )
    assert ids == ["run_A", "run_B"]


def test_two_runs_are_isolated(tmp_path: Path) -> None:
    writer_a = _writer(tmp_path, run_id="run_A")
    writer_a.emit(_evidence())
    writer_b = _writer(tmp_path, run_id="run_B")
    writer_b.emit(_evidence())
    writer_b.emit(_evidence(subject_hash="s2"))

    assert len(events_path("run_A", root=tmp_path).read_text(encoding="utf-8").splitlines()) == 1
    assert len(events_path("run_B", root=tmp_path).read_text(encoding="utf-8").splitlines()) == 2


def test_emit_preserves_content_hash_identity(tmp_path: Path) -> None:
    packet = _evidence()
    expected = packet.content_hash()
    hash_a = _writer(tmp_path, run_id="run_A").emit(packet)
    hash_b = _writer(tmp_path, run_id="run_B", actor=Actor(type="human", id="kingpin")).emit(packet)
    # Identity is independent of which run/actor/sequence recorded it.
    assert hash_a == hash_b == expected


def test_default_clock_is_iso_utc(tmp_path: Path) -> None:
    writer = TraceWriter(
        run_id="run_C", actor=Actor(type="agent", id="claude"), intent="backtest", root=tmp_path
    )
    writer.emit(_evidence())
    line = json.loads(
        events_path("run_C", root=tmp_path).read_text(encoding="utf-8").splitlines()[0]
    )
    assert datetime.fromisoformat(line["created_at"]).tzinfo is not None


def test_env_override_trace_root(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("GENESIS_TRACE_ROOT", str(tmp_path / "envroot"))
    writer = TraceWriter(run_id="run_E", actor=Actor(type="agent", id="claude"), intent="backtest")
    writer.emit(_evidence())
    assert (tmp_path / "envroot" / "run_E" / "run.json").exists()
