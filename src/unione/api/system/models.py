"""Models of the System section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, model_of, to_enum

from unione.common import EmailCounterMode

__all__ = ["SystemPingResponse", "SystemInfoResponse", "ProjectAccountingObject", "SystemInfoResponseAccounting"]


@dataclass
class SystemPingResponse:
    """SystemPingResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    user_id: Optional[int] = None
    """Unique user identifier."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SystemPingResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            user_id=data.get("user_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "user_id": self.user_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SystemInfoResponse:
    """SystemInfoResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    user_id: Optional[int] = None
    """Unique user identifier."""

    email: Optional[str] = None
    """Email of the user."""

    project_id: Optional[str] = None
    """Unqiue project identifier, ASCII string up to 36 characters long. Present only if the API key used
    for request is the project API key.
    """

    project_name: Optional[str] = None
    """Project name, unique for user account. Present only if the API key used for request is the project
    API key.
    """

    project_accounting: Optional[ProjectAccountingObject] = None
    """Object with email counter properties. Present only if the API key used for request is the user API
    key.
    """

    accounting: Optional[SystemInfoResponseAccounting] = None
    """Object with accounting period properties. Present only if the API key used for request is the user
    API key.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SystemInfoResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            user_id=data.get("user_id"),
            email=data.get("email"),
            project_id=data.get("project_id"),
            project_name=data.get("project_name"),
            project_accounting=model_of(ProjectAccountingObject, data.get("project_accounting")),
            accounting=model_of(SystemInfoResponseAccounting, data.get("accounting")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "user_id": self.user_id,
            "email": self.email,
            "project_id": self.project_id,
            "project_name": self.project_name,
            "project_accounting": self.project_accounting.to_dict() if self.project_accounting is not None else None,
            "accounting": self.accounting.to_dict() if self.accounting is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectAccountingObject:
    """Object with email counter properties. Present only if the API key used for request is the user API
    key.
    """

    email_counter: Optional[int] = None
    """Project's email counter value. It increases on every email sent."""

    email_counter_limit: Optional[int] = None
    """Allows you to limit the number of emails sent by the project. The sending stops when the limit is
    reached. Any non-negative 64-bit integer is acceptable. 0 means no limit.
    """

    email_counter_mode: Optional[EmailCounterMode] = None
    """'default' - the counter resets to zero automatically at the beginning of each accounting period.
    'permanent' - the counter never resets automatically.
    Default: `default`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectAccountingObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            email_counter=data.get("email_counter"),
            email_counter_limit=data.get("email_counter_limit"),
            email_counter_mode=to_enum(EmailCounterMode, data.get("email_counter_mode")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "email_counter": self.email_counter,
            "email_counter_limit": self.email_counter_limit,
            "email_counter_mode": self.email_counter_mode,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SystemInfoResponseAccounting:
    """Object with accounting period properties. Present only if the API key used for request is the user
    API key.
    """

    period_start: Optional[str] = None
    """Date and time of accounting period start in UTC in "YYYY-MM-DD hh:mm:ss" format."""

    period_end: Optional[str] = None
    """Date and time of accounting period end in UTC in "YYYY-MM-DD hh:mm:ss" format."""

    emails_included: Optional[int] = None
    """Number of emails included into accounting period."""

    emails_sent: Optional[int] = None
    """Number of emails sent during accounting period. Can be bigger than emails_included in case of
    overage.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SystemInfoResponseAccounting:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            period_start=data.get("period_start"),
            period_end=data.get("period_end"),
            emails_included=data.get("emails_included"),
            emails_sent=data.get("emails_sent"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "period_start": self.period_start,
            "period_end": self.period_end,
            "emails_included": self.emails_included,
            "emails_sent": self.emails_sent,
        }
        return {k: v for k, v in result.items() if v is not None}
