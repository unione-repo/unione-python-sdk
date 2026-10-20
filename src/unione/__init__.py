"""UniOne API client."""
from typing import Dict, Optional

from .client import ApiClient, ApiError, Configuration, Transport, TransportLike, UrllibTransport, base_url_for
from .api.email import EmailApi
from .api.email_validation import EmailValidationApi
from .api.confirmed_email import ConfirmedEmailApi
from .api.template import TemplateApi
from .api.webhook import WebhookApi
from .api.suppression import SuppressionApi
from .api.domain import DomainApi
from .api.event_dump import EventDumpApi
from .api.tag import TagApi
from .api.project import ProjectApi
from .api.system import SystemApi
from .api.obsolete import ObsoleteApi

__all__ = ["client", "UniOneClient", "ApiClient", "ApiError", "Configuration", "Transport", "UrllibTransport"]
__version__ = "1.1.3"


class UniOneClient:
    """Entry point of the UniOne API: one attribute per section.

        client = UniOneClient("YOUR_API_KEY")
        client.email.send(...)
    """

    def __init__(self, api_key: str, host: Optional[str] = None, timeout: float = 30.0,
            platform: Optional[str] = None, transport: Optional[TransportLike] = None,
            headers: Optional[Dict[str, str]] = None) -> None:
        """host: API host (HOST_* constants of the client package, e.g. "us1.unione.io") or a full base URL;
        None: the default one.
        platform: package that uses the SDK and its version (e.g. "django.1.0.0"), sent in the "platform"
        query parameter before the SDK one.
        transport: HTTP layer, an object with send(method, url, headers, body, timeout) -> (status, body) or
        such a function (client.Transport); None: UrllibTransport.
        headers: extra HTTP headers of every request.
        """
        config = Configuration(api_key, timeout=timeout, platform=platform, headers=dict(headers or {}))
        if host:
            config.base_url = base_url_for(host)
        self.api_client = ApiClient(config, transport)
        self.email = EmailApi(self.api_client)
        """This group of methods is related with email sending."""
        self.email_validation = EmailValidationApi(self.api_client)
        """Email validation methods. As a result of the check, you’ll get detailed information on email
        validity. It will help eliminate nonexistent emails, decrease the number of complaints, clean up the
        subscribers list and eventually enhance your sender reputation score. For example, you may add
        validation to a subscription form on your site to let users know they’ve just entered an invalid
        address.
        """
        self.confirmed_email = ConfirmedEmailApi(self.api_client)
        """Manage email addresses confirmed for sandbox-domain sending. These methods are available only with a
        main account API key.
        """
        self.template = TemplateApi(self.api_client)
        """You have the option of storing a template on the UniOne side and then using it by id, which is
        highly recommended for sending repetitive messages or high volume traffic. UniOne supports two
        different [template engines](https://docs.unione.io/en/template-engines).
        """
        self.webhook = WebhookApi(self.api_client)
        """UniOne lets you recieve notifications about email status changes or spam blocks. You provide an URL
        and every time a watched event occurs we will notify you by submitting a request with JSON data to
        this URL.
        """
        self.suppression = SuppressionApi(self.api_client)
        """Methods for managing suppression lists. An email can be added to suppression list because of
        unsubscription, bounce or complain.
        """
        self.domain = DomainApi(self.api_client)
        """You can use these methods to setup sender domains and check their statuses. They might be useful in
        case you want to automate adding domains for your own clients.
        """
        self.event_dump = EventDumpApi(self.api_client)
        """These methods are used to obtain a list of events for a given period of time. The data is stored for
        up to 45 days, depending on your tariff, i. e. you may fetch all event data starting from 00:00:00
        31 days ago and up to current time. For custom tarifs with big sending volumes event dumps are
        available only for the last 7 days.
        """
        self.tag = TagApi(self.api_client)
        """This family of methods is used to manage user-defined tags. Tags are used to categorize letters
        based on your own criteria, e. g. to create a distinction between marketing and transactional
        letters or group together all notifications for a particular order type. UniOne allows you to assign
        tags to all outgoing emails, and the tags you’ve set may then be used to filter and analyze delivery
        statistics.
        """
        self.project = ProjectApi(self.api_client)
        """Projects allow you to group several independent domains, webhooks, templates, and unsubscription
        lists together. It's very useful if you have your own clients and manage their data from a single
        UniOne account. Each project receives its own API key, and all API calls with that API key only deal
        with the data of that project. This way, you can assign a separate project for each client and be
        sure that they won't conflict; e.g. unsubscribing from one project won't affect another.
        """
        self.system = SystemApi(self.api_client)
        """System operations."""
        self.obsolete = ObsoleteApi(self.api_client)
        """Obsolete methods dealing with unsubscribes. We recommend using the more flexible
        [suppression](https://docs.unione.io/en/web-api-ref#suppression) methods instead. Note that you
        can't resubscribe an unsubscribed recipient using WebAPI, but you can send him an email with
        subscription link using email/subscribe method.
        """


def client(api_key: str, host: Optional[str] = None, timeout: float = 30.0, *,
           platform: Optional[str] = None, transport: Optional[TransportLike] = None,
           headers: Optional[Dict[str, str]] = None) -> UniOneClient:
    """Create the API client: ``unione.client("YOUR_API_KEY")`` or ``unione.client("YOUR_API_KEY",
    "us1.unione.io")``; the other arguments: see UniOneClient.
    """
    return UniOneClient(api_key, host, timeout, platform, transport, headers)
