from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest


def _load_pip_audit_script_module():
    repo_root = Path(__file__).resolve().parents[2]
    script_path = repo_root / "scripts" / "audit" / "pip_audit.py"
    spec = importlib.util.spec_from_file_location("genesis_v2_pip_audit_script", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_local_pip_audit_script_uses_baseline_ignores(monkeypatch) -> None:
    module = _load_pip_audit_script_module()
    captured: dict[str, Any] = {}

    def _fake_run(command, *, cwd, env, check, shell):
        captured["command"] = command
        captured["cwd"] = cwd
        captured["env"] = env
        captured["check"] = check

        class _Result:
            returncode = 0

        return _Result()

    monkeypatch.setattr(module.subprocess, "run", _fake_run)

    rc = module.main([])

    assert rc == 0
    assert list(captured["command"][:4]) == [
        sys.executable,
        "-m",
        "pip_audit",
        "--progress-spinner",
    ]
    assert captured["command"][4] == "off"
    assert captured["check"] is False
    assert captured["cwd"] == Path(__file__).resolve().parents[2]
    assert captured["env"]["PIPAPI_PYTHON_LOCATION"] == sys.executable
    ignore_args: list[str] = []
    for index, value in enumerate(captured["command"]):
        if value == "--ignore-vuln" and index + 1 < len(captured["command"]):
            ignore_args.append(captured["command"][index + 1])

    assert set(ignore_args) == set(module._BASELINE_IGNORES.keys())


def test_local_pip_audit_script_strict_mode_omits_baseline_ignores(monkeypatch) -> None:
    module = _load_pip_audit_script_module()
    captured: dict[str, Any] = {}

    def _fake_run(command, *, cwd, env, check, shell):
        captured["command"] = command
        captured["env"] = env

        class _Result:
            returncode = 0

        return _Result()

    monkeypatch.setattr(module.subprocess, "run", _fake_run)

    rc = module.main(["--strict"])

    assert rc == 0
    assert "--ignore-vuln" not in captured["command"]
    assert captured["env"]["PIPAPI_PYTHON_LOCATION"] == sys.executable


def test_local_pip_audit_script_propagates_failure(monkeypatch) -> None:
    module = _load_pip_audit_script_module()

    def _fake_run(command, *, cwd, env, check, shell):
        class _Result:
            returncode = 5

        return _Result()

    monkeypatch.setattr(module.subprocess, "run", _fake_run)

    with pytest.raises(SystemExit) as exc_info:
        raise SystemExit(module.main([]))

    assert exc_info.value.code == 5
