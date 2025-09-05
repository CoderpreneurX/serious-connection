from typing import Callable
from fastapi import FastAPI
from core.logging import get_logger

logger = get_logger(__name__)


def create_start_app_handler(app: FastAPI):
    async def start_app():
        logger.info("🚀 Application startup: Serious Connection is now running!")

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        logger.info("🛑 Application shutdown: Serious Connection has stopped.")

    return stop_app
