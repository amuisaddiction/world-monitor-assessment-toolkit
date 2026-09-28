import httpx
import logging
import re
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_safe_request(url: str, method: str = "GET", timeout: int = 5) -> Optional[httpx.Response]:
    try:
        with httpx.Client(verify=False, timeout=timeout) as client:
            return client.request(method, url)
    except httpx.RequestError as exc:
        logger.error(f"Error requesting {exc.request.url!r}: {exc}")
        return None

def redact_secrets(data: str) -> str:
    redacted = re.sub(r"(Bearer\s+)[A-Za-z0-9\-\._~]+", r"\1[REDACTED]", data)
    return redacted
