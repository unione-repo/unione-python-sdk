"""ProjectApi: API methods of the Project section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from ...common.models import SuccessResponse
from .models import ProjectCreateRequest, ProjectCreateResponse, ProjectDeleteRequest, ProjectListRequest, ProjectListResponse, ProjectUpdateRequest, ProjectUpdateResponse


class ProjectApi:
    """Projects allow you to group several independent domains, webhooks, templates, and unsubscription
    lists together. It's very useful if you have your own clients and manage their data from a single
    UniOne account. Each project receives its own API key, and all API calls with that API key only deal
    with the data of that project. This way, you can assign a separate project for each client and be
    sure that they won't conflict; e.g. unsubscribing from one project won't affect another.

    Projects methods are disabled by default due to antispam measures. To enable them, [contact
    support](https://cp.unione.io/en/support).

    Please note that sending domains are confirmed and used on per-project basis by default. But it's
    possible to allow projects to send emails from domains confirmed for main account - just [ask
    support](https://cp.unione.io/en/support) to enable it.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def create(self, request: ProjectCreateRequest) -> ProjectCreateResponse:
        """Creates a new project.

        Documentation: https://docs.unione.io/en/web-api-ref#project-create

        Raises ApiError when the API returns an error.
        """
        return ProjectCreateResponse.from_dict(self._client.call("/project/create.json", request.to_dict()))

    def update(self, request: ProjectUpdateRequest) -> ProjectUpdateResponse:
        """Updates a project.

        Documentation: https://docs.unione.io/en/web-api-ref#project-update

        Raises ApiError when the API returns an error.
        """
        return ProjectUpdateResponse.from_dict(self._client.call("/project/update.json", request.to_dict()))

    def list(self, request: ProjectListRequest) -> ProjectListResponse:
        """Lists projects.

        Documentation: https://docs.unione.io/en/web-api-ref#project-list

        Raises ApiError when the API returns an error.
        """
        return ProjectListResponse.from_dict(self._client.call("/project/list.json", request.to_dict()))

    def delete(self, request: ProjectDeleteRequest) -> SuccessResponse:
        """Deletes a project.

        The project will be moved to the "trash bin" before being permanently deleted. You can restore the
        project by contacting support.

        Documentation: https://docs.unione.io/en/web-api-ref#project-delete

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/project/delete.json", request.to_dict()))
