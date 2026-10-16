"""Models of the Domain section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, model_of, to_enum

from unione.common import VerificationRecordStatus

__all__ = ["DkimStatus", "DomainGetDnsRecordsRequest", "DomainGetDnsRecordsResponse", "DomainValidateVerificationRecordRequest", "DomainValidateVerificationRecordResponse", "DomainValidateDkimRequest", "DomainValidateDkimResponse", "DomainListRequest", "DomainListResponse", "DomainListResponseDomainsItem", "DomainListResponseDomainsItemVerificationRecord", "DomainListResponseDomainsItemDkim", "DomainGetSandboxDomainResponse", "DomainDeleteRequest", "DomainDeleteResponse"]


class DkimStatus(str, Enum):
    """Only domains with "active" DKIM record are allowed as sender domains."""

    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass
class DomainGetDnsRecordsRequest:
    """DomainGetDnsRecordsRequest"""

    domain: str
    """Domain to get DNS records for."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainGetDnsRecordsRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            domain=data.get("domain"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "domain": self.domain,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainGetDnsRecordsResponse:
    """DomainGetDnsRecordsResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    domain: Optional[str] = None
    """Domain to get DNS records for."""

    verification_record: Optional[str] = None
    """Record to be added "as is" to verify ownership of this domain."""

    dkim: Optional[str] = None
    """DKIM signature for the domain. This property contains only the key part, you should prepend it with
    "v=DKIM1; k=rsa; p=" for the TXT record to be valid.
    """

    dmarc: Optional[str] = None
    """Target of the CNAME record for the "_dmarc" host of the domain."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainGetDnsRecordsResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            domain=data.get("domain"),
            verification_record=data.get("verification-record"),
            dkim=data.get("dkim"),
            dmarc=data.get("dmarc"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "domain": self.domain,
            "verification-record": self.verification_record,
            "dkim": self.dkim,
            "dmarc": self.dmarc,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainValidateVerificationRecordRequest:
    """DomainValidateVerificationRecordRequest"""

    domain: str
    """Domain to validate verification record for."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainValidateVerificationRecordRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            domain=data.get("domain"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "domain": self.domain,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainValidateVerificationRecordResponse:
    """DomainValidateVerificationRecordResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    message: Optional[str] = None
    """Debug message."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainValidateVerificationRecordResponse:
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


@dataclass
class DomainValidateDkimRequest:
    """DomainValidateDkimRequest"""

    domain: str
    """Domain to validate DKIM record for."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainValidateDkimRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            domain=data.get("domain"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "domain": self.domain,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainValidateDkimResponse:
    """DomainValidateDkimResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    message: Optional[str] = None
    """Debug message."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainValidateDkimResponse:
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


@dataclass
class DomainListRequest:
    """DomainListRequest"""

    domain: Optional[str] = None
    """Optional domain name if you want to get the status of single domain only."""

    limit: Optional[int] = None
    """Limits the number of domains returned. Default is 50.
    Default: `50`.
    """

    offset: Optional[int] = None
    """Index of the first domain in the list, starting with 0.
    Default: `0`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainListRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            domain=data.get("domain"),
            limit=data.get("limit"),
            offset=data.get("offset"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "domain": self.domain,
            "limit": self.limit,
            "offset": self.offset,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainListResponse:
    """DomainListResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    domains: Optional[List[DomainListResponseDomainsItem]] = None
    """Array of objects describing domains."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            domains=list_of(data.get("domains"), lambda item0: model_of(DomainListResponseDomainsItem, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "domains": [item0.to_dict() for item0 in self.domains] if self.domains is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainListResponseDomainsItem:
    """DomainListResponseDomainsItem"""

    domain: Optional[str] = None
    """Domain name."""

    verification_record: Optional[DomainListResponseDomainsItemVerificationRecord] = None
    """Object describing verification record value and status."""

    dkim: Optional[DomainListResponseDomainsItemDkim] = None
    """Object describing DKIM record value and status."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainListResponseDomainsItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            domain=data.get("domain"),
            verification_record=model_of(DomainListResponseDomainsItemVerificationRecord, data.get("verification-record")),
            dkim=model_of(DomainListResponseDomainsItemDkim, data.get("dkim")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "domain": self.domain,
            "verification-record": self.verification_record.to_dict() if self.verification_record is not None else None,
            "dkim": self.dkim.to_dict() if self.dkim is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainListResponseDomainsItemVerificationRecord:
    """Object describing verification record value and status."""

    value: Optional[str] = None
    """Record to be added "as is" to verify ownership of this domain."""

    status: Optional[VerificationRecordStatus] = None
    """Only domains with "confirmed" verification record are allowed as sender domains."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainListResponseDomainsItemVerificationRecord:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            value=data.get("value"),
            status=to_enum(VerificationRecordStatus, data.get("status")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "value": self.value,
            "status": self.status,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainListResponseDomainsItemDkim:
    """Object describing DKIM record value and status."""

    key: Optional[str] = None
    """DKIM signature for the domain. This property contains only the key part, you should prepend it with
    "k=rsa, p=" part for the record to be valid (see
    [domain/get-dns-records](https://docs.unione.io/en/web-api-ref#domain-get-dns-records)).
    """

    status: Optional[DkimStatus] = None
    """Only domains with "active" DKIM record are allowed as sender domains."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainListResponseDomainsItemDkim:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            key=data.get("key"),
            status=to_enum(DkimStatus, data.get("status")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "key": self.key,
            "status": self.status,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainGetSandboxDomainResponse:
    """DomainGetSandboxDomainResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    domain: Optional[str] = None
    """Sandbox domain name."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainGetSandboxDomainResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            domain=data.get("domain"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "domain": self.domain,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainDeleteRequest:
    """DomainDeleteRequest"""

    domain: str
    """Domain name to delete."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainDeleteRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            domain=data.get("domain"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "domain": self.domain,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DomainDeleteResponse:
    """DomainDeleteResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    message: Optional[str] = None
    """Domain deleted"""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainDeleteResponse:
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
