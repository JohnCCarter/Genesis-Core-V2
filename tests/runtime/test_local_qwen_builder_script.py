from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from genesis_core_v2_cli import qwen_builder as qwen_builder_module


def _run_local_qwen_builder(*args: str) -> dict[str, object]:
    repo_root = Path(__file__).resolve().parents[2]

    completed = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "ai" / "qwen_builder.py"), *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(completed.stdout)


def test_local_qwen_builder_script_prints_runtime_config() -> None:
    payload = _run_local_qwen_builder("--print-config")

    assert "credential_env" not in payload
    assert payload["api_base"] == "https://integrate.api.nvidia.com/v1"
    assert payload["model"] == "qwen/qwen3-coder-480b-a35b-instruct"
    assert payload["temperature"] == 0.4
    assert payload["top_p"] == 0.8
    assert payload["max_tokens"] == 4096
    assert payload["stream"] is False


def test_local_qwen_builder_script_prints_streaming_runtime_config() -> None:
    payload = _run_local_qwen_builder("--print-config", "--stream")

    assert "credential_env" not in payload
    assert payload["api_base"] == "https://integrate.api.nvidia.com/v1"
    assert payload["model"] == "qwen/qwen3-coder-480b-a35b-instruct"
    assert payload["stream"] is True


def test_local_qwen_builder_prefers_repo_env_over_inherited_shell_key(
    monkeypatch, tmp_path: Path
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("NVIDIA_API_KEY=file-value\n", encoding="utf-8")

    monkeypatch.setattr(qwen_builder_module, "ENV_FILE", env_file)
    monkeypatch.setenv("NVIDIA_API_KEY", "shell-value")

    qwen_builder_module._load_local_env()

    assert os.environ["NVIDIA_API_KEY"] == "file-value"
