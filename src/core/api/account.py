from __future__ import annotations

import asyncio
import time
import uuid

from fastapi import APIRouter

from core.utils.logging_redaction import get_logger

_LOGGER = get_logger("core.server")

_ACCOUNT_CACHE = {
    "wallets": {"ts": 0.0, "data": {"items": []}},
    "positions": {"ts": 0.0, "data": {"items": []}},
    "orders": {"ts": 0.0, "data": {"items": []}},
}
_ACCOUNT_TTL = 5.0

router = APIRouter()


def _resolve_bfx_read():
    import core.server as server_mod

    read_helpers = getattr(server_mod, "bfx_read", None)
    if read_helpers is None:
        raise RuntimeError("Batch E2 account verification requires `core.server.bfx_read`.")
    return read_helpers


@router.get("/auth/check")
async def auth_check() -> dict:
    """Read-only smoke: wallets + positions (paper). Return only ok and item counts."""
    read_helpers = _resolve_bfx_read()
    wallets, positions = await asyncio.gather(
        read_helpers.get_wallets(),
        read_helpers.get_positions(),
    )
    wallet_count = len(wallets) if isinstance(wallets, list) else 0
    position_count = len(positions) if isinstance(positions, list) else 0
    return {"ok": True, "wallets": wallet_count, "positions": position_count}


@router.get("/account/wallets")
async def account_wallets() -> dict:
    now = time.time()
    if now - _ACCOUNT_CACHE["wallets"]["ts"] < _ACCOUNT_TTL:
        return _ACCOUNT_CACHE["wallets"]["data"]
    try:
        data = await _resolve_bfx_read().get_wallets()
        items = []
        if isinstance(data, list):
            for wallet in data:
                if (
                    isinstance(wallet, list)
                    and len(wallet) >= 5
                    and str(wallet[0]).lower() == "exchange"
                ):
                    items.append(
                        {
                            "type": wallet[0],
                            "currency": str(wallet[1]).upper(),
                            "balance": float(wallet[2]),
                            "available": float(wallet[4]) if wallet[4] is not None else None,
                        }
                    )
        out = {"items": items}
        _ACCOUNT_CACHE["wallets"] = {"ts": now, "data": out}
        return out
    except Exception:
        error_id = uuid.uuid4().hex[:12]
        _LOGGER.exception("/account/wallets failed (error_id=%s)", error_id)
        return {"items": [], "error": "internal_error", "error_id": error_id}


@router.get("/account/positions")
async def account_positions() -> dict:
    now = time.time()
    if now - _ACCOUNT_CACHE["positions"]["ts"] < _ACCOUNT_TTL:
        return _ACCOUNT_CACHE["positions"]["data"]
    try:
        data = await _resolve_bfx_read().get_positions()
        items = []
        if isinstance(data, list):
            for position in data:
                if isinstance(position, list) and len(position) >= 4:
                    symbol = str(position[0])
                    if not (symbol.startswith("tTEST") or ":TEST" in symbol):
                        continue
                    items.append(
                        {
                            "symbol": symbol,
                            "status": position[1],
                            "amount": float(position[2]),
                            "base_price": float(position[3]) if position[3] is not None else None,
                        }
                    )
        out = {"items": items}
        _ACCOUNT_CACHE["positions"] = {"ts": now, "data": out}
        return out
    except Exception:
        error_id = uuid.uuid4().hex[:12]
        _LOGGER.exception("/account/positions failed (error_id=%s)", error_id)
        return {"items": [], "error": "internal_error", "error_id": error_id}


@router.get("/account/orders")
async def account_orders() -> dict:
    now = time.time()
    if now - _ACCOUNT_CACHE["orders"]["ts"] < _ACCOUNT_TTL:
        return _ACCOUNT_CACHE["orders"]["data"]
    try:
        data = await _resolve_bfx_read().get_orders()
        items = []
        if isinstance(data, list):
            for order in data:
                if isinstance(order, list) and len(order) >= 8:
                    symbol = str(order[3])
                    if not (symbol.startswith("tTEST") or ":TEST" in symbol):
                        continue
                    items.append(
                        {
                            "symbol": symbol,
                            "amount": float(order[6]) if order[6] is not None else None,
                            "type": order[8] if len(order) > 8 else None,
                            "status": order[13] if len(order) > 13 else None,
                        }
                    )
        out = {"items": items}
        _ACCOUNT_CACHE["orders"] = {"ts": now, "data": out}
        return out
    except Exception:
        error_id = uuid.uuid4().hex[:12]
        _LOGGER.exception("/account/orders failed (error_id=%s)", error_id)
        return {"items": [], "error": "internal_error", "error_id": error_id}
