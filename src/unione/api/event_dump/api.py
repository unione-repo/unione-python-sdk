"""EventDumpApi: API methods of the EventDump section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from ...common.models import SuccessResponse
from .models import EventDumpCreateRequest, EventDumpCreateResponse, EventDumpDeleteRequest, EventDumpGetRequest, EventDumpGetResponse, EventDumpListResponse


class EventDumpApi:
    """These methods are used to obtain a list of events for a given period of time. The data is stored for
    up to 45 days, depending on your tariff, i. e. you may fetch all event data starting from 00:00:00
    31 days ago and up to current time. For custom tarifs with big sending volumes event dumps are
    available only for the last 7 days.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def create(self, request: EventDumpCreateRequest) -> EventDumpCreateResponse:
        """This asynchronous method initiates the preparation of data dump in CSV format. The number of dump
        files created or stored is limited to 10; to order more files, you have to delete one of the
        previous ones or wait until they will be deleted automatically. A newly created dump file is kept
        for 8 hours. If the request period is more than a day or there are too many events then several
        files will be generated and each file will contain no more than 100,000 events. File contains
        columns with the following information - 'event_time', 'job_id', 'from_email', 'email', 'status',
        'delivery_status', 'metadata', 'destination_response', 'user_agent', 'url', 'ip', 'tags' and
        'project_id' (for accounts with projects enabled). You can change the fields and include 'subject'
        field using 'dump_fileds' parameter.

        Documentation: https://docs.unione.io/en/web-api-ref#event-dump-create

        Raises ApiError when the API returns an error.
        """
        return EventDumpCreateResponse.from_dict(self._client.call("/event-dump/create.json", request.to_dict()))

    def get(self, request: EventDumpGetRequest) -> EventDumpGetResponse:
        """Returns dump properties for a given identifier

        Documentation: https://docs.unione.io/en/web-api-ref#event-dump-get

        Raises ApiError when the API returns an error.
        """
        return EventDumpGetResponse.from_dict(self._client.call("/event-dump/get.json", request.to_dict()))

    def list(self) -> EventDumpListResponse:
        """This method does not require any parameters; returns the full list of existing dumps.

        Documentation: https://docs.unione.io/en/web-api-ref#event-dump-list

        Raises ApiError when the API returns an error.
        """
        return EventDumpListResponse.from_dict(self._client.call("/event-dump/list.json"))

    def delete(self, request: EventDumpDeleteRequest) -> SuccessResponse:
        """Removes dump from queue or storage.

        Documentation: https://docs.unione.io/en/web-api-ref#event-dump-delete

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/event-dump/delete.json", request.to_dict()))
