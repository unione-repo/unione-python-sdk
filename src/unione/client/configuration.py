"""API connection settings."""
from dataclasses import dataclass, field
from typing import Dict, Optional

DEFAULT_BASE_URL = "https://api.unione.io/en/transactional/api/v1"
HOST_API = "api.unione.io"
HOST_EU1 = "eu1.unione.io"
HOST_US1 = "us1.unione.io"

BASE_PATH = "/en/transactional/api/v1"
"""Path of the API on every host."""


def base_url_for(host: str) -> str:
    """Base URL for an API host: "eu1.unione.io" -> "https://eu1.unione.io" + BASE_PATH; a full URL is kept as is."""
    if "://" in host:
        return host.rstrip("/")
    return "https://" + host.strip("/") + BASE_PATH


@dataclass
class Configuration:
    """API key, base URL of the API and HTTP settings."""

    api_key: str
    """User or project API key, sent in the X-API-KEY header."""

    base_url: str = DEFAULT_BASE_URL
    """Base URL of the API."""

    timeout: float = 30.0
    """Request timeout in seconds."""

    user_agent: str = "unione-python-sdk/1.2.3"

    platform: Optional[str] = None
    """Package that uses the SDK and its version, e.g. "django.1.0.0": goes to the "platform" query parameter before the SDK one
    (api_client.PLATFORM): "django.1.0.0,python-sdk.1.0.0"."""

    headers: Dict[str, str] = field(default_factory=dict)
    """Extra HTTP headers of every request (e.g. a tracing id); they override the default ones of the same name."""
