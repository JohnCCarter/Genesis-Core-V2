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
        "NVIDIA_API_KEY=change-me",
        "NVIDIA_API_BASE=https://integrate.api.nvidia.com/v1",
        "NVIDIA_QWEN_MODEL=qwen/qwen3-coder-480b-a35b-instruct",
        "SYMBOL_MODE=realistic",
        "LOG_LEVEL=INFO",
    ]:
        assert expected_line in template_text
