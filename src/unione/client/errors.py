"""Error raised when the API returns an error or the response can not be processed."""
from typing import Any, Dict, Optional


class ApiError(Exception):
    """API error: message, HTTP status, API error code and the decoded error response."""

    def __init__(
        self,
        message: str,
        http_status: int = 0,
        error_code: Optional[int] = None,
        response_body: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.http_status = http_status
        self.error_code = error_code
        self.response_body = response_body
