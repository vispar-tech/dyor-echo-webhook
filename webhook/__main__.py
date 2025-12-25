import uvicorn

from .settings import settings


def main() -> None:
    """
    Run FastAPI app via uvicorn.

    Starts the uvicorn server with configuration from settings,
    using the app factory pattern.
    """

    uvicorn.run(  # type: ignore
        "webhook.app:get_app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        factory=True,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    main()
