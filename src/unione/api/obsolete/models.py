"""Models of the Obsolete section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, model_of, to_enum

__all__ = ["ObsoleteUnsubscribedSetMessage", "ObsoleteUnsubscribedSetRequest", "ObsoleteUnsubscribedSetResponse", "ObsoleteUnsubscribedCheckRequest", "ObsoleteUnsubscribedCheckResponse", "ObsoleteUnsubscribedListRequest", "ObsoleteUnsubscribedListResponse", "ObsoleteUnsubscribedListResponseUnsubscribedItem"]


class ObsoleteUnsubscribedSetMessage(str, Enum):
    """Unsubscription process details:

    - "unsubscribed" if email has just been unsubscribed,
    - "was inactive" if it was inactive due some reason,
    - "was unsubscribed" if it already was unsubscribed before the call,
    - "added and unsubscribed" if it's a new email without status history and it was added and then unsubscribed immediately.
    """

    UNSUBSCRIBED = "unsubscribed"
    WAS_INACTIVE = "was inactive"
    WAS_UNSUBSCRIBED = "was unsubscribed"
    ADDED_AND_UNSUBSCRIBED = "added and unsubscribed"


@dataclass
class ObsoleteUnsubscribedSetRequest:
    """ObsoleteUnsubscribedSetRequest"""

    address: str
    """Email to be unsubscribed."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedSetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            address=data.get("address"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "address": self.address,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ObsoleteUnsubscribedSetResponse:
    """ObsoleteUnsubscribedSetResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    address: Optional[str] = None
    """The unsubscribed email."""

    message: Optional[ObsoleteUnsubscribedSetMessage] = None
    """Unsubscription process details:

    - "unsubscribed" if email has just been unsubscribed,
    - "was inactive" if it was inactive due some reason,
    - "was unsubscribed" if it already was unsubscribed before the call,
    - "added and unsubscribed" if it's a new email without status history and it was added and then unsubscribed immediately.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedSetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            address=data.get("address"),
            message=to_enum(ObsoleteUnsubscribedSetMessage, data.get("message")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "address": self.address,
            "message": self.message,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ObsoleteUnsubscribedCheckRequest:
    """ObsoleteUnsubscribedCheckRequest"""

    address: str
    """Email to check."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedCheckRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            address=data.get("address"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "address": self.address,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ObsoleteUnsubscribedCheckResponse:
    """ObsoleteUnsubscribedCheckResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    address: Optional[str] = None
    """Email that was checked."""

    is_unsubscribed: Optional[bool] = None
    """true if unsubscribed, false if not."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedCheckResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            address=data.get("address"),
            is_unsubscribed=data.get("is_unsubscribed"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "address": self.address,
            "is_unsubscribed": self.is_unsubscribed,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ObsoleteUnsubscribedListRequest:
    """ObsoleteUnsubscribedListRequest"""

    date_from: Optional[str] = None
    """Date in the format YYYY-MM-DD to get all unsubscribed emails from the "date_from" to the present
    day. If the parameter is not specified, the default period is today (from 00:00 UTC).
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedListRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            date_from=data.get("date_from"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "date_from": self.date_from,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ObsoleteUnsubscribedListResponse:
    """ObsoleteUnsubscribedListResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    unsubscribed: Optional[List[ObsoleteUnsubscribedListResponseUnsubscribedItem]] = None
    """Array of object describing unsubscribed emails."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            unsubscribed=list_of(data.get("unsubscribed"), lambda item0: model_of(ObsoleteUnsubscribedListResponseUnsubscribedItem, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "unsubscribed": [item0.to_dict() for item0 in self.unsubscribed] if self.unsubscribed is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ObsoleteUnsubscribedListResponseUnsubscribedItem:
    """ObsoleteUnsubscribedListResponseUnsubscribedItem"""

    address: Optional[str] = None
    """Unsubscribed email."""

    unsubscribed_on: Optional[str] = None
    """Date and time when a recipient unsubscribed, in UTC timezone and "YYYY-MM-DD hh:mm:ss" format."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ObsoleteUnsubscribedListResponseUnsubscribedItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            address=data.get("address"),
            unsubscribed_on=data.get("unsubscribed_on"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "address": self.address,
            "unsubscribed_on": self.unsubscribed_on,
        }
        return {k: v for k, v in result.items() if v is not None}
