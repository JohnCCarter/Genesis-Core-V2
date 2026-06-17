"""Small, local atomic-write / append helpers for the trace layer.

Kept local (not imported from config/optimizer) so the trace foundation does not couple to those
surfaces. Mirrors the proven tmp+fsync+replace pattern in ``config/authority.py``.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from core.utils.json_stable import JsonObject


def atomic_write_text(path: Path, text: str) -> None:
    """Write text atomically: tmp file in the same dir, fsync, then replace."""

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)
    try:
        dir_fd = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    except (OSError, AttributeError):  # O_DIRECTORY is unavailable on Windows  # nosec B110
        pass


def append_line(path: Path, line: str) -> None:
    """Append exactly one newline-terminated line."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(line.rstrip("\n") + "\n")
        handle.flush()


def compact_json_line(payload: JsonObject) -> str:
    """Serialize one JSON object to a single deterministic line (for *.jsonl)."""

    return json.dumps(payload, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
