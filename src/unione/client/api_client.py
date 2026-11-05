"""Low level client: every API method is a POST request with a JSON body that returns JSON.

The HTTP layer is pluggable: ApiClient(config, transport=...) takes any object with the method
``send(method, url, headers, body, timeout) -> (status, body)`` (or a plain function with these arguments),
see Transport. The default one, UrllibTransport, uses the standard library.
"""
import http.client
import json
import socket
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable, Dict, Mapping, Optional, Tuple, Union

from .configuration import Configuration
from . import _errors
from .errors import ApiError

PLATFORM = "python-sdk.1.3.1"
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
            if _is_timeout(e):
                raise ApiError(f"HTTP request timed out after {timeout:g} s", kind=ApiError.KIND_TIMEOUT) from e
            raise ApiError(f"HTTP request failed: {e}", kind=ApiError.KIND_NETWORK) from e


def _is_timeout(error: BaseException) -> bool:
    """socket.timeout (TimeoutError since Python 3.10), also inside the URLError of urllib, or an exception whose class
    name contains "Timeout" (requests.Timeout, httpx.TimeoutException, ...), also as the cause of the error."""
    for e in (error, getattr(error, "reason", None), error.__cause__):
        if isinstance(e, (socket.timeout, TimeoutError)):
            return True
        if isinstance(e, BaseException) and any("Timeout" in c.__name__ for c in type(e).__mro__):
            return True
    return False


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
        method = _errors.method_of(path)
        if not self.config.api_key:
            raise _invalid_request(method, "the API key is empty: pass the API key of the user or of the project to "
                                           "the client")
        try:
            text = json.dumps(body or {}, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            raise _invalid_request(method, f"can not encode the request: {e}") from e
        found = _errors.missing(method, json.loads(text))
        if found is not None:
            raise _invalid_request(method, f"{found} is required")
        data = text.encode("utf-8")
        url = self.config.base_url.rstrip("/") + "/" + path.lstrip("/") + "?" + urllib.parse.urlencode(
            {"platform": f"{self.config.platform},{PLATFORM}" if self.config.platform else PLATFORM})
        send = getattr(self.transport, "send", None)
        if not callable(send):
            send = self.transport
        try:
            status, raw = send("POST", url, self.headers(), data, self.config.timeout)
        except ApiError as e:
            # an error of the transport: it keeps its data and gets the method; a plain ApiError (kind api, no code,
            # no HTTP status) of a custom transport is a network one
            if e.method:
                raise
            kind = e.kind
            if kind == ApiError.KIND_API and e.error_code is None and not e.http_status:
                kind = ApiError.KIND_NETWORK
            message = e.message if e.message.startswith(method + ": ") else f"{method}: {e.message}"
            raise ApiError(message, e.http_status, e.error_code, e.response_body, method=method, hint=e.hint,
                           kind=kind, api_message=e.api_message) from e
        except Exception as e:  # noqa: BLE001 - any failure of the HTTP layer is an ApiError
            if _is_timeout(e):
                raise ApiError(f"{method}: HTTP request timed out: {e}", method=method,
                               kind=ApiError.KIND_TIMEOUT) from e
            raise ApiError(f"{method}: HTTP request failed: {e}", method=method, kind=ApiError.KIND_NETWORK) from e
        status = int(status)
        if isinstance(raw, str):
            raw = raw.encode("utf-8")
        raw = raw or b""

        try:
            payload = json.loads(raw.decode("utf-8"))
        except ValueError as e:
            raise ApiError(f"{method}: invalid JSON in response (HTTP {status}): {_snippet(raw)}", status,
                           method=method, kind=ApiError.KIND_INVALID_RESPONSE) from e
        if not isinstance(payload, dict):
            raise ApiError(f"{method}: unexpected response (HTTP {status}): {_snippet(raw)}", status,
                           method=method, kind=ApiError.KIND_INVALID_RESPONSE)

        if status >= 400 or payload.get("status") == "error":
            code = _errors.code_of(payload.get("code"))
            text = payload.get("message")
            raise ApiError(
                _errors.api_message(method, str(payload.get("message") or ""), status, code),
                status,
                code,
                payload,
                method=method,
                hint=_errors.hint(code),
                kind=ApiError.KIND_API,
                api_message=None if text is None else str(text),
            )
        return payload


def _snippet(raw: bytes) -> str:
    """The start of a response body for an error message."""
    return _errors.quote(raw.decode("utf-8", "replace"))


def _invalid_request(method: str, message: str) -> ApiError:
    return ApiError(f"{method}: {message}", method=method, kind=ApiError.KIND_INVALID_REQUEST)
