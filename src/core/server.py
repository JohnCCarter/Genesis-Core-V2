# ruff: noqa: I001
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.api.ui import router as ui_router, ui_page
from core.api.account import (
    _ACCOUNT_CACHE,
    _ACCOUNT_TTL,
    account_orders,
    account_positions,
    account_wallets,
    auth_check,
    router as account_router,
)
from core.api.config import router as config_router
from core.api.info import (
    TEST_SPOT_WHITELIST,
    observability_dashboard,
    paper_whitelist,
    router as info_router,
)
from core.api.models import reload_models, router as models_router
from core.api.paper import paper_estimate, paper_submit, router as paper_router
from core.api.public import (
    _CANDLES_CACHE,
    _CANDLES_TTL,
    public_candles,
    router as public_router,
)
from core.api.status import _AUTH, debug_auth, health, router as status_router
from core.api.strategy import router as strategy_router
from core.config.settings import get_settings  # noqa: F401
from core.io.bitfinex import read_helpers as bfx_read  # noqa: F401
from core.io.bitfinex.exchange_client import aclose_http_client, get_exchange_client  # noqa: F401
from core.utils.logging_redaction import get_logger

_LOGGER = get_logger("core.server")

# Minsta orderstorlek per test-ticker (kan uppdateras via probing)
MIN_ORDER_SIZE: dict[str, float] = {
    "tTESTADA:TESTUSD": 4.0,
    "tTESTALGO:TESTUSD": 8.0,
    "tTESTAPT:TESTUSD": 0.03,
    "tTESTAVAX:TESTUSD": 0.08,
    "tTESTBTC:TESTUSD": 0.001,
    "tTESTBTC:TESTUSDT": 0.001,
    "tTESTDOGE:TESTUSD": 22.0,
    "tTESTDOT:TESTUSD": 0.2,
    "tTESTEOS:TESTUSD": 2.0,
    "tTESTETH:TESTUSD": 0.001,
    "tTESTFIL:TESTUSD": 0.2,
    "tTESTLTC:TESTUSD": 0.04,
    "tTESTNEAR:TESTUSD": 0.4,
    "tTESTSOL:TESTUSD": 0.02,
    "tTESTXAUT:TESTUSD": 0.002,
    "tTESTXTZ:TESTUSD": 2.0,
}
MIN_ORDER_MARGIN: float = 0.05


def _real_from_test(sym: str) -> str:
    u = sym.upper().lstrip("T")
    if ":" in u:
        base_part, quote_part = u.split(":", 1)
    else:
        base_part, quote_part = u, "USD"
    base_part = base_part.replace("TEST", "")
    quote_part = quote_part.replace("TEST", "")
    return "t" + base_part + quote_part


def _base_ccy_from_test(sym: str) -> str:
    u = sym.upper().lstrip("T")
    base_part = u.split(":", 1)[0] if ":" in u else u
    return base_part.replace("TEST", "")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup only in the local-only V2 API shell."""
    try:
        _, h, v = _AUTH.get()
        print(f"CONFIG_VERSION={v} CONFIG_HASH={h[:12]}")
    except Exception as e:
        print(f"CONFIG_READ_FAILED: {e}")

    yield

    try:
        await aclose_http_client()
    except Exception as e:
        _LOGGER.debug("shutdown_close_http_client_error: %s", e)


app = FastAPI(lifespan=lifespan)
app.include_router(account_router)
app.include_router(config_router)
app.include_router(info_router)
app.include_router(status_router)
app.include_router(models_router)
app.include_router(public_router)
app.include_router(ui_router)
app.include_router(strategy_router)
app.include_router(paper_router)

__all__ = [
    "_ACCOUNT_CACHE",
    "_ACCOUNT_TTL",
    "_CANDLES_CACHE",
    "_CANDLES_TTL",
    "account_orders",
    "_base_ccy_from_test",
    "_LOGGER",
    "_real_from_test",
    "account_positions",
    "account_router",
    "account_wallets",
    "app",
    "aclose_http_client",
    "auth_check",
    "bfx_read",
    "debug_auth",
    "get_exchange_client",
    "health",
    "get_settings",
    "info_router",
    "models_router",
    "MIN_ORDER_MARGIN",
    "MIN_ORDER_SIZE",
    "observability_dashboard",
    "paper_whitelist",
    "paper_estimate",
    "paper_router",
    "paper_submit",
    "public_candles",
    "public_router",
    "reload_models",
    "status_router",
    "strategy_router",
    "TEST_SPOT_WHITELIST",
    "ui_page",
    "ui_router",
]
