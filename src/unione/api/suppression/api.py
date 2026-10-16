"""SuppressionApi: API methods of the Suppression section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from ...common.models import SuccessResponse
from .models import SuppressionDeleteRequest, SuppressionGetRequest, SuppressionGetResponse, SuppressionListRequest, SuppressionListResponse, SuppressionSetRequest


class SuppressionApi:
    """Methods for managing suppression lists. An email can be added to suppression list because of
    unsubscription, bounce or complain.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def set(self, request: SuppressionSetRequest) -> SuccessResponse:
        """Adds an email address to the suppression list. You can always remove this address from the
        suppression list later using the
        [suppression/delete](https://docs.unione.io/en/web-api-ref#suppression-delete) method.

        Documentation: https://docs.unione.io/en/web-api-ref#suppression-set

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/suppression/set.json", request.to_dict()))

    def get(self, request: SuppressionGetRequest) -> SuppressionGetResponse:
        """Gets a reason and date of email suppression.

        Documentation: https://docs.unione.io/en/web-api-ref#suppression-get

        Raises ApiError when the API returns an error.
        """
        return SuppressionGetResponse.from_dict(self._client.call("/suppression/get.json", request.to_dict()))

    def list(self, request: SuppressionListRequest) -> SuppressionListResponse:
        """Returns a suppression list since provided date.

        Documentation: https://docs.unione.io/en/web-api-ref#suppression-list

        Raises ApiError when the API returns an error.
        """
        return SuppressionListResponse.from_dict(self._client.call("/suppression/list.json", request.to_dict()))

    def delete(self, request: SuppressionDeleteRequest) -> SuccessResponse:
        """Deletes an email from suppression list (only records with is_deletable=true). If there are no
        entries of this email in the suppression list, API error 3003 is returned. If such entries exist but
        no one can be deleted, API error 3004 is returned. If daily limit of deletes exceeded, API error 906
        is returned.

        Documentation: https://docs.unione.io/en/web-api-ref#suppression-delete

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/suppression/delete.json", request.to_dict()))
