"""Models of the EventDump section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, model_of, to_enum

from unione.common import EmailStatus

__all__ = ["EventDumpCreateRequest", "FilterObject", "EventDumpCreateResponse", "EventDumpGetRequest", "EventDumpGetResponse", "EventDumpObject", "EventDumpFilesObject", "EventDumpListResponse", "EventDumpDeleteRequest"]


@dataclass
class EventDumpCreateRequest:
    """EventDumpCreateRequest"""

    start_time: str
    """Date and time in YYYY-MM-DD hh:mm:ss format, specifying period start time. Data is stored for up to
    32 days, depending on your tariff.
    """

    end_time: Optional[str] = None
    """Date and time in YYYY-MM-DD hh:mm:ss format, specifying period end time (non-inclusive)."""

    limit: Optional[int] = None
    """Maximum number of events returned (default is 50). If this value is over 100 000, several files will
    be created, each having 100 000 events maximum.
    """

    all_projects: Optional[bool] = None
    """For accounts with projects enabled, the value all_projects=true allows to fetch data for all
    existing projects.
    Default: `False`.
    """

    filter: Optional[FilterObject] = None
    """An object with the properties of the event dump filter."""

    dump_fields: Optional[List[str]] = None
    """An array of strings containing the names of columns you need in your report, in your preferred
    order. If the 'dump_fields' array is missing or empty, a default field list and order will be
    applied. Allowed values, in their default order, are - 'project_id', 'event_time', 'job_id',
    'from_email', 'email', 'status', 'delivery_status', 'metadata', 'destination_response',
    'user_agent', 'url', 'ip', 'tags'. For maximum security, the 'subject' field is not included by
    default, but you can add it by explicitly including in the 'dump_fields' array.
    """

    aggregate: Optional[str] = None
    """Allows you to obtain aggregated statistics for a given time period. The two allowed values are:

    - __day_status__ - fetch aggregated statistics (the filter value must be missing or empty, as filters are not allowed with this option);
    - __an empty string__ - used by default, event_dump/create works as if the aggregate parameter is omitted.
    """

    delimiter: Optional[str] = None
    """Field delimiter, can be set to either  ',' or ';', defaults to  ','."""

    format: Optional[str] = None
    """File format, either “csv” (default) or “csv_gzip”.
    Default: `csv`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpCreateRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            limit=data.get("limit"),
            all_projects=data.get("all_projects"),
            filter=model_of(FilterObject, data.get("filter")),
            dump_fields=list_of(data.get("dump_fields")),
            aggregate=data.get("aggregate"),
            delimiter=data.get("delimiter"),
            format=data.get("format"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "limit": self.limit,
            "all_projects": self.all_projects,
            "filter": self.filter.to_dict() if self.filter is not None else None,
            "dump_fields": self.dump_fields,
            "aggregate": self.aggregate,
            "delimiter": self.delimiter,
            "format": self.format,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class FilterObject:
    """An object with the properties of the event dump filter."""

    job_id: Optional[str] = None
    """Job identifier returned earlier by [email/send](https://docs.unione.io/en/web-api-ref#email-send)
    method.
    """

    status: Optional[EmailStatus] = None
    """Email status. Possible values are:

    __accepted__ — the message has been accepted, but not sent yet.
    __sent__ — the message has been sent, but not delivered yet.
    __delivered__ — the message has been delivered.
    __opened__ — the message has been delivered and read.
    __clicked__ — the message has been delivered, read, and at least one of the links in email has been
    clicked.
    __unsubscribed__ — the message has been delivered to the recipient and read, but then the recipient
    unsubscribed.
    __subscribed__ — the message has been delivered to the recipient and read, but then the recipient
    unsubscribed and subscribed again.
    __soft_bounced__ — temporary delivery failure. UniOne will try to deliver the message during 48
    hours.
    __hard_bounced__ — failed to deliver the message, there will be no delivery attempts.
    __spam__ — the message has been delivered, but it was reported as spam by the recipient.
    """

    delivery_status: Optional[str] = None
    """UniOne internal detailed delivery status, you can pass several values at once, comma-separated. Some
    possible values are:

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

    email: Optional[str] = None
    """Recipient email address"""

    email_from: Optional[str] = None
    """Sender email address"""

    domain: Optional[str] = None
    """Recipient domain"""

    campaign_id: Optional[str] = None
    """Campaign identifier, unsigned decimal integer or UUID up to 128-bit, passed in metadata with name
    "campaign_id" (name is configurable thru support).
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> FilterObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            job_id=data.get("job_id"),
            status=to_enum(EmailStatus, data.get("status")),
            delivery_status=data.get("delivery_status"),
            email=data.get("email"),
            email_from=data.get("email_from"),
            domain=data.get("domain"),
            campaign_id=data.get("campaign_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "job_id": self.job_id,
            "status": self.status,
            "delivery_status": self.delivery_status,
            "email": self.email,
            "email_from": self.email_from,
            "domain": self.domain,
            "campaign_id": self.campaign_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpCreateResponse:
    """EventDumpCreateResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    dump_id: Optional[str] = None
    """Dump identifier, used to call the
    [event-dump/get](https://docs.unione.io/en/web-api-ref#event-dump-get) method.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpCreateResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            dump_id=data.get("dump_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "dump_id": self.dump_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpGetRequest:
    """EventDumpGetRequest"""

    dump_id: str
    """Dump identifier received by the method
    [event-dump/create](https://docs.unione.io/en/web-api-ref#event-dump-create).
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpGetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            dump_id=data.get("dump_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "dump_id": self.dump_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpGetResponse:
    """EventDumpGetResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    event_dump: Optional[EventDumpObject] = None
    """An object with the properties of the event dump."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpGetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            event_dump=model_of(EventDumpObject, data.get("event_dump")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "event_dump": self.event_dump.to_dict() if self.event_dump is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpObject:
    """An object with the properties of the event dump."""

    dump_id: Optional[str] = None
    """Dump ID received by the method
    [event-dump/create](https://docs.unione.io/en/web-api-ref#event-dump-create).
    """

    dump_status: Optional[str] = None
    """Task status, possible values are:

    - __queued__ - the task is in the queue, processing is not started yet;
    - __in_process__ - the request is being processed;
    - __ready__ - the task is finished, dump file is ready for download;
    - __failed__ -  processing failed due to an internal error.
    """

    files: Optional[List[EventDumpFilesObject]] = None
    """An array of objects, each representing a file, ready for download. You may start downloading
    everything listed in “files” even if "dump_status" is still "in_process". If there are no events,
    according to the specified parameters, an empty array will be returned.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            dump_id=data.get("dump_id"),
            dump_status=data.get("dump_status"),
            files=list_of(data.get("files"), lambda item0: model_of(EventDumpFilesObject, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "dump_id": self.dump_id,
            "dump_status": self.dump_status,
            "files": [item0.to_dict() for item0 in self.files] if self.files is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpFilesObject:
    """An object with the properties of the event dump file."""

    url: Optional[str] = None
    """Use this unique URL to download the requested dump file (either .csv or .csv.gz, depending on your
    request).
    """

    size: Optional[int] = None
    """File size."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpFilesObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            url=data.get("url"),
            size=data.get("size"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "url": self.url,
            "size": self.size,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpListResponse:
    """EventDumpListResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    event_dumps: Optional[List[EventDumpObject]] = None
    """An array of objects describing event dumps. Each object is similar to 'event_dump' object returned
    by the [event-dump/get](https://docs.unione.io/en/web-api-ref#event-dump-get) method.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            event_dumps=list_of(data.get("event_dumps"), lambda item0: model_of(EventDumpObject, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "event_dumps": [item0.to_dict() for item0 in self.event_dumps] if self.event_dumps is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EventDumpDeleteRequest:
    """EventDumpDeleteRequest"""

    dump_id: str
    """Dump identifier, obtained via the
    [event-dump/create](https://docs.unione.io/en/web-api-ref#event-dump-create) method.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EventDumpDeleteRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            dump_id=data.get("dump_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "dump_id": self.dump_id,
        }
        return {k: v for k, v in result.items() if v is not None}
