import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Request


logger = logging.getLogger(__name__)
router = APIRouter()


async def _parse_request_body(request: Request) -> dict[str, Any]:
    """
    Parse and validate JSON payload from request.

    Args:
        request: The incoming FastAPI request object.

    Returns:
        A dictionary containing the parsed JSON payload.

    Raises:
        HTTPException: If the request body is not valid JSON (status code 400).
    """
    raw_body = await request.body()
    raw_text = raw_body.decode("utf-8")

    logger.info(f"Received webhook request - Raw body: {raw_text}")

    try:
        return await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")


async def _process_webhook(payload: dict[str, Any]) -> dict[str, str]:
    """
    Process webhook payload and return result.

    Args:
        payload: The webhook payload as a dictionary.

    Returns:
        A dictionary containing the processing result with status information.

    Raises:
        HTTPException: If webhook processing fails (status code 500).
    """
    try:
        logger.info(f"Received webhook payload: {payload}")
        result = {"status": "logged"}
        logger.info(f"Webhook processed successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"Webhook processing failed: {e}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")


@router.post("/echo/webhook")
@router.get("/echo/webhook")
async def webhook_endpoint(request: Request) -> dict[str, str | dict[str, str]]:
    """
    Entry point for webhook events.

    Accepts any JSON payload and delegates to business logic handler.
    Supports both GET and POST methods.

    Args:
        request: The incoming FastAPI request object.

    Returns:
        A dictionary containing the status and processing result.

    Raises:
        HTTPException: If request parsing or processing fails.
    """
    payload = await _parse_request_body(request)
    result = await _process_webhook(payload)
    return {"status": "ok", "result": result}
