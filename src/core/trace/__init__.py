"""Agent-readable run-trace substrate (ADR 0002): writer + filesystem layout."""

from __future__ import annotations

from core.trace.paths import (
    events_path,
    index_path,
    run_dir,
    run_json_path,
    trace_root,
)
from core.trace.reader import (
    TraceError,
    TraceNotFoundError,
    TraceReadError,
    find_runs,
    follow_parents,
    latest_run,
    parse_packet,
    read_events,
    read_evidence,
    read_run,
)
from core.trace.recorder import (
    new_run_id,
    record_backtest_run,
    record_candidate_build,
    resolve_actor_from_env,
)
from core.trace.writer import TraceWriter, rebuild_index

__all__ = [
    "TraceError",
    "TraceNotFoundError",
    "TraceReadError",
    "TraceWriter",
    "events_path",
    "find_runs",
    "follow_parents",
    "index_path",
    "latest_run",
    "new_run_id",
    "parse_packet",
    "read_events",
    "read_evidence",
    "read_run",
    "rebuild_index",
    "record_backtest_run",
    "record_candidate_build",
    "resolve_actor_from_env",
    "run_dir",
    "run_json_path",
    "trace_root",
]
