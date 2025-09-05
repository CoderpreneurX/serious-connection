from fastapi import FastAPI
from core.events import create_start_app_handler, create_stop_app_handler
from core.router import api_router
from core.config import settings
from core.exceptions import register_exception_handlers


def get_application() -> FastAPI:
    app = FastAPI(title="Serious Connection", debug=settings.DEBUG, version="0.1.0")

    # Lifespan events
    app.add_event_handler("startup", create_start_app_handler(app))
    app.add_event_handler("shutdown", create_stop_app_handler(app))

    # Exceptions
    register_exception_handlers(app=app)

    # Routers
    app.include_router(api_router)

    return app


app = get_application()
