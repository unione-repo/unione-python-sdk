"""ConfirmedEmailApi: API methods of the ConfirmedEmail section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from .models import ConfirmedEmailCreateResponse, ConfirmedEmailDeleteResponse, ConfirmedEmailListResponse, ConfirmedEmailRequest


class ConfirmedEmailApi:
    """Manage email addresses confirmed for sandbox-domain sending. These methods are available only with a
    main account API key.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def create(self, request: ConfirmedEmailRequest) -> ConfirmedEmailCreateResponse:
        """Adds an email address and sends a confirmation link.

        Documentation: https://docs.unione.io/en/web-api-ref#confirmed-email-create

        Raises ApiError when the API returns an error.
        """
        return ConfirmedEmailCreateResponse.from_dict(self._client.call("/confirmed-email/create.json", request.to_dict()))

    def list(self) -> ConfirmedEmailListResponse:
        """Lists confirmed and unconfirmed email addresses for the account.

        Documentation: https://docs.unione.io/en/web-api-ref#confirmed-email-list

        Raises ApiError when the API returns an error.
        """
        return ConfirmedEmailListResponse.from_dict(self._client.call("/confirmed-email/list.json"))

    def delete(self, request: ConfirmedEmailRequest) -> ConfirmedEmailDeleteResponse:
        """Deletes an email address from the account's confirmed email list.

        Documentation: https://docs.unione.io/en/web-api-ref#confirmed-email-delete

        Raises ApiError when the API returns an error.
        """
        return ConfirmedEmailDeleteResponse.from_dict(self._client.call("/confirmed-email/delete.json", request.to_dict()))
