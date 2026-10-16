"""Models of the Webhook section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, map_of, model_of, to_enum

from unione.common import EmailStatus

__all__ = ["WebhookStatus", "WebhookEventFormat", "EventName", "DeviceType", "TrafficType", "BlockType", "DomainStatus", "WebhookSetRequest", "WebhookEventsObject", "WebhookSetResponse", "WebhookObject", "WebhookCallback", "WebhookCallbackEventsByUserItem", "WebhookCallbackEventsByUserItemEventsItem", "WebhookCallbackEventsByUserItemEventsItemEventData", "WebhookCallbackEventsByUserItemEventsItemEventDataDeliveryInfo", "WebhookGetRequest", "WebhookGetResponse", "WebhookListRequest", "WebhookListResponse", "WebhookDeleteRequest"]


class WebhookStatus(str, Enum):
    """Webhook status, "active" by default. "disabled" means that webhook has been disabled by the user,
    "stopped" means that webhook has been stopped by the system after 24h of failed calls (with minimum
    of 10 distinct events).
    """

    ACTIVE = "active"
    DISABLED = "disabled"
    STOPPED = "stopped"


class WebhookEventFormat(str, Enum):
    """Notification format. "json_post"(default) or "json_post_gzip"."""

    JSON_POST = "json_post"
    JSON_POST_GZIP = "json_post_gzip"


class EventName(str, Enum):
    """Type of event data contained in event_data field, either "transactional_email_status" or
    "transactional_spam_block".
    """

    TRANSACTIONAL_EMAIL_STATUS = "transactional_email_status"
    TRANSACTIONAL_SPAM_BLOCK = "transactional_spam_block"


class DeviceType(str, Enum):
    """Recipient's device type, detected from the user agent. Present for "clicked" and "opened" statuses;
    equals "unknown" if the device type couldn't be detected.
    """

    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"
    OTHER = "other"
    UNKNOWN = "unknown"


class TrafficType(str, Enum):
    """Traffic quality for "opened" and "clicked" statuses. "human" means a recognized browser or email
    client without machine signs; "machine" means a bot, link scanner or security proxy; "protected"
    means a mailbox/OS privacy proxy where a human action cannot be confirmed (Apple Mail Privacy
    Protection / iCloud Private Relay, Gmail Image Proxy — Apple MPP is protected, not machine);
    "unknown" means the user agent is missing, broken or not recognized.
    """

    HUMAN = "human"
    MACHINE = "machine"
    PROTECTED = "protected"
    UNKNOWN = "unknown"


class BlockType(str, Enum):
    """Spam block type, either single or multiple sending SMTP. For single sending SMTP block in common
    pool UniOne retries several other SMTPs. This property exists only if
    event_name="transactional_spam_block".
    """

    ONE_SMTP = "one_smtp"
    ALL_SMTP = "all_smtp"


class DomainStatus(str, Enum):
    """Whether it's a block or unblock event. This property exists only if
    event_name="transactional_spam_block".
    """

    BLOCKED = "blocked"
    UNBLOCKED = "unblocked"


@dataclass
class WebhookSetRequest:
    """WebhookSetRequest"""

    url: str
    """URL that will receive the notification when an event occurs. The URL should be unique for a user or
    a project. Only ASCII characters are supported for now in URL, please convert to
    [Punycode](https://en.wikipedia.org/wiki/Punycode) if you need to use non-ASCII characters.
    """

    status: Optional[WebhookStatus] = None
    """Webhook status, "active" by default. "disabled" means that webhook has been disabled by the user,
    "stopped" means that webhook has been stopped by the system after 24h of failed calls (with minimum
    of 10 distinct events).
    Default: `active`.
    """

    event_format: Optional[WebhookEventFormat] = None
    """Notification format. "json_post"(default) or "json_post_gzip".
    Default: `json_post`.
    """

    delivery_info: Optional[int] = None
    """Shall detailed delivery info be returned(1) or not(0). When it's 1, the information about SMTP
    response and internal delivery status is returned for "hard_bounced" and "soft_bounced" email
    statuses; the user agent, recipient IP address, detected geo fields, device info detected from the
    user agent (device type and brand, OS name, browser or email client name) and traffic_type (human,
    machine, protected or unknown) are returned for "opened" and "clicked" statuses; URL is returned for
    "clicked" status. For "delivered", "soft_bounced" and "hard_bounced" statuses UniOne may also return
    sender_ip, the IP address of the SMTP server that sent the message, if available.
    Allowed values: `0`, `1`.
    Default: `0`.
    """

    single_event: Optional[int] = None
    """0=several event notifications can be reported in single webhook call, 1=only single event can be
    reported in one call (not recommended).
    Allowed values: `0`, `1`.
    Default: `0`.
    """

    max_parallel: Optional[int] = None
    """Maximum quantity of permitted parallel queries to your server. The more your server can handle - the
    better.
    Default: `10`.
    """

    events: Optional[WebhookEventsObject] = None
    """Object containing events to notify of."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookSetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            url=data.get("url"),
            status=to_enum(WebhookStatus, data.get("status")),
            event_format=to_enum(WebhookEventFormat, data.get("event_format")),
            delivery_info=data.get("delivery_info"),
            single_event=data.get("single_event"),
            max_parallel=data.get("max_parallel"),
            events=model_of(WebhookEventsObject, data.get("events")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "url": self.url,
            "status": self.status,
            "event_format": self.event_format,
            "delivery_info": self.delivery_info,
            "single_event": self.single_event,
            "max_parallel": self.max_parallel,
            "events": self.events.to_dict() if self.events is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookEventsObject:
    """Object containing events to notify of."""

    spam_block: Optional[List[str]] = None
    """If present then spam block events will be reported. Should contain single array element with "*"
    string.
    """

    email_status: Optional[List[EmailStatus]] = None
    """If present then email status change events will be reported. Contains names of statuses to notify
    of.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookEventsObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            spam_block=list_of(data.get("spam_block")),
            email_status=list_of(data.get("email_status"), lambda item0: to_enum(EmailStatus, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "spam_block": self.spam_block,
            "email_status": self.email_status,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookSetResponse:
    """WebhookSetResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    object: Optional[WebhookObject] = None
    """Object with all the webhook properties."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookSetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            object=model_of(WebhookObject, data.get("object")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "object": self.object.to_dict() if self.object is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookObject:
    """Object with all the webhook properties."""

    id: Optional[int] = None
    """Webhook unique identifier."""

    url: Optional[str] = None
    """Webhook URL."""

    status: Optional[WebhookStatus] = None
    """Webhook status, "active" by default. "disabled" means that webhook has been disabled by the user,
    "stopped" means that webhook has been stopped by the system after 24h of failed calls (with minimum
    of 10 distinct events).
    Default: `active`.
    """

    event_format: Optional[WebhookEventFormat] = None
    """Notification format. "json_post"(default) or "json_post_gzip".
    Default: `json_post`.
    """

    delivery_info: Optional[int] = None
    """Shall detailed delivery info be returned(1) or not(0). When it's 1, the information about SMTP
    response and internal delivery status is returned for "hard_bounced" and "soft_bounced" email
    statuses; the user agent, recipient IP address, detected geo fields, device info detected from the
    user agent (device type and brand, OS name, browser or email client name) and traffic_type (human,
    machine, protected or unknown) are returned for "opened" and "clicked" statuses; URL is returned for
    "clicked" status. For "delivered", "soft_bounced" and "hard_bounced" statuses UniOne may also return
    sender_ip, the IP address of the SMTP server that sent the message, if available.
    Allowed values: `0`, `1`.
    Default: `0`.
    """

    single_event: Optional[int] = None
    """0=several event notifications can be reported in single webhook call, 1=only single event can be
    reported in one call (not recommended).
    Allowed values: `0`, `1`.
    Default: `0`.
    """

    max_parallel: Optional[int] = None
    """Maximum quantity of permitted parallel queries to your server. The more your server can handle - the
    better.
    Default: `10`.
    """

    updated_at: Optional[str] = None
    """Webhook properties last update date and time in UTC timezone in "YYYY-MM-DD hh:mm:ss" format."""

    events: Optional[WebhookEventsObject] = None
    """Object containing events to notify of."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            id=data.get("id"),
            url=data.get("url"),
            status=to_enum(WebhookStatus, data.get("status")),
            event_format=to_enum(WebhookEventFormat, data.get("event_format")),
            delivery_info=data.get("delivery_info"),
            single_event=data.get("single_event"),
            max_parallel=data.get("max_parallel"),
            updated_at=data.get("updated_at"),
            events=model_of(WebhookEventsObject, data.get("events")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "id": self.id,
            "url": self.url,
            "status": self.status,
            "event_format": self.event_format,
            "delivery_info": self.delivery_info,
            "single_event": self.single_event,
            "max_parallel": self.max_parallel,
            "updated_at": self.updated_at,
            "events": self.events.to_dict() if self.events is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookCallback:
    """Webhook callback format description."""

    auth: Optional[str] = None
    """MD5-hash of the message body, in which the value "auth" is replaced by api key of the user/project;
    with this field the recipient of the notification can both authenticate and verify the notification
    integrity
    """

    events_by_user: Optional[List[WebhookCallbackEventsByUserItem]] = None
    """Array with only one element, containing events of a user/project."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookCallback:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            auth=data.get("auth"),
            events_by_user=list_of(data.get("events_by_user"), lambda item0: model_of(WebhookCallbackEventsByUserItem, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "auth": self.auth,
            "events_by_user": [item0.to_dict() for item0 in self.events_by_user] if self.events_by_user is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookCallbackEventsByUserItem:
    """WebhookCallbackEventsByUserItem"""

    user_id: Optional[int] = None
    """Unique user identifier."""

    project_id: Optional[str] = None
    """Project identifier, present only if webhook was registered for the project using project API key."""

    project_name: Optional[str] = None
    """Project name, present only if webhook was registered for the project using project API key."""

    events: Optional[List[WebhookCallbackEventsByUserItemEventsItem]] = None
    """Array of events reported by webhook."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookCallbackEventsByUserItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            user_id=data.get("user_id"),
            project_id=data.get("project_id"),
            project_name=data.get("project_name"),
            events=list_of(data.get("events"), lambda item0: model_of(WebhookCallbackEventsByUserItemEventsItem, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "user_id": self.user_id,
            "project_id": self.project_id,
            "project_name": self.project_name,
            "events": [item0.to_dict() for item0 in self.events] if self.events is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookCallbackEventsByUserItemEventsItem:
    """WebhookCallbackEventsByUserItemEventsItem"""

    event_name: Optional[EventName] = None
    """Type of event data contained in event_data field, either "transactional_email_status" or
    "transactional_spam_block".
    """

    event_data: Optional[WebhookCallbackEventsByUserItemEventsItemEventData] = None
    """Object with different event properties depending on "event_name". Below you can see all the
    properties, "transactional_email_status"-related first and then "transactional_spam_block"-related.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookCallbackEventsByUserItemEventsItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            event_name=to_enum(EventName, data.get("event_name")),
            event_data=model_of(WebhookCallbackEventsByUserItemEventsItemEventData, data.get("event_data")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "event_name": self.event_name,
            "event_data": self.event_data.to_dict() if self.event_data is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookCallbackEventsByUserItemEventsItemEventData:
    """Object with different event properties depending on "event_name". Below you can see all the
    properties, "transactional_email_status"-related first and then "transactional_spam_block"-related.
    """

    job_id: Optional[str] = None
    """Job identifier returned earlier by [email/send](https://docs.unione.io/en/web-api-ref#email-send)
    method. Property exists only if event_name="transactional_email_status".
    """

    metadata: Optional[Dict[str, str]] = None
    """Metadata passed in [email/send](https://docs.unione.io/en/web-api-ref#email-send) method in
    recipients.metadata or global_metadata properties. This property exists only if
    event_name="transactional_email_status".
    """

    email: Optional[str] = None
    """Recipient's email. This property exists only if event_name="transactional_email_status"."""

    status: Optional[EmailStatus] = None
    """Email delivery status. This property exists only if event_name="transactional_email_status".
    Possible values are:

    __accepted__ — the message has been accepted, but not sent yet.
    __sent__ — the message has been sent, but not delivered yet.
    __delivered__ — the message has been delivered. It can be changed to “opened”, “clicked”,
    “unsubscribed”, “subscribed” or “spam”.
    __opened__ — the message has been delivered and read. It can be changed to “clicked”,
    “unsubscribed”, “subscribed” or “spam”.
    __clicked__ — the message has been delivered, read, and at least one of the links in email has been
    clicked. It can be changed to “unsubscribed”, “subscribed” or “spam”.
    __unsubscribed__ — the message has been delivered to the recipient and read, but then the recipient
    unsubscribed. It can be changed to “subscribed”.
    __subscribed__ — the message has been delivered to the recipient and read, but then the recipient
    unsubscribed and subscribed again. It can be changed to “unsubscribed”.
    __soft_bounced__ — temporary delivery failure. UniOne will try to deliver the message during 48
    hours. In case of success the status changes to “delivered”, in case of failure to deliver during 48
    hours message status changes to “hard_bounced”.
    __hard_bounced__ — failed to deliver the message, there will be no delivery attempts. It's a final
    status. There are a lot of possible reasons, you can use SMTP response from
    delivery_info.destination_response field or UniOne internal reason classification from
    delivery_info.delivery_status field to analyze the reason.
    __spam__ — the message has been delivered, but it was reported as spam by the recipient. UniOne can
    receive and process the spam complaint from several domains, including msn.com, outlook.com,
    hotmail.com, live.com, ukr.net, yahoo.com, aol.com using
    [FBL](https://en.wikipedia.org/wiki/Feedback_loop_(email)).
    """

    event_time: Optional[str] = None
    """Event date & time in UTC time zone in "YYYY-MM-DD hh:mm:ss" format. This property exists only if
    event_name="transactional_email_status".
    """

    url: Optional[str] = None
    """URL for "opened" and "clicked" statuses. This property exists only if
    event_name="transactional_email_status".
    """

    delivery_info: Optional[WebhookCallbackEventsByUserItemEventsItemEventDataDeliveryInfo] = None
    """Object with detailed delivery info.Event date & time in UTC time zone in "YYYY-MM-DD hh:mm:ss"
    format. This property exists only if webhook has delivery_info proeprty set to 1 and
    event_name="transactional_email_status".
    """

    block_time: Optional[str] = None
    """Spam block date & time in UTC time zone in "YYYY-MM-DD hh:mm:ss" format. This property exists only
    if event_name="transactional_spam_block".
    """

    block_type: Optional[BlockType] = None
    """Spam block type, either single or multiple sending SMTP. For single sending SMTP block in common
    pool UniOne retries several other SMTPs. This property exists only if
    event_name="transactional_spam_block".
    """

    domain: Optional[str] = None
    """Domain that blocked sending. This property exists only if event_name="transactional_spam_block"."""

    smtp_blocks_count: Optional[int] = None
    """Number of sending SMTPs blocked. This property exists only if event_name="transactional_spam_block"."""

    domain_status: Optional[DomainStatus] = None
    """Whether it's a block or unblock event. This property exists only if
    event_name="transactional_spam_block".
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookCallbackEventsByUserItemEventsItemEventData:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            job_id=data.get("job_id"),
            metadata=map_of(data.get("metadata")),
            email=data.get("email"),
            status=to_enum(EmailStatus, data.get("status")),
            event_time=data.get("event_time"),
            url=data.get("url"),
            delivery_info=model_of(WebhookCallbackEventsByUserItemEventsItemEventDataDeliveryInfo, data.get("delivery_info")),
            block_time=data.get("block_time"),
            block_type=to_enum(BlockType, data.get("block_type")),
            domain=data.get("domain"),
            smtp_blocks_count=data.get("SMTP_blocks_count"),
            domain_status=to_enum(DomainStatus, data.get("domain_status")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "job_id": self.job_id,
            "metadata": self.metadata,
            "email": self.email,
            "status": self.status,
            "event_time": self.event_time,
            "url": self.url,
            "delivery_info": self.delivery_info.to_dict() if self.delivery_info is not None else None,
            "block_time": self.block_time,
            "block_type": self.block_type,
            "domain": self.domain,
            "SMTP_blocks_count": self.smtp_blocks_count,
            "domain_status": self.domain_status,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookCallbackEventsByUserItemEventsItemEventDataDeliveryInfo:
    """Object with detailed delivery info.Event date & time in UTC time zone in "YYYY-MM-DD hh:mm:ss"
    format. This property exists only if webhook has delivery_info proeprty set to 1 and
    event_name="transactional_email_status".
    """

    delivery_status: Optional[str] = None
    """UniOne internal detailed delivery status. Some possible values are:

    __err_user_unknown__ -- email address doesn't exist;
    __err_user_inactive__ -- email address isn't used anymore;
    __err_will_retry__ -- email was temporary rejected, delivery will be retried later;
    __err_mailbox_discarded__ -- email address was active earlier, but now it's deleted;
    __err_mailbox_full__ -- mailbox is full;
    __err_spam_rejected__ -- email was rejected as a spam;
    __err_blacklisted__ -- email was rejected because sender IP or sender domain is found in a black
    list;
    __err_too_large__ -- email size is over limit, according to recipient's server;
    __err_unsubscribed__ -- email was unsubscribed;
    __err_unreachable__ -- numerous delivery failures lead to mark this email address as permanently
    unavailable;
    __err_skip_letter__ -- sending has been canceled because the email address is temporarily
    unavailable;
    __err_domain_inactive__ -- the domain does not accept mail or does not exist;
    __err_destination_misconfigured__ -- the domain does not accept mail due to incorrect settings on
    the recipient’s side, and the server’s response contains information about a cause that can be fixed
    (for example, an inoperative blacklist is used, etc.);
    __err_delivery_failed__ -- delivery failed due to other reasons;
    __err_spam_skipped__ -- sending has been canceled because the campaign has been blocked as a spam;
    __err_lost__ -- the message was not sent due to inconsistency of its parts or it has been lost
    because of the failure on our side. The sender needs to re-send the letter on his own, since the
    original has not been saved;

    We reserve the right to change or add internal delivery statuses as we need, so the following list
    is provided as an example only, without any description: ok_sent, ok_delivered, ok_read,
    ok_link_visited, ok_unsubscribed, ok_resubscribed, ok_spam_folder, ok_fbl, not_sent,
    skip_dup_unreachable, skip_dup_temp_unreachable, skip_dup_mailbox_full, err_spam_removed,
    err_resend, err_unknown, err_retry_letter, err_src_invalid, err_dest_invalid, err_not_available,
    err_internal, err_no_dns, err_no_smtp, err_giveup.
    """

    destination_response: Optional[str] = None
    """SMTP response."""

    user_agent: Optional[str] = None
    """User agent of recipient. Present only if detected for "clicked" and "opened" statuses."""

    device_type: Optional[DeviceType] = None
    """Recipient's device type, detected from the user agent. Present for "clicked" and "opened" statuses;
    equals "unknown" if the device type couldn't be detected.
    """

    device_brand: Optional[str] = None
    """Recipient's device brand, detected from the user agent. Present for "clicked" and "opened" statuses
    if detected. For device_type "mobile" and "tablet" it's always present and equals "unknown" when the
    brand couldn't be detected.
    """

    os_name: Optional[str] = None
    """Name of the operating system of the recipient's device, detected from the user agent. Present for
    "clicked" and "opened" statuses; equals "unknown" if the OS couldn't be detected.
    """

    browser_name: Optional[str] = None
    """Name of the browser the email was opened in, detected from the user agent. Present for "clicked" and
    "opened" statuses only if a browser was detected, so it never comes together with email_client_name.
    """

    email_client_name: Optional[str] = None
    """Name of the email client application the email was opened in, detected from the user agent. Present
    for "clicked" and "opened" statuses only if an email client was detected, so it never comes together
    with browser_name.
    """

    traffic_type: Optional[TrafficType] = None
    """Traffic quality for "opened" and "clicked" statuses. "human" means a recognized browser or email
    client without machine signs; "machine" means a bot, link scanner or security proxy; "protected"
    means a mailbox/OS privacy proxy where a human action cannot be confirmed (Apple Mail Privacy
    Protection / iCloud Private Relay, Gmail Image Proxy — Apple MPP is protected, not machine);
    "unknown" means the user agent is missing, broken or not recognized.
    """

    ip: Optional[str] = None
    """Recipient's IP address. Present only if detected for "clicked" and "opened" statuses."""

    country_code: Optional[str] = None
    """ISO 3166-1 alpha-2 country code detected from recipient IP. Present for "clicked" and "opened"
    statuses.
    """

    country: Optional[str] = None
    """Country detected from recipient IP. Present for "clicked" and "opened" statuses."""

    city: Optional[str] = None
    """City detected from recipient IP. Present for "clicked" and "opened" statuses."""

    sender_ip: Optional[str] = None
    """IP address of the SMTP server that sent the message. Present only for "delivered", "soft_bounced"
    and "hard_bounced" statuses, if available.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookCallbackEventsByUserItemEventsItemEventDataDeliveryInfo:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            delivery_status=data.get("delivery_status"),
            destination_response=data.get("destination_response"),
            user_agent=data.get("user_agent"),
            device_type=to_enum(DeviceType, data.get("device_type")),
            device_brand=data.get("device_brand"),
            os_name=data.get("os_name"),
            browser_name=data.get("browser_name"),
            email_client_name=data.get("email_client_name"),
            traffic_type=to_enum(TrafficType, data.get("traffic_type")),
            ip=data.get("ip"),
            country_code=data.get("country_code"),
            country=data.get("country"),
            city=data.get("city"),
            sender_ip=data.get("sender_ip"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "delivery_status": self.delivery_status,
            "destination_response": self.destination_response,
            "user_agent": self.user_agent,
            "device_type": self.device_type,
            "device_brand": self.device_brand,
            "os_name": self.os_name,
            "browser_name": self.browser_name,
            "email_client_name": self.email_client_name,
            "traffic_type": self.traffic_type,
            "ip": self.ip,
            "country_code": self.country_code,
            "country": self.country,
            "city": self.city,
            "sender_ip": self.sender_ip,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookGetRequest:
    """WebhookGetRequest"""

    url: str
    """Webhook URL."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookGetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            url=data.get("url"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "url": self.url,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookGetResponse:
    """WebhookGetResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    object: Optional[WebhookObject] = None
    """Object with all the webhook properties."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookGetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            object=model_of(WebhookObject, data.get("object")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "object": self.object.to_dict() if self.object is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookListRequest:
    """WebhookListRequest"""

    limit: Optional[int] = None
    """Limits the number of webhooks returned. 50 is recommended."""

    offset: Optional[int] = None
    """Index of the first webhook in the list, starting with 0.
    Default: `0`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookListRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            limit=data.get("limit"),
            offset=data.get("offset"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "limit": self.limit,
            "offset": self.offset,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookListResponse:
    """WebhookListResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    objects: Optional[List[WebhookObject]] = None
    """Array of webhooks objects."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            objects=list_of(data.get("objects"), lambda item0: model_of(WebhookObject, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "objects": [item0.to_dict() for item0 in self.objects] if self.objects is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class WebhookDeleteRequest:
    """WebhookDeleteRequest"""

    url: str
    """Webhook URL."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookDeleteRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            url=data.get("url"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "url": self.url,
        }
        return {k: v for k, v in result.items() if v is not None}
