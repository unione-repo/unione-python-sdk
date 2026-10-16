"""WebhookApi: API methods of the Webhook section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from ...common.models import SuccessResponse
from .models import WebhookCallback, WebhookDeleteRequest, WebhookGetRequest, WebhookGetResponse, WebhookListRequest, WebhookListResponse, WebhookSetRequest, WebhookSetResponse


class WebhookApi:
    """UniOne lets you recieve notifications about email status changes or spam blocks. You provide an URL
    and every time a watched event occurs we will notify you by submitting a request with JSON data to
    this URL.

    You can configure the format of webhook calls (JSON or gzipped JSON), which events you want to be
    notified of, whether or not you let us groups several events in one request, do you want to receive
    extra details like SMTP answer or recipient's user agent, etc.

    Please note that your webhook handler should be able to process at least 5 parallel requests, up to
    100 events each (but you can configure the maximum number of parallel connections up to 100, which
    is recommended).

    If the URL of your webhook handler is not available (the response is not HTTP 200 OK within 3
    seconds timeout), the system will repeat requests each 10 minutes during 24 hours, passing extra
    parameter retry_count. If there were at least 10 events during last 24 hours and all the webhook
    requests about these events have failed then we consider webhook handler broken and change it's
    status to inactive automatically. A notification about that is sent to an email [configured in
    control panel](https://cp.unione.io/en/user/alerting/technical/).

    The format of webhook request and details of each event are described
    [here](https://docs.unione.io/en/web-api-ref#callback-format).
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def set(self, request: WebhookSetRequest) -> WebhookSetResponse:
        """Sets or edits a [webhook](https://docs.unione.io/en/web-api-ref#webhook), i.e. an event notification
        handler.

        Documentation: https://docs.unione.io/en/web-api-ref#webhook-set

        Raises ApiError when the API returns an error.
        """
        return WebhookSetResponse.from_dict(self._client.call("/webhook/set.json", request.to_dict()))

    def get(self, request: WebhookGetRequest) -> WebhookGetResponse:
        """Gets properties of a [webhook](https://docs.unione.io/en/web-api-ref#webhook).

        Documentation: https://docs.unione.io/en/web-api-ref#webhook-get

        Raises ApiError when the API returns an error.
        """
        return WebhookGetResponse.from_dict(self._client.call("/webhook/get.json", request.to_dict()))

    def list(self, request: WebhookListRequest) -> WebhookListResponse:
        """List all or some [webhooks](https://docs.unione.io/en/web-api-ref#webhook) (event notification
        handlers) of a user or a project.

        Documentation: https://docs.unione.io/en/web-api-ref#webhook-list

        Raises ApiError when the API returns an error.
        """
        return WebhookListResponse.from_dict(self._client.call("/webhook/list.json", request.to_dict()))

    def delete(self, request: WebhookDeleteRequest) -> SuccessResponse:
        """Deletes an event notification handler

        You can also temporarily deactivate webhook without deleting it by setting it's status to "disabled"
        in [webhook/set](https://docs.unione.io/en/web-api-ref#webhook-set) method.

        Documentation: https://docs.unione.io/en/web-api-ref#webhook-delete

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/webhook/delete.json", request.to_dict()))

    @staticmethod
    def parse_callback(body: str) -> WebhookCallback:
        """Webhook callback format description."""
        return WebhookCallback.from_dict(json.loads(body))
