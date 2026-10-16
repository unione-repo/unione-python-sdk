"""Models of the ConfirmedEmail section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, model_of, to_enum

from unione.common import VerificationRecordStatus

__all__ = ["ConfirmedEmailRequest", "ConfirmedEmailCreateResponse", "ConfirmedEmail", "ConfirmedEmailListResponse", "ConfirmedEmailDeleteResponse"]


@dataclass
class ConfirmedEmailRequest:
    """ConfirmedEmailRequest"""

    email: str
    """Email address to add or delete."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ConfirmedEmailRequest:
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


@dataclass
class ConfirmedEmailCreateResponse:
    """ConfirmedEmailCreateResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    confirmed_email: Optional[ConfirmedEmail] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ConfirmedEmailCreateResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            confirmed_email=model_of(ConfirmedEmail, data.get("confirmed_email")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "confirmed_email": self.confirmed_email.to_dict() if self.confirmed_email is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ConfirmedEmail:
    """ConfirmedEmail"""

    email: Optional[str] = None

    status: Optional[VerificationRecordStatus] = None
    """Confirmation status of the email address."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ConfirmedEmail:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            email=data.get("email"),
            status=to_enum(VerificationRecordStatus, data.get("status")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "email": self.email,
            "status": self.status,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ConfirmedEmailListResponse:
    """ConfirmedEmailListResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    confirmed_emails: Optional[List[ConfirmedEmail]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ConfirmedEmailListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            confirmed_emails=list_of(data.get("confirmed_emails"), lambda item0: model_of(ConfirmedEmail, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "confirmed_emails": [item0.to_dict() for item0 in self.confirmed_emails] if self.confirmed_emails is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ConfirmedEmailDeleteResponse:
    """ConfirmedEmailDeleteResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    message: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ConfirmedEmailDeleteResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            message=data.get("message"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "message": self.message,
        }
        return {k: v for k, v in result.items() if v is not None}
