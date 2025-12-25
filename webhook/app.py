from fastapi import FastAPI

from webhook.logging import setup_logging

from .router import router


def get_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance with logging setup and router included.
    """
    setup_logging()
    app = FastAPI(title="Dyor Echo Webhook - FastAPI", docs_url=None, redoc_url=None)
    app.include_router(router)
    return app
