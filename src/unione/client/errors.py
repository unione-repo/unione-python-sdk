"""Error raised when the API returns an error, the request fails or is invalid, or the response can not be
processed. The message names the API method and, for an API error, the code, the HTTP status and how to fix it:
"email/send: Unknown recipient (API error 204, HTTP 400). Fix: ... See ...#api-errors".
"""
from typing import Any, Dict, Optional


class ApiError(Exception):
    """API error: message, HTTP status, API error code, the decoded error response, the API method, how to fix it,
    what failed (kind) and whether a repeat may succeed (retryable)."""

    KIND_API = "api"
    """The API returned an error (error_code, hint)."""
    KIND_NETWORK = "network"
    """The request could not be sent or the response could not be received."""
    KIND_TIMEOUT = "timeout"
    """The request timed out."""
    KIND_INVALID_RESPONSE = "invalid_response"
    """The response is not the JSON of the API (a proxy page, a broken body)."""
    KIND_INVALID_REQUEST = "invalid_request"
    """Found before sending (an empty API key, a required field missing): no request was sent."""

    def __init__(
        self,
        message: str,
        http_status: int = 0,
        error_code: Optional[int] = None,
        response_body: Optional[Dict[str, Any]] = None,
        *,
        method: str = "",
        hint: Optional[str] = None,
        kind: str = KIND_API,
        api_message: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.http_status = http_status
        self.error_code = error_code
        self.response_body = response_body
        self.method = method
        """API method of the request, e.g. "email/send"; empty when unknown."""
        self.hint = hint
        """How to fix the API error (the errors table of the docs), None when unknown."""
        self.kind = kind
        """What failed: one of the KIND_* constants."""
        self.api_message = api_message
        """The API's own error message (the "message" of the error response) as is, None when there was no API
        response; the exception message is the decorated one."""

    @property
    def retryable(self) -> bool:
        """A repeat of the request may succeed: a network error, a timeout, HTTP 429 or 5xx."""
        if self.kind in (self.KIND_NETWORK, self.KIND_TIMEOUT):
            return True
        if self.kind in (self.KIND_API, self.KIND_INVALID_RESPONSE):
            return self.http_status == 429 or self.http_status >= 500
        return False
