"""EmailApi: API methods of the Email section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from ...common.models import SuccessResponse
from .models import EmailSendRequest, EmailSendResponse, EmailSubscribeRequest


class EmailApi:
    """This group of methods is related with email sending."""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def send(self, request: EmailSendRequest) -> EmailSendResponse:
        """Sends an email or a bunch of emails

        While sending you can provide substitutions (merge tags), use a template, turn on read or click
        tracking, etc.

        Restrictions:
        * maximum request size is 10 MB
        * maximum number of recipients is 500
        * The symbol '/' is not allowed in attachment names

        If the list of recipients contains invalid, non-existent, duplicate, or unsubscribed emails, those
        emails will be returned in the output parameter failed_emails, and the email will be sent to all
        other valid emails addresses. If all the emails addresses fall into failed_emails, sending will not
        be carried out and API error 204 will be returned.

        Documentation: https://docs.unione.io/en/web-api-ref#email-send

        Raises ApiError when the API returns an error.
        """
        return EmailSendResponse.from_dict(self._client.call("/email/send.json", request.to_dict()))

    def subscribe(self, request: EmailSubscribeRequest) -> SuccessResponse:
        """Sends an email with (re)subscribe link.

        This method allows subscription renewal by a former subscriber who has previously unsubscribed, or
        who is blocked because of complaints. This method sends an email with a new subscription link to a
        former subscriber. Once the recipient clicks the link, their subscription status is restored.
        There is a default restriction that limits this method to being used once a day. If you need to
        resubscribe more often, please ask support about it.

        Documentation: https://docs.unione.io/en/web-api-ref#email-subscribe

        Raises ApiError when the API returns an error.
        """
        return SuccessResponse.from_dict(self._client.call("/email/subscribe.json", request.to_dict()))
