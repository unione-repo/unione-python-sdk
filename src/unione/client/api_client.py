"""Low level client: every API method is a POST request with a JSON body that returns JSON.

The HTTP layer is pluggable: ApiClient(config, transport=...) takes any object with the method
``send(method, url, headers, body, timeout) -> (status, body)`` (or a plain function with these arguments),
see Transport. The default one, UrllibTransport, uses the standard library.
"""
import http.client
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable, Dict, Mapping, Optional, Tuple, Union

from .configuration import Configuration
from .errors import ApiError

PLATFORM = "python-sdk.1.1.2"
"""The SDK and its version in the "platform" query parameter of every request."""


class Transport:
    """Interface of the HTTP layer of ApiClient (subclassing is optional, any object with ``send`` works)."""

    def send(self, method: str, url: str, headers: Mapping[str, str], body: bytes,
             timeout: float) -> Tuple[int, bytes]:
        """Send an HTTP request and return (HTTP status, raw response body).

        method: "POST"; url: full URL with the query string; headers: all request headers (API key included);
        body: JSON encoded as UTF-8; timeout: seconds. HTTP error statuses (4xx, 5xx) are returned, not raised:
        ApiClient turns them into ApiError. A network failure may raise any exception: ApiClient wraps it in ApiError.
        """
        raise NotImplementedError


TransportLike = Union[Transport, Callable[[str, str, Mapping[str, str], bytes, float], Tuple[int, bytes]]]
"""A Transport or a function with the arguments of Transport.send."""


class UrllibTransport(Transport):
    """Default transport: urllib.request of the standard library."""

    def send(self, method: str, url: str, headers: Mapping[str, str], body: bytes,
             timeout: float) -> Tuple[int, bytes]:
        request = urllib.request.Request(url, data=body, method=method, headers=dict(headers))
        try:
            try:
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    return response.status, response.read()
            except urllib.error.HTTPError as e:
                return e.code, e.read()
        except (urllib.error.URLError, http.client.HTTPException, OSError, ValueError) as e:
            raise ApiError(f"HTTP request failed: {e}") from e


class ApiClient:
    """Sends API requests through the transport (UrllibTransport by default)."""

    def __init__(self, config: Configuration, transport: Optional[TransportLike] = None) -> None:
        self.config = config
        self.transport: TransportLike = transport if transport is not None else UrllibTransport()

    def headers(self) -> Dict[str, str]:
        """Headers of every request: JSON, User-Agent, the API key, then Configuration.headers."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.config.user_agent,
            "X-API-KEY": self.config.api_key,
        }
        headers.update(self.config.headers or {})
        return headers

    def call(self, path: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Call an API method, e.g. ``call("/email/send.json", {...})``, and return the decoded response."""
        url = self.config.base_url.rstrip("/") + "/" + path.lstrip("/") + "?" + urllib.parse.urlencode(
            {"platform": f"{self.config.platform},{PLATFORM}" if self.config.platform else PLATFORM})
        data = json.dumps(body or {}, ensure_ascii=False).encode("utf-8")
        send = getattr(self.transport, "send", None)
        if not callable(send):
            send = self.transport
        try:
            status, raw = send("POST", url, self.headers(), data, self.config.timeout)
        except ApiError:
            raise
        except Exception as e:  # noqa: BLE001 - any failure of the HTTP layer is an ApiError
            raise ApiError(f"HTTP request failed: {e}") from e
        status = int(status)
        if isinstance(raw, str):
            raw = raw.encode("utf-8")
        raw = raw or b""

        try:
            payload = json.loads(raw.decode("utf-8"))
        except ValueError as e:
            raise ApiError(f"Invalid JSON in response (HTTP {status}): {raw[:500]!r}", status) from e
        if not isinstance(payload, dict):
            raise ApiError(f"Unexpected response (HTTP {status}): {raw[:500]!r}", status)

        if status >= 400 or payload.get("status") == "error":
            code = payload.get("code")
            raise ApiError(
                str(payload.get("message") or "API error"),
                status,
                int(code) if isinstance(code, (int, str)) and str(code).isdigit() else None,
                payload,
            )
        return payload
