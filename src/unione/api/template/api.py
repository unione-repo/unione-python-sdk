"""TemplateApi: API methods of the Template section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from ...common.models import SuccessResponse
from .models import TemplateDeleteRequest, TemplateGetRequest, TemplateGetResponse, TemplateListRequest, TemplateListResponse, TemplateSetRequest, TemplateSetResponse


class TemplateApi:
    """You have the option of storing a template on the UniOne side and then using it by id, which is
    highly recommended for sending repetitive messages or high volume traffic. UniOne supports two
    different [template engines](https://docs.unione.io/en/template-engines).
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def set(self, request: TemplateSetRequest) -> TemplateSetResponse:
        """Creates or updates an email template.

        Restrictions:
        * The maximum request size is 10 MB.
        * The number of templates is limited to 10000.

        Documentation: https://docs.unione.io/en/web-api-ref#template-set

        Raises ApiError when the API returns an error.
        """
        return TemplateSetResponse.from_dict(self._client.call("/template/set.json", request.to_dict()))

    def get(self, request: TemplateGetRequest) -> TemplateGetResponse:
        """Gets template properties by it's id.

        Documentation: https://docs.unione.io/en/web-api-ref#template-get

        Raises ApiError when the API returns an error.
        """
        return TemplateGetResponse.from_dict(self._client.call("/template/get.json", request.to_dict()))

    def list(self, request: TemplateListRequest) -> TemplateListResponse:
        """Returns the list of all or some templates of the account.

        You can iterate thru large list using "offset" and "limit" parameters. When less than "limit"
        templates are returned then the end of list is reached.

        Documentation: https://docs.unione.io/en/web-api-ref#template-list

        Raises ApiError when the API returns an error.
        """
        return TemplateListResponse.from_dict(self._client.call("/template/list.json", request.to_dict()))

    def delete(self, request: TemplateDeleteRequest) -> SuccessResponse:
        """Deletes a template by id.

        Documentation: https://docs.unione.io/en/web-api-ref#template-delete

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/template/delete.json", request.to_dict()))
