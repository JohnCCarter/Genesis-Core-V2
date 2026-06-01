from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"


def _prefer_local_src() -> None:
    normalized_src = str(SRC_ROOT.resolve())
    filtered: list[str] = []
    for entry in sys.path:
        try:
            normalized_entry = str(Path(entry).resolve())
        except Exception:
            normalized_entry = entry
        if normalized_entry == normalized_src:
            continue
        filtered.append(entry)
    sys.path[:] = [str(SRC_ROOT), *filtered]

    core_module = sys.modules.get("core")
    module_file = getattr(core_module, "__file__", None)
    if module_file is None:
        return
    if str(Path(module_file).resolve()).startswith(normalized_src):
        return
    for name in tuple(sys.modules):
        if name == "core" or name.startswith("core."):
            sys.modules.pop(name, None)


def main() -> int:
    _prefer_local_src()
    return import_module("core.bootstrap.champion_smoke").main()


if __name__ == "__main__":
    raise SystemExit(main())
