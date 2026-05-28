from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.api.config import router as config_router
from core.api.models import reload_models, router as models_router
from core.api.status import _AUTH, debug_auth, health, router as status_router
from core.api.strategy import router as strategy_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup only in the local-only V2 API shell."""
    try:
        _, h, v = _AUTH.get()
        print(f"CONFIG_VERSION={v} CONFIG_HASH={h[:12]}")
    except Exception as e:
        print(f"CONFIG_READ_FAILED: {e}")

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(config_router)
app.include_router(status_router)
app.include_router(models_router)
app.include_router(strategy_router)

__all__ = [
    "app",
    "debug_auth",
    "health",
    "models_router",
    "reload_models",
    "status_router",
    "strategy_router",
]
