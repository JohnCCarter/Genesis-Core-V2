from __future__ import annotations

import argparse
import asyncio
import importlib
import json
import os
import sys
from pathlib import Path
from typing import Any

LOCAL_REPO_ROOT = Path(__file__).resolve().parents[2]
LOCAL_SRC_ROOT = LOCAL_REPO_ROOT / "src"
DEFAULT_MCP_CONFIG_PATH = LOCAL_REPO_ROOT / "config" / "mcp_settings.json"
DEFAULT_PYTEST_ARGS = ["-q"]


def _purge_shadowed_local_package(package_name: str, *, local_prefixes: tuple[str, ...]) -> None:
    module = sys.modules.get(package_name)
    module_file = getattr(module, "__file__", None)
    if module_file is None:
        return
    try:
        normalized_module_file = str(Path(module_file).resolve())
    except Exception:
        normalized_module_file = str(module_file)
    if any(normalized_module_file.startswith(prefix) for prefix in local_prefixes):
        return
    for name in tuple(sys.modules):
        if name == package_name or name.startswith(f"{package_name}."):
            sys.modules.pop(name, None)


def _prefer_local_paths() -> None:
    normalized_local_src = str(LOCAL_SRC_ROOT.resolve())
    normalized_local_repo = str(LOCAL_REPO_ROOT.resolve())
    filtered: list[str] = []
    for entry in sys.path:
        try:
            normalized_entry = str(Path(entry).resolve())
        except Exception:
            normalized_entry = entry
        if normalized_entry in {normalized_local_src, normalized_local_repo}:
            continue
        filtered.append(entry)
    sys.path[:] = [str(LOCAL_SRC_ROOT), str(LOCAL_REPO_ROOT), *filtered]
    _purge_shadowed_local_package("core", local_prefixes=(normalized_local_src,))
    _purge_shadowed_local_package("mcp_server", local_prefixes=(normalized_local_repo,))


def _prefer_local_pythonpath() -> None:
    normalized_src = str(LOCAL_SRC_ROOT)
    existing = [entry for entry in os.environ.get("PYTHONPATH", "").split(os.pathsep) if entry]
    if normalized_src not in existing:
        os.environ["PYTHONPATH"] = (
            os.pathsep.join([normalized_src, *existing]) if existing else normalized_src
        )


def _load_api_server_module():
    import core.server as server_mod

    return server_mod


def _load_mcp_server_module():
    os.environ["GENESIS_MCP_CONFIG_PATH"] = str(DEFAULT_MCP_CONFIG_PATH)

    import mcp_server.server as server_mod

    return server_mod


def _build_api_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local Genesis-Core-V2 API shell")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true")
    parser.add_argument("--print-config", action="store_true")
    return parser


def _build_api_runtime_config(args: argparse.Namespace) -> dict[str, Any]:
    server_mod = _load_api_server_module()
    app = server_mod.app
    routes = app.routes
    return {
        "app": "core.server:app",
        "app_dir": str(LOCAL_SRC_ROOT),
        "host": args.host,
        "port": args.port,
        "reload": bool(args.reload),
        "module_file": str(Path(server_mod.__file__).resolve()),
        "route_count": len(routes),
    }


def api_shell_main(argv: list[str] | None = None) -> int:
    args = _build_api_parser().parse_args(argv)
    config = _build_api_runtime_config(args)
    if args.print_config:
        print(json.dumps(config, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    import uvicorn

    uvicorn.run(
        config["app"],
        app_dir=config["app_dir"],
        host=config["host"],
        port=config["port"],
        reload=config["reload"],
    )
    return 0


def _build_mcp_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local Genesis-Core-V2 MCP stdio shell")
    parser.add_argument("--print-config", action="store_true")
    return parser


def _build_mcp_runtime_config(server_mod) -> dict[str, Any]:
    return {
        "config_env": os.environ.get("GENESIS_MCP_CONFIG_PATH", ""),
        "config_path": str(DEFAULT_MCP_CONFIG_PATH),
        "feature_flags": {
            "file_operations": server_mod.config.features.file_operations,
            "code_execution": server_mod.config.features.code_execution,
            "git_integration": server_mod.config.features.git_integration,
        },
        "log_level": server_mod.config.log_level,
        "module_file": str(Path(server_mod.__file__).resolve()),
        "server_name": server_mod.config.server_name,
        "tool_count": len(server_mod.TOOLS),
    }


def mcp_stdio_main(argv: list[str] | None = None) -> int:
    args = _build_mcp_parser().parse_args(argv)
    try:
        server_mod = _load_mcp_server_module()
    except ModuleNotFoundError as exc:
        missing_name = getattr(exc, "name", "mcp")
        raise SystemExit(
            f'genesis-v2-mcp-stdio requires the [{missing_name}] dependency; install with `python -m pip install -e ".[mcp]"`.'
        ) from exc

    config = _build_mcp_runtime_config(server_mod)
    if args.print_config:
        print(json.dumps(config, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    asyncio.run(server_mod.main())
    return 0


def _build_pytest_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local Genesis-Core-V2 pytest suite")
    parser.add_argument("--print-config", action="store_true")
    return parser


def _build_pytest_runtime_config(pytest_args: list[str] | None = None) -> dict[str, Any]:
    return {
        "cwd": str(LOCAL_REPO_ROOT),
        "src_root": str(LOCAL_SRC_ROOT),
        "pythonpath": os.environ.get("PYTHONPATH", ""),
        "pytest_args": list(pytest_args or DEFAULT_PYTEST_ARGS),
    }


def pytest_suite_main(argv: list[str] | None = None) -> int:
    _prefer_local_pythonpath()
    parsed_args, pytest_args = _build_pytest_parser().parse_known_args(argv)
    config = _build_pytest_runtime_config(pytest_args or DEFAULT_PYTEST_ARGS)
    if parsed_args.print_config:
        print(json.dumps(config, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    os.chdir(LOCAL_REPO_ROOT)

    try:
        import pytest
    except ModuleNotFoundError as exc:
        raise SystemExit(
            'genesis-v2-pytest requires pytest; install with `python -m pip install -e ".[dev]"`.'
        ) from exc

    return int(pytest.main(config["pytest_args"]))


def _run_smoke_entrypoint(module_name: str) -> int:
    _prefer_local_paths()
    return importlib.import_module(module_name).main()


def backtest_smoke_main() -> int:
    return _run_smoke_entrypoint("core.bootstrap.backtest_smoke")


def champion_smoke_main() -> int:
    return _run_smoke_entrypoint("core.bootstrap.champion_smoke")


def evaluate_champion_smoke_main() -> int:
    return _run_smoke_entrypoint("core.bootstrap.evaluate_champion_smoke")


def fixture_smoke_main() -> int:
    return _run_smoke_entrypoint("core.bootstrap.fixture_smoke")


def model_smoke_main() -> int:
    return _run_smoke_entrypoint("core.bootstrap.model_smoke")


def smoke_suite_main() -> int:
    return _run_smoke_entrypoint("core.bootstrap.smoke_suite")


__all__ = [
    "api_shell_main",
    "mcp_stdio_main",
    "pytest_suite_main",
    "champion_smoke_main",
    "evaluate_champion_smoke_main",
    "fixture_smoke_main",
    "backtest_smoke_main",
    "model_smoke_main",
    "smoke_suite_main",
]
