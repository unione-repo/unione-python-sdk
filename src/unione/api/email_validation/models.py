"""Models of the EmailValidation section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict

__all__ = ["EmailValidationSingleRequest", "EmailValidationSingleResponse"]


@dataclass
class EmailValidationSingleRequest:
    """EmailValidationSingleRequest"""

    email: str
    """Email address to be checked."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EmailValidationSingleRequest:
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
class EmailValidationSingleResponse:
    """EmailValidationSingleResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    email: Optional[str] = None
    """Email address to be checked."""

    result: Optional[str] = None
    """Possible statuses:

    - "valid" - the address is valid,
    - "invalid" - the address is invalid,
    - "suspicious" - the address looks suspicious,
    - "unknown" - could not perform validation, the domain’s mail server has not responded within the time limit.
    """

    cause: Optional[str] = None
    """Possible statuses:

    - "no_mx_record" - no MX record found for the target domain,
    - "syntax_error" - the address syntax is invalid,
    - "possible_typo" - the address is likely to have a typo,
    - "mailbox_not_found" - the address does not exist,
    - "global_suppression" - the address has been marked as unreachable due to multiple previous delivery errors,
    - "disposable" - this is a disposable one-time email address which is usually valid for a few minutes only,
    - "role" - the address is not likely to belong to an actual person, but rather to a certain business staff role,
    - "abuse" - the address is known to be a source of a large number of complaints, sometimes issued automatically,
    - "spamtrap" - this email is a spam trap, it is published openly but never used for actual emails. Sending messages to such addresses has a huge negative impact on reputation score,
    - "smtp_connection_failed" - the domain’s SMTP server does not respond; the address may contain a typo.
    """

    validity: Optional[int] = None
    """Validity score, from 0 to 100 (0 – invalid, 100 – valid)."""

    local_part: Optional[str] = None
    """Local part (everything preceding the @ sign)."""

    domain: Optional[str] = None
    """Domain name part."""

    mx_found: Optional[bool] = None
    """True if the address’ domain does have an MX record, false if does not."""

    mx_record: Optional[str] = None
    """Preferred MX record for the domain."""

    did_you_mean: Optional[str] = None
    """For addresses which are likely to have typing errors (cause=possible_typo), a suggested variant with
    a fixed typo.
    """

    processed_at: Optional[str] = None
    """Email check date and time, YYYY-MM-DD hh:mm:ss UTC."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EmailValidationSingleResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            email=data.get("email"),
            result=data.get("result"),
            cause=data.get("cause"),
            validity=data.get("validity"),
            local_part=data.get("local_part"),
            domain=data.get("domain"),
            mx_found=data.get("mx_found"),
            mx_record=data.get("mx_record"),
            did_you_mean=data.get("did_you_mean"),
            processed_at=data.get("processed_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "email": self.email,
            "result": self.result,
            "cause": self.cause,
            "validity": self.validity,
            "local_part": self.local_part,
            "domain": self.domain,
            "mx_found": self.mx_found,
            "mx_record": self.mx_record,
            "did_you_mean": self.did_you_mean,
            "processed_at": self.processed_at,
        }
        return {k: v for k, v in result.items() if v is not None}
