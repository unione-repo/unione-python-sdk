"""Models of the Suppression section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, model_of

__all__ = ["SuppressionSetRequest", "SuppressionGetRequest", "SuppressionGetResponse", "SuppressionGetObject", "SuppressionListRequest", "SuppressionListResponse", "SuppressionListObject", "SuppressionDeleteRequest"]


@dataclass
class SuppressionSetRequest:
    """SuppressionSetRequest"""

    email: str
    """Email to add in suppression list."""

    cause: str
    """Cause of email being suppressed. One of:

    - __unsubscribed__ - email is unsubscribed;
    - __temporary_unavailable__ - the email address is unavailable. This means that over the next three days sending to this address will return an error. Email may be temporarily unavailable due to several reasons, e.g.:

    - a previous email has been rejected by the recipient's server for spam;
    - the recipient's mailbox is full or is not used;
    - recipient's domain does not accept mail;
    - sending server was rejected due to blacklisting;

    - __permanent_unavailable__ - the email address is permanently unavailable due to multiple hard bounces;
    - __complained__ -  the recipient reported spam in the previous emails;
    """

    created: Optional[str] = None
    """When suppression was created, in UTC timezone in "YYYY-MM-DD hh:mm:ss" format."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionSetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            email=data.get("email"),
            cause=data.get("cause"),
            created=data.get("created"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "email": self.email,
            "cause": self.cause,
            "created": self.created,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionGetRequest:
    """SuppressionGetRequest"""

    email: str
    """Email to get suppression details for."""

    all_projects: Optional[bool] = None
    """If a user has projects functionality enabled, he/she can pass all_projects=true to search in all
    projects' data.
    Default: `False`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionGetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            email=data.get("email"),
            all_projects=data.get("all_projects"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "email": self.email,
            "all_projects": self.all_projects,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionGetResponse:
    """SuppressionGetResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    email: Optional[str] = None
    """The email for which suppression details were requested."""

    suppressions: Optional[List[SuppressionGetObject]] = None
    """Array of suppression objects."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionGetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            email=data.get("email"),
            suppressions=list_of(data.get("suppressions"), lambda item0: model_of(SuppressionGetObject, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "email": self.email,
            "suppressions": [item0.to_dict() for item0 in self.suppressions] if self.suppressions is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionGetObject:
    """Object with suppression details."""

    project_id: Optional[str] = None
    """Unqiue project identifier, ASCII string up to 36 characters long."""

    cause: Optional[str] = None
    """Cause of email being suppressed. One of:

    - __unsubscribed__ - email is unsubscribed;
    - __temporary_unavailable__ - the email address is unavailable. This means that over the next three days sending to this address will return an error. Email may be temporarily unavailable due to several reasons, e.g.:

    - a previous email has been rejected by the recipient's server for spam;
    - the recipient's mailbox is full or is not used;
    - recipient's domain does not accept mail;
    - sending server was rejected due to blacklisting;

    - __permanent_unavailable__ - the email address is permanently unavailable due to multiple hard bounces;
    - __complained__ -  the recipient reported spam in the previous emails;
    - __blocked__ -  sending to the email is prohibited by administration of UniOne.
    We may add some new causes in the future.
    """

    source: Optional[str] = None
    """Source of email being suppressed. One of:

    - __user__ - suppressed by user with    [suppression/set](https://docs.unione.io/en/web-api-ref#suppression-set);
    - __system__ - sending to the email is prohibited by system, for example due to multiple hard bounces;
    - __subscriber__ - the recipient reported spam or unsubscribed in the previous emails.
    """

    is_deletable: Optional[bool] = None
    """Is it possible to delete this suppression by calling suppression/delete method."""

    created: Optional[str] = None
    """When suppression was created, in UTC timezone in "YYYY-MM-DD hh:mm:ss" format."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionGetObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            project_id=data.get("project_id"),
            cause=data.get("cause"),
            source=data.get("source"),
            is_deletable=data.get("is_deletable"),
            created=data.get("created"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "project_id": self.project_id,
            "cause": self.cause,
            "source": self.source,
            "is_deletable": self.is_deletable,
            "created": self.created,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionListRequest:
    """SuppressionListRequest"""

    cause: Optional[str] = None
    """Cause of email being suppressed. One of:

    - __unsubscribed__ - email is unsubscribed;
    - __temporary_unavailable__ - the email address is unavailable. This means that over the next three days sending to this address will return an error. Email may be temporarily unavailable due to several reasons, e.g.:

    - a previous email has been rejected by the recipient's server for spam;
    - the recipient's mailbox is full or is not used;
    - recipient's domain does not accept mail;
    - sending server was rejected due to blacklisting;

    - __permanent_unavailable__ - the email address is permanently unavailable due to multiple hard bounces;
    - __complained__ -  the recipient reported spam in the previous emails;
    - __blocked__ -  sending to the email is prohibited by administration of UniOne.
    We may add some new causes in the future.
    """

    source: Optional[str] = None
    """Source of email being suppressed. One of:

    - __user__ - suppressed by user with    [suppression/set](https://docs.unione.io/en/web-api-ref#suppression-set);
    - __system__ - sending to the email is prohibited by system, for example due to multiple hard bounces;
    - __subscriber__ - the recipient reported spam or unsubscribed in the previous emails.
    """

    start_time: Optional[str] = None
    """Date in the format YYYY-MM-DD hh:mm:ss to get suppression list from the "start_time" to the present
    day. Ignored if "cursor" is not empty.
    """

    cursor: Optional[str] = None
    """The parameter indicates from which position the selection is to be started. Must be empty or omitted
    for the first data chunk. In order to get subsequent chunks, you must set the "cursor" parameter in
    your request, using the value received in response to the previous request.
    """

    limit: Optional[int] = None
    """Limits the number of records to be returned at one time, default is 50."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionListRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            cause=data.get("cause"),
            source=data.get("source"),
            start_time=data.get("start_time"),
            cursor=data.get("cursor"),
            limit=data.get("limit"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "cause": self.cause,
            "source": self.source,
            "start_time": self.start_time,
            "cursor": self.cursor,
            "limit": self.limit,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionListResponse:
    """SuppressionListResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    suppressions: Optional[List[SuppressionListObject]] = None
    """Array of suppression objects."""

    cursor: Optional[str] = None
    """The parameter indicates from which position the selection is to be started. Must be empty or omitted
    for the first data chunk. In order to get subsequent chunks, you must set the "cursor" parameter in
    your request, using the value received in response to the previous request.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            suppressions=list_of(data.get("suppressions"), lambda item0: model_of(SuppressionListObject, item0)),
            cursor=data.get("cursor"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "suppressions": [item0.to_dict() for item0 in self.suppressions] if self.suppressions is not None else None,
            "cursor": self.cursor,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionListObject:
    """Object with suppression details."""

    email: Optional[str] = None
    """Email to get suppression details for."""

    cause: Optional[str] = None
    """Cause of email being suppressed. One of:

    - __unsubscribed__ - email is unsubscribed;
    - __temporary_unavailable__ - the email address is unavailable. This means that over the next three days sending to this address will return an error. Email may be temporarily unavailable due to several reasons, e.g.:

    - a previous email has been rejected by the recipient's server for spam;
    - the recipient's mailbox is full or is not used;
    - recipient's domain does not accept mail;
    - sending server was rejected due to blacklisting;

    - __permanent_unavailable__ - the email address is permanently unavailable due to multiple hard bounces;
    - __complained__ -  the recipient reported spam in the previous emails;
    - __blocked__ -  sending to the email is prohibited by administration of UniOne.
    We may add some new causes in the future.
    """

    source: Optional[str] = None
    """Source of email being suppressed. One of:

    - __user__ - suppressed by user with    [suppression/set](https://docs.unione.io/en/web-api-ref#suppression-set);
    - __system__ - sending to the email is prohibited by system, for example due to multiple hard bounces;
    - __subscriber__ - the recipient reported spam or unsubscribed in the previous emails.
    """

    is_deletable: Optional[bool] = None
    """Is it possible to delete this suppression by calling suppression/delete method."""

    created: Optional[str] = None
    """When suppression was created, in UTC timezone in "YYYY-MM-DD hh:mm:ss" format."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionListObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            email=data.get("email"),
            cause=data.get("cause"),
            source=data.get("source"),
            is_deletable=data.get("is_deletable"),
            created=data.get("created"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "email": self.email,
            "cause": self.cause,
            "source": self.source,
            "is_deletable": self.is_deletable,
            "created": self.created,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuppressionDeleteRequest:
    """SuppressionDeleteRequest"""

    email: str
    """An email to delete from suppression list."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuppressionDeleteRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            email=data.get("email"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "email": self.email,
        }
        return {k: v for k, v in result.items() if v is not None}
