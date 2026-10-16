"""TagApi: API methods of the Tag section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from ...common.models import SuccessResponse
from .models import TagDeleteRequest, TagListResponse


class TagApi:
    """This family of methods is used to manage user-defined tags. Tags are used to categorize letters
    based on your own criteria, e. g. to create a distinction between marketing and transactional
    letters or group together all notifications for a particular order type. UniOne allows you to assign
    tags to all outgoing emails, and the tags you’ve set may then be used to filter and analyze delivery
    statistics.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def list(self) -> TagListResponse:
        """This method returns the full list of user-defined tags. Does not receive any parameters.

        Documentation: https://docs.unione.io/en/web-api-ref#tag-list

        Raises ApiError when the API returns an error.
        """
        return TagListResponse.from_dict(self._client.call("/tag/list.json"))

    def delete(self, request: TagDeleteRequest) -> SuccessResponse:
        """Removes tag.

        Documentation: https://docs.unione.io/en/web-api-ref#tag-delete

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/tag/delete.json", request.to_dict()))
