from __future__ import annotations

from pathlib import Path

import pytest

from core.packets import Actor, EvidencePacket, GateResult, PacketEnvelope
from core.trace import (
    TraceNotFoundError,
    TraceReadError,
    TraceWriter,
    events_path,
    find_runs,
    follow_parents,
    latest_run,
    read_events,
    read_evidence,
    read_run,
    run_json_path,
)

_TS = "2026-06-17T12:00:00+00:00"


def _env() -> PacketEnvelope:
    return PacketEnvelope(
        run_id="dummy", trace_id="dummy", actor=Actor(type="agent", id="dummy"), created_at=_TS
    )


def _evidence(**overrides) -> EvidencePacket:
    base = {
        "envelope": _env(),
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
        "clock": lambda: _TS,
    }
    base.update(overrides)
    return TraceWriter(**base)


def test_read_run_round_trips(tmp_path: Path) -> None:
    _writer(tmp_path, symbol="tBTCUSD", timeframe="1h")
    record = read_run("run_X", root=tmp_path)
    assert record.run_id == "run_X"
    assert record.symbol == "tBTCUSD"
    assert record.intent == "backtest"


def test_read_run_missing_raises(tmp_path: Path) -> None:
    with pytest.raises(TraceNotFoundError):
        read_run("nope", root=tmp_path)


def test_read_events_parses_in_sequence(tmp_path: Path) -> None:
    writer = _writer(tmp_path)
    writer.emit(_evidence())
    writer.emit(GateResult(envelope=_env(), stage="validate", status="PASS"))
    packets = read_events("run_X", root=tmp_path)
    assert [p.envelope.sequence_number for p in packets] == [0, 1]
    assert isinstance(packets[0], EvidencePacket)
    assert isinstance(packets[1], GateResult)


def test_read_events_missing_run_raises_but_empty_run_is_empty(tmp_path: Path) -> None:
    with pytest.raises(TraceNotFoundError):
        read_events("nope", root=tmp_path)
    _writer(tmp_path, run_id="run_empty")  # init only, no events
    assert read_events("run_empty", root=tmp_path) == []


def test_find_and_latest_run_filter_and_order(tmp_path: Path) -> None:
    _writer(
        tmp_path, run_id="run_A", symbol="tBTCUSD", started_at="2026-06-17T10:00:00+00:00"
    ).close(outcome="FAIL")
    _writer(
        tmp_path, run_id="run_B", symbol="tETHUSD", started_at="2026-06-17T11:00:00+00:00"
    ).close(outcome="PASS")

    all_backtests = find_runs(intent="backtest", root=tmp_path)
    assert [r.run_id for r in all_backtests] == ["run_A", "run_B"]  # sorted by started_at

    assert latest_run(intent="backtest", root=tmp_path).run_id == "run_B"
    assert find_runs(symbol="tBTCUSD", root=tmp_path)[0].run_id == "run_A"
    assert latest_run(outcome="PASS", root=tmp_path).run_id == "run_B"
    assert latest_run(intent="does-not-exist", root=tmp_path) is None


def test_follow_parents_reconstructs_chain(tmp_path: Path) -> None:
    _writer(tmp_path, run_id="run_P").close()
    _writer(tmp_path, run_id="run_C", parent_run_id="run_P").close()
    chain = follow_parents("run_C", root=tmp_path)
    assert [r.run_id for r in chain] == ["run_C", "run_P"]
    assert [r.run_id for r in follow_parents("run_P", root=tmp_path)] == ["run_P"]


def test_read_evidence_by_content_hash(tmp_path: Path) -> None:
    writer = _writer(tmp_path)
    content_hash = writer.emit(_evidence(subject_hash="unique-subject"))
    found = read_evidence(content_hash, root=tmp_path)
    assert isinstance(found, EvidencePacket)
    assert found.subject_hash == "unique-subject"
    assert read_evidence("deadbeef", root=tmp_path) is None


def test_discovery_falls_back_to_run_json_when_index_missing(tmp_path: Path) -> None:
    _writer(tmp_path, run_id="run_A").close()
    _writer(tmp_path, run_id="run_B").close()
    (tmp_path / "index.jsonl").unlink()
    ids = sorted(r.run_id for r in find_runs(root=tmp_path))
    assert ids == ["run_A", "run_B"]


def test_unknown_packet_type_fails_closed(tmp_path: Path) -> None:
    _writer(tmp_path, run_id="run_bad")
    events_path("run_bad", root=tmp_path).write_text(
        '{"packet_type":"bogus","run_id":"run_bad"}\n', encoding="utf-8"
    )
    with pytest.raises(TraceReadError):
        read_events("run_bad", root=tmp_path)


def test_corrupt_run_json_fails_closed(tmp_path: Path) -> None:
    _writer(tmp_path, run_id="run_corrupt")
    run_json_path("run_corrupt", root=tmp_path).write_text("{ not json", encoding="utf-8")
    with pytest.raises(TraceReadError):
        read_run("run_corrupt", root=tmp_path)
