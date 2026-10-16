"""ObsoleteApi: API methods of the Obsolete section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from .models import ObsoleteUnsubscribedCheckRequest, ObsoleteUnsubscribedCheckResponse, ObsoleteUnsubscribedListRequest, ObsoleteUnsubscribedListResponse, ObsoleteUnsubscribedSetRequest, ObsoleteUnsubscribedSetResponse


class ObsoleteApi:
    """Obsolete methods dealing with unsubscribes. We recommend using the more flexible
    [suppression](https://docs.unione.io/en/web-api-ref#suppression) methods instead. Note that you
    can't resubscribe an unsubscribed recipient using WebAPI, but you can send him an email with
    subscription link using email/subscribe method.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def unsubscribed_set(self, request: ObsoleteUnsubscribedSetRequest) -> ObsoleteUnsubscribedSetResponse:
        """Registers a new unsubscribed email.

        After registering an email as unsubscribed all future attempts to send a message to this email will
        be rejected. Please note that there's no way to remove an email from unsubscribed thru the API. But
        you can send an email with a link to resubscribe using
        [email/subscribe](https://docs.unione.io/en/web-api-ref#email-subscribe) method or remove
        "unsubscribed" status manually on [Email Search page](https://cp.unione.io/en/user/email) in control
        panel (but only a limited number of unsubscribed email per day can be removed).

        Documentation: https://docs.unione.io/en/web-api-ref#unsubscribed-set

        Raises ApiError when the API returns an error.
        """
        return ObsoleteUnsubscribedSetResponse.from_dict(self._client.call("/unsubscribed/set.json", request.to_dict()))

    def unsubscribed_check(self, request: ObsoleteUnsubscribedCheckRequest) -> ObsoleteUnsubscribedCheckResponse:
        """Checks if an email is unsubscribed.

        Documentation: https://docs.unione.io/en/web-api-ref#unsubscribed-check

        Raises ApiError when the API returns an error.
        """
        return ObsoleteUnsubscribedCheckResponse.from_dict(self._client.call("/unsubscribed/check.json", request.to_dict()))

    def unsubscribed_list(self, request: ObsoleteUnsubscribedListRequest) -> ObsoleteUnsubscribedListResponse:
        """Returns a list of all unsubscribed emails since provided date.

        Documentation: https://docs.unione.io/en/web-api-ref#unsubscribed-list

        Raises ApiError when the API returns an error.
        """
        return ObsoleteUnsubscribedListResponse.from_dict(self._client.call("/unsubscribed/list.json", request.to_dict()))
