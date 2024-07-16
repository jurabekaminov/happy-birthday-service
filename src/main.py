import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from src.api import system_routes, v1_router
from src.app.app_config import app_settings
from src.domain.notifications import notifications_handler

logger = logging.getLogger(__name__)

def setup_logging() -> None:
    with Path("src/logs_config.json").open("r") as f:
        config = json.load(f)
    logging.config.dictConfig(config)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    setup_logging()
    scheduler = notifications_handler.get_scheduler()
    scheduler.start()
    logger.info("Application startup complete.")
    yield
    scheduler.shutdown()
    logger.info("Application shutdown complete.")


def create_app() -> FastAPI:
    app = FastAPI(
        title=app_settings.TITLE,
        version=app_settings.VERSION,
        lifespan=lifespan
    )
    app.include_router(system_routes, prefix="/system", tags=["system"])
    app.include_router(v1_router, prefix="/api/v1")
    return app

