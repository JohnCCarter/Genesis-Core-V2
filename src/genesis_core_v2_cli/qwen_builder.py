from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None

REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = REPO_ROOT / ".env"
DEFAULT_API_BASE = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL = "qwen/qwen3-coder-480b-a35b-instruct"
DEFAULT_TEMPERATURE = 0.4
DEFAULT_TOP_P = 0.8
DEFAULT_MAX_TOKENS = 4096
API_KEY_ENV = "NVIDIA_API_KEY"


def _first_present_env(*keys: str) -> tuple[str, str] | tuple[None, None]:
    for key in keys:
        value = os.environ.get(key)
        if value and str(value).strip():
            return str(value), key
    return None, None


def _load_local_env() -> None:
    if load_dotenv is None:
        return
    try:
        load_dotenv(dotenv_path=ENV_FILE, override=True)
    except Exception:
        return


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Query the NVIDIA-hosted Qwen builder helper through the OpenAI-compatible API"
        )
    )
    prompt_group = parser.add_mutually_exclusive_group()
    prompt_group.add_argument("--prompt")
    prompt_group.add_argument("--prompt-file", type=Path)
    parser.add_argument("--system")
    default_base, _ = _first_present_env("NVIDIA_API_BASE", "LLM_API_BASE", "OPENAI_API_BASE")
    default_model, _ = _first_present_env("NVIDIA_QWEN_MODEL", "LLM_MODEL", "NVIDIA_GLM_MODEL")
    parser.add_argument("--base-url", default=default_base or DEFAULT_API_BASE)
    parser.add_argument("--model", default=default_model or DEFAULT_MODEL)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--top-p", type=float, default=DEFAULT_TOP_P)
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--print-config", action="store_true")
    return parser


def build_runtime_config(
    *,
    base_url: str,
    model: str,
    temperature: float,
    top_p: float,
    max_tokens: int,
    stream: bool,
    system_prompt: str | None,
) -> dict[str, Any]:
    api_key, api_key_env = _first_present_env(
        API_KEY_ENV, "LLM_API_KEY", "OPENAI_API_KEY", "GLM_API_KEY"
    )
    normalized_api_key = api_key or ""
    return {
        "api_base": base_url,
        "api_key_env": api_key_env or API_KEY_ENV,
        "env_file": str(ENV_FILE),
        "has_api_key": bool(normalized_api_key and normalized_api_key != "change-me"),
        "max_tokens": int(max_tokens),
        "model": model,
        "repo_root": str(REPO_ROOT),
        "stream": bool(stream),
        "system_prompt_enabled": bool(system_prompt and system_prompt.strip()),
        "temperature": float(temperature),
        "top_p": float(top_p),
    }


def _resolve_prompt(args: argparse.Namespace) -> str:
    prompt = ""
    if args.prompt is not None:
        prompt = str(args.prompt)
    elif args.prompt_file is not None:
        prompt = args.prompt_file.read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        prompt = sys.stdin.read()
    else:
        raise SystemExit("Provide --prompt, --prompt-file, or pipe prompt text on stdin.")

    if not prompt.strip():
        raise SystemExit("Prompt must not be empty.")
    return prompt


def _build_messages(prompt: str, system_prompt: str | None) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = [{"role": "user", "content": prompt}]
    if system_prompt and system_prompt.strip():
        messages.insert(0, {"role": "system", "content": system_prompt})
    return messages


def _serialize_usage(usage: Any) -> dict[str, Any] | None:
    if usage is None:
        return None
    if hasattr(usage, "model_dump"):
        return usage.model_dump()
    if hasattr(usage, "dict"):
        return usage.dict()
    return None


def _build_response_payload(completion: Any, *, requested_model: str) -> dict[str, Any]:
    choice = completion.choices[0]
    message = choice.message
    payload: dict[str, Any] = {
        "content": getattr(message, "content", "") or "",
        "finish_reason": getattr(choice, "finish_reason", None),
        "model": getattr(completion, "model", requested_model) or requested_model,
        "role": getattr(message, "role", "assistant"),
    }
    usage_payload = _serialize_usage(getattr(completion, "usage", None))
    if usage_payload is not None:
        payload["usage"] = usage_payload
    return payload


def _write_cold_start_note(*, stream: bool) -> None:
    if stream:
        print(
            "Note: streaming is enabled; first-token latency depends on the selected provider/model.",
            file=sys.stderr,
        )
        return
    print(
        "Note: non-stream mode waits for the full response; use --stream for earlier feedback.",
        file=sys.stderr,
    )


def _stream_completion(
    client: Any,
    *,
    config: dict[str, Any],
    messages: list[dict[str, str]],
) -> None:
    stream = client.chat.completions.create(
        model=config["model"],
        messages=messages,
        temperature=config["temperature"],
        top_p=config["top_p"],
        max_tokens=config["max_tokens"],
        stream=True,
    )
    wrote_output = False
    try:
        for chunk in stream:
            choices = getattr(chunk, "choices", None) or []
            if not choices:
                continue
            delta = getattr(choices[0], "delta", None)
            content = getattr(delta, "content", None) if delta is not None else None
            if isinstance(content, str) and content:
                sys.stdout.write(content)
                sys.stdout.flush()
                wrote_output = True
    finally:
        close = getattr(stream, "close", None)
        if callable(close):
            close()
    if wrote_output:
        sys.stdout.write("\n")
        sys.stdout.flush()


def _raise_user_facing_request_error(exc: Exception, *, api_key_env: str) -> None:
    status_code = getattr(exc, "status_code", None)
    if status_code == 401:
        raise SystemExit(
            f"Provider returned HTTP 401. Update {api_key_env} in {ENV_FILE.name} or the shell and retry."
        ) from exc
    if status_code == 403:
        raise SystemExit(
            f"Provider returned HTTP 403 Authorization failed. The saved or inherited {api_key_env} is not authorized for this model. Save the correct key in {ENV_FILE.name} and retry."
        ) from exc
    raise exc


def main(argv: list[str] | None = None) -> int:
    _load_local_env()
    args = build_parser().parse_args(argv)
    config = build_runtime_config(
        base_url=str(args.base_url),
        model=str(args.model),
        temperature=float(args.temperature),
        top_p=float(args.top_p),
        max_tokens=int(args.max_tokens),
        stream=bool(args.stream),
        system_prompt=args.system,
    )
    if args.print_config:
        print(json.dumps(config, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    api_key, api_key_env = _first_present_env(
        API_KEY_ENV, "LLM_API_KEY", "OPENAI_API_KEY", "GLM_API_KEY"
    )
    normalized_api_key = api_key or ""
    normalized_api_key_env = api_key_env or API_KEY_ENV
    if not normalized_api_key or normalized_api_key == "change-me":
        raise SystemExit(
            f"Set {normalized_api_key_env} (or LLM_API_KEY) in {ENV_FILE.name} or the shell before calling this builder helper."
        )

    prompt = _resolve_prompt(args)
    try:
        from openai import APIStatusError, APITimeoutError, OpenAI
    except ModuleNotFoundError as exc:
        raise SystemExit(
            'genesis-v2-qwen-builder requires the `openai` package; install with `python -m pip install -e "."`.'
        ) from exc

    client = OpenAI(base_url=config["api_base"], api_key=normalized_api_key)
    messages = _build_messages(prompt, args.system)
    _write_cold_start_note(stream=bool(args.stream))
    try:
        if args.stream:
            _stream_completion(client, config=config, messages=messages)
            return 0

        completion = client.chat.completions.create(
            model=config["model"],
            messages=messages,
            temperature=config["temperature"],
            top_p=config["top_p"],
            max_tokens=config["max_tokens"],
            stream=False,
        )
    except APITimeoutError as exc:
        raise SystemExit(
            "The provider request timed out. Retry with --stream for earlier feedback and verify base URL/model settings."
        ) from exc
    except APIStatusError as exc:
        _raise_user_facing_request_error(exc, api_key_env=normalized_api_key_env)

    print(
        json.dumps(
            _build_response_payload(completion, requested_model=config["model"]),
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
