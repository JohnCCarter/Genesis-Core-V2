from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


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

    def _fake_run(command, *, cwd, env, check):
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
    assert captured["command"][:4] == [sys.executable, "-m", "pip_audit", "--progress-spinner"]
    assert captured["command"][4] == "off"
    assert captured["check"] is False
    assert captured["cwd"] == Path(__file__).resolve().parents[2]
    assert captured["env"]["PIPAPI_PYTHON_LOCATION"] == sys.executable
    assert "--ignore-vuln" in captured["command"]
    assert "CVE-2025-53366" in captured["command"]
    assert "PYSEC-2026-161" in captured["command"]


def test_local_pip_audit_script_strict_mode_omits_baseline_ignores(monkeypatch) -> None:
    module = _load_pip_audit_script_module()
    captured: dict[str, Any] = {}

    def _fake_run(command, *, cwd, env, check):
        captured["command"] = command

        class _Result:
            returncode = 0

        return _Result()

    monkeypatch.setattr(module.subprocess, "run", _fake_run)

    rc = module.main(["--strict"])

    assert rc == 0
    assert "--ignore-vuln" not in captured["command"]
