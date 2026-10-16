"""SystemApi: API methods of the System section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from .models import SystemInfoResponse, SystemPingResponse


class SystemApi:
    """System operations."""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def ping(self) -> SystemPingResponse:
        """Checks API key validity and returns user ID.

        Documentation: https://docs.unione.io/en/web-api-ref#system-ping

        Raises ApiError when the API returns an error.
        """
        return SystemPingResponse.from_dict(self._client.call("/system/ping.json"))

    def info(self) -> SystemInfoResponse:
        """Gets user or project info by API key.

        Documentation: https://docs.unione.io/en/web-api-ref#system-info

        Raises ApiError when the API returns an error.
        """
        return SystemInfoResponse.from_dict(self._client.call("/system/info.json"))
