from __future__ import annotations

from pathlib import Path


def test_local_env_example_tracks_the_narrow_placeholder_values() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    template_text = (repo_root / ".env.example").read_text(encoding="utf-8")

    assert "# Copy this file to .env for local use." in template_text
    for expected_line in [
        "BEARER_TOKEN=change-me",
        "BITFINEX_API_KEY=change-me",
        "BITFINEX_API_SECRET=change-me",
        "SYMBOL_MODE=realistic",
        "LOG_LEVEL=INFO",
    ]:
        assert expected_line in template_text
