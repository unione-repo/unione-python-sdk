"""EmailValidationApi: API methods of the EmailValidation section."""
import json
from typing import Any, Dict

from ...client import ApiClient
from .models import EmailValidationSingleRequest, EmailValidationSingleResponse


class EmailValidationApi:
    """Email validation methods. As a result of the check, you’ll get detailed information on email
    validity. It will help eliminate nonexistent emails, decrease the number of complaints, clean up the
    subscribers list and eventually enhance your sender reputation score. For example, you may add
    validation to a subscription form on your site to let users know they’ve just entered an invalid
    address.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def single(self, request: EmailValidationSingleRequest) -> EmailValidationSingleResponse:
        """A maximum of two concurrent requests are allowed; if you send more requests, an error will be
        returned. Since the verification process should be completed promptly, we've set a time limit on
        email check. If we encounter a slow email server that does not respond in 5 seconds, you may get an
        “unknown” status.

        Documentation: https://docs.unione.io/en/web-api-ref#email-validation-single

        Raises ApiError when the API returns an error.
        """
        return EmailValidationSingleResponse.from_dict(self._client.call("/email-validation/single.json", request.to_dict()))
