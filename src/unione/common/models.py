"""Models of the Common section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ..client.enums import as_dict

__all__ = ["TemplateEngine", "EmailStatus", "VerificationRecordStatus", "EmailCounterMode", "BodyObject", "HeadersObject", "AttachmentsArrayItem", "InlineAttachmentsArrayItem", "SuccessResponse"]


class TemplateEngine(str, Enum):
    """The [template engine](https://docs.unione.io/en/template-engines) for handling the
    substitutions(merge tags), "simple", "velocity", "liquid" or "none". Default value is "simple".
    """

    SIMPLE = "simple"
    VELOCITY = "velocity"
    LIQUID = "liquid"
    NONE = "none"


class EmailStatus(str, Enum):
    """EmailStatus"""

    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    UNSUBSCRIBED = "unsubscribed"
    SUBSCRIBED = "subscribed"
    SOFT_BOUNCED = "soft_bounced"
    HARD_BOUNCED = "hard_bounced"
    SPAM = "spam"


class VerificationRecordStatus(str, Enum):
    """Only domains with "confirmed" verification record are allowed as sender domains."""

    CONFIRMED = "confirmed"
    UNCONFIRMED = "unconfirmed"


class EmailCounterMode(str, Enum):
    """Sets the email counter mode. It allows you to choose whether the counter should reset automatically,
    or remain permanent. The following values are acceptable: 'default' - the counter resets to zero
    automatically at the beginning of each accounting period, 'permanent' - the counter never resets
    automatically. The reset can be done only manually by the user in the request with the passes 0
    value in the email_counter field. If the request doesn't contain the field or contains a null value,
    the limit value doesn't change.
    """

    DEFAULT = "default"
    PERMANENT = "permanent"


@dataclass
class BodyObject:
    """Contains HTML/plaintext/AMP parts of the email. Either html or plaintext part is required."""

    html: Optional[str] = None
    """HTML part of the email body"""

    plaintext: Optional[str] = None
    """Plaintext part of the email body."""

    amp: Optional[str] = None
    """Optional [AMP](http://amp.dev/documentation/guides-and-tutorials/learn/email_fundamentals/) part of
    the email body.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BodyObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            html=data.get("html"),
            plaintext=data.get("plaintext"),
            amp=data.get("amp"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "html": self.html,
            "plaintext": self.plaintext,
            "amp": self.amp,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class HeadersObject:
    """Contains email headers, maximum 50. Only headers with “X-” name prefix are accepted, all other are
    ignored, for example X-UNIONE-Global-Language, X-UNIONE-Template-Engine. Standard headers "To,"
    "CC," and "BCC" are passed without the "X-." Yet, they are processed in a particular way and, as a
    result, have a number of restrictions. You can find more details about it [here](/cc-and-bcc). If
    our support have approved omitting standard unsubscription block for you, you can also pass
    List-Unsubscribe, List-Subscribe, List-Help, List-Owner, List-Archive, In-Reply-To and References
    headers.
    """

    x_unione_global_language: Optional[str] = None
    """The language of the unsubscribe footer and unsubscribe page. Languages supported are: "be", "de",
    "en", "es", "fr", "it", "pl", "pt", "ru", "ua", "kz".
    """

    x_unione_template_engine: Optional[str] = None
    """The template engine for handling the substitutions(merge tags), “simple”, “velocity”, “liquid” or
    “none”. Default value is “simple”. Has a priority over the value allowed in the “template_engine”
    parameter.
    """

    extra: Dict[str, str] = field(default_factory=dict)
    """Fields beyond the named ones, sent as is next to them (a named field wins), e.g. any X-* header,
    "CC", "List-Unsubscribe": extra={"X-MyHeader": "some data"}. Unknown keys of a response go here too.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HeadersObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            x_unione_global_language=data.get("X-UNIONE-Global-Language"),
            x_unione_template_engine=data.get("X-UNIONE-Template-Engine"),
            extra={key: value for key, value in data.items() if key not in ("X-UNIONE-Global-Language", "X-UNIONE-Template-Engine", )},
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted. The keys of extra go next to the named fields (a named
        field wins).
        """
        result = {
            "X-UNIONE-Global-Language": self.x_unione_global_language,
            "X-UNIONE-Template-Engine": self.x_unione_template_engine,
        }
        extra = {key: value for key, value in (self.extra or {}).items() if key not in result and value is not None}
        return {**extra, **{k: v for k, v in result.items() if v is not None}}


@dataclass
class AttachmentsArrayItem:
    """AttachmentsArrayItem"""

    type: str
    """Attachment type, see [MIME](https://en.wikipedia.org/wiki/MIME). If unsure, use
    "application/octet-stream".
    """

    name: str
    """Attachment name in the format: "name.extension". When multiple attachments are passed, their names
    must be unique. The symbol ‘/’ is not allowed in attachment names.
    """

    content: str
    """File contents in [base64](https://en.wikipedia.org/wiki/Base64). Maximum file size 7MB (9786710
    bytes in base64).
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AttachmentsArrayItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            type=data.get("type"),
            name=data.get("name"),
            content=data.get("content"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "type": self.type,
            "name": self.name,
            "content": self.content,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class InlineAttachmentsArrayItem:
    """InlineAttachmentsArrayItem"""

    type: str
    """Attachment type, see [MIME](https://en.wikipedia.org/wiki/MIME). If unsure, use
    "application/octet-stream".
    """

    name: str
    """Attachment content id. For example, "name"="IMAGECID1" should be referenced in HTML like <img
    src="cid:IMAGECID1">.
    """

    content: str
    """File contents in [base64](https://en.wikipedia.org/wiki/Base64). Maximum file size 7MB (9786710
    bytes in base64).
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> InlineAttachmentsArrayItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            type=data.get("type"),
            name=data.get("name"),
            content=data.get("content"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "type": self.type,
            "name": self.name,
            "content": self.content,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class SuccessResponse:
    """SuccessResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SuccessResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
        }
        return {k: v for k, v in result.items() if v is not None}
