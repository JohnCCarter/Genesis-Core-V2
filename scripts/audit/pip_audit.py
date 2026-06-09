"""Run pip-audit with the current Genesis-Core-V2 baseline policy.

Why this exists
---------------
A plain `pip-audit` run currently reports known vulnerabilities in pinned dependencies
that are not being widened in this bounded tooling slice. We still want a repeatable,
repo-local dependency audit loop, but we also want CI to stay green until those
upgrades are handled in dedicated dependency slices.

This wrapper:
- runs `python -m pip_audit`
- points pip-audit at the active interpreter explicitly
- applies the current baseline ignore list by default
- supports `--strict` to run without the baseline ignores
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Final

_BASELINE_IGNORES: Final[dict[str, str]] = {}


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "pyproject.toml").is_file() and (parent / "src").is_dir():
            return parent
    return here.parents[2]


def _build_command(*, strict: bool) -> tuple[str, ...]:
    command: list[str] = [sys.executable, "-m", "pip_audit", "--progress-spinner", "off"]
    if not strict:
        for vulnerability_id in _BASELINE_IGNORES:
            command.extend(["--ignore-vuln", vulnerability_id])
    return tuple(command)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Run without the current baseline ignore list.",
    )
    args = parser.parse_args(argv)

    repo_root = _find_repo_root()
    command = _build_command(strict=bool(args.strict))
    env = os.environ.copy()
    env["PIPAPI_PYTHON_LOCATION"] = sys.executable

    if not args.strict:
        print("[INFO] Applying pip-audit baseline ignores:")
        for vulnerability_id, reason in _BASELINE_IGNORES.items():
            print(f"- {vulnerability_id}: {reason}")

    # nosemgrep: python.lang.security.audit.dangerous-subprocess-use-audit
    completed = subprocess.run(command, cwd=repo_root, env=env, check=False, shell=False)
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
