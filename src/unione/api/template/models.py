"""Models of the Template section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, map_of, model_of, to_enum

from unione.common import AttachmentsArrayItem, BodyObject, HeadersObject, InlineAttachmentsArrayItem, TemplateEngine

__all__ = ["EditorType", "TemplateSetRequest", "TemplateObject", "TemplateSetResponse", "TemplateGetRequest", "TemplateGetResponse", "TemplateListRequest", "TemplateListResponse", "TemplateListObject", "TemplateDeleteRequest"]


class EditorType(str, Enum):
    """Editor type, "html" or "visual". Default is "html". You can create a template with "visual" editor
    type only in web interface.
    """

    HTML = "html"
    VISUAL = "visual"


@dataclass
class TemplateSetRequest:
    """Object with all the properties of the template."""

    template: TemplateObject
    """Object with all the template properties."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateSetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            template=model_of(TemplateObject, data.get("template")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "template": self.template.to_dict() if self.template is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateObject:
    """Object with all the template properties."""

    name: str
    """Template name."""

    from_email: str
    """Sender's email."""

    id: Optional[str] = None
    """Template unique identifier. If you omit the "id" field then new template will be created. If you
    specify the "id" field, the system will try to find a template with the specified id and edit it.
    """

    editor_type: Optional[EditorType] = None
    """Editor type, "html" or "visual". Default is "html". You can create a template with "visual" editor
    type only in web interface.
    """

    template_engine: Optional[TemplateEngine] = None
    """The [template engine](https://docs.unione.io/en/template-engines) for handling the
    substitutions(merge tags), "simple", "velocity", "liquid" or "none". Default value is "simple".
    """

    global_substitutions: Optional[Dict[str, str]] = None
    """Object for passing the substitutions(merge tags) common for all recipients - e.g., company name. If
    the substitution names are duplicated in object "substitutions", the values of the variables will be
    taken from the object "substitutions". The substitutions can be used in the following parameters:

    - body.html
    - body.plaintext
    - body.amp
    - subject
    - from_name
    - options.unsubscribe_url
    A substitution name can consist from latin characeters, numbers and "_" symbol, and should start
    with the letter.
    """

    global_metadata: Optional[Dict[str, str]] = None
    """Object for passing the metadata common for all the recipients, such as "key": "value". Max key
    quantity: 10. Max key length: 64 symbols. Max value length: 1024 symbols. The metadata is returned
    by [webhook](https://docs.unione.io/en/web-api-ref#webhook). To group single emails into a campaign,
    you can use the system key 'campaign_id' with a value in the form of a non-negative decimal integer
    up to 128 bits or a UUID in the format 'c7703772-453e-4c77-a9ae-9a1b94051b5a'. Incorrect values will
    be treated as '0'.
    """

    body: Optional[BodyObject] = None
    """Contains HTML/plaintext/AMP parts of the email. Either html or plaintext part is required."""

    subject: Optional[str] = None
    """Email subject."""

    from_name: Optional[str] = None
    """Sender's name."""

    reply_to: Optional[str] = None
    """Optional Reply-To email (in case it's different to sender's email)"""

    reply_to_name: Optional[str] = None
    """Optional Reply-To name (if reply_to email is specified and you want to display not only this email
    but also the name)
    """

    track_links: Optional[int] = None
    """1 = click tracking is on (default), 0 = click tracking is off. To use track_links = 0, you need to
    ask support to enable this feature.
    Allowed values: `0`, `1`.
    """

    track_read: Optional[int] = None
    """1 = read tracking is on (default), 0=read tracking is off. To use track_read = 0, you need to ask
    support to enable this feature.
    Allowed values: `0`, `1`.
    """

    headers: Optional[HeadersObject] = None
    """Contains email headers, maximum 50. Only headers with “X-” name prefix are accepted, all other are
    ignored, for example X-UNIONE-Global-Language, X-UNIONE-Template-Engine. Standard headers "To,"
    "CC," and "BCC" are passed without the "X-." Yet, they are processed in a particular way and, as a
    result, have a number of restrictions. You can find more details about it [here](/cc-and-bcc). If
    our support have approved omitting standard unsubscription block for you, you can also pass
    List-Unsubscribe, List-Subscribe, List-Help, List-Owner, List-Archive, In-Reply-To and References
    headers.
    """

    attachments: Optional[List[AttachmentsArrayItem]] = None
    """Optional array of attachments"""

    inline_attachments: Optional[List[InlineAttachmentsArrayItem]] = None
    """Optional array of inline attachments, e.g. for including images in email instead of loading them
    from external URL.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            name=data.get("name"),
            from_email=data.get("from_email"),
            id=data.get("id"),
            editor_type=to_enum(EditorType, data.get("editor_type")),
            template_engine=to_enum(TemplateEngine, data.get("template_engine")),
            global_substitutions=map_of(data.get("global_substitutions")),
            global_metadata=map_of(data.get("global_metadata")),
            body=model_of(BodyObject, data.get("body")),
            subject=data.get("subject"),
            from_name=data.get("from_name"),
            reply_to=data.get("reply_to"),
            reply_to_name=data.get("reply_to_name"),
            track_links=data.get("track_links"),
            track_read=data.get("track_read"),
            headers=model_of(HeadersObject, data.get("headers")),
            attachments=list_of(data.get("attachments"), lambda item0: model_of(AttachmentsArrayItem, item0)),
            inline_attachments=list_of(data.get("inline_attachments"), lambda item0: model_of(InlineAttachmentsArrayItem, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "id": self.id,
            "name": self.name,
            "editor_type": self.editor_type,
            "template_engine": self.template_engine,
            "global_substitutions": self.global_substitutions,
            "global_metadata": self.global_metadata,
            "body": self.body.to_dict() if self.body is not None else None,
            "subject": self.subject,
            "from_email": self.from_email,
            "from_name": self.from_name,
            "reply_to": self.reply_to,
            "reply_to_name": self.reply_to_name,
            "track_links": self.track_links,
            "track_read": self.track_read,
            "headers": self.headers.to_dict() if self.headers is not None else None,
            "attachments": [item0.to_dict() for item0 in self.attachments] if self.attachments is not None else None,
            "inline_attachments": [item0.to_dict() for item0 in self.inline_attachments] if self.inline_attachments is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateSetResponse:
    """TemplateSetResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    template: Optional[TemplateObject] = None
    """Object with all the template properties."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateSetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            template=model_of(TemplateObject, data.get("template")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "template": self.template.to_dict() if self.template is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateGetRequest:
    """TemplateGetRequest"""

    id: str
    """Template id."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateGetRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            id=data.get("id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "id": self.id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateGetResponse:
    """TemplateGetResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    template: Optional[TemplateObject] = None
    """Object with all the template properties."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateGetResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            template=model_of(TemplateObject, data.get("template")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "template": self.template.to_dict() if self.template is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateListRequest:
    """TemplateListRequest"""

    limit: Optional[int] = None
    """Limits the number of templates returned, default is 50.
    Default: `50`.
    """

    offset: Optional[int] = None
    """Index of the first template in the list, starting with 0.
    Default: `0`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateListRequest:
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
class TemplateListResponse:
    """TemplateListResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    templates: Optional[List[TemplateListObject]] = None
    """Array of template objects."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            templates=list_of(data.get("templates"), lambda item0: model_of(TemplateListObject, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "templates": [item0.to_dict() for item0 in self.templates] if self.templates is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateListObject:
    """TemplateListObject"""

    id: Optional[str] = None
    """Template unique identifier."""

    name: Optional[str] = None
    """Template name."""

    editor_type: Optional[EditorType] = None
    """Editor type, "html" or "visual". Default is "html". You can create a template with "visual" editor
    type only in web interface.
    """

    template_engine: Optional[TemplateEngine] = None
    """The [template engine](https://docs.unione.io/en/template-engines) for handling the
    substitutions(merge tags), "simple", "velocity", "liquid" or "none". Default value is "simple".
    """

    global_substitutions: Optional[Dict[str, str]] = None
    """Object for passing the substitutions(merge tags) common for all recipients - e.g., company name. If
    the substitution names are duplicated in object "substitutions", the values of the variables will be
    taken from the object "substitutions". The substitutions can be used in the following parameters:

    - body.html
    - body.plaintext
    - body.amp
    - subject
    - from_name
    - options.unsubscribe_url
    A substitution name can consist from latin characeters, numbers and "_" symbol, and should start
    with the letter.
    """

    global_metadata: Optional[Dict[str, str]] = None
    """Object for passing the metadata common for all the recipients, such as "key": "value". Max key
    quantity: 10. Max key length: 64 symbols. Max value length: 1024 symbols. The metadata is returned
    by [webhook](https://docs.unione.io/en/web-api-ref#webhook). To group single emails into a campaign,
    you can use the system key 'campaign_id' with a value in the form of a non-negative decimal integer
    up to 128 bits or a UUID in the format 'c7703772-453e-4c77-a9ae-9a1b94051b5a'. Incorrect values will
    be treated as '0'.
    """

    body: Optional[BodyObject] = None
    """Contains HTML/plaintext/AMP parts of the email. Either html or plaintext part is required."""

    subject: Optional[str] = None
    """Email subject."""

    from_email: Optional[str] = None
    """Sender's email."""

    from_name: Optional[str] = None
    """Sender's name."""

    reply_to: Optional[str] = None
    """Optional Reply-To email (in case it's different to sender's email)"""

    reply_to_name: Optional[str] = None
    """Optional Reply-To name (if reply_to email is specified and you want to display not only this email
    but also the name)
    """

    track_links: Optional[int] = None
    """1 = click tracking is on (default), 0 = click tracking is off. To use track_links = 0, you need to
    ask support to enable this feature.
    Allowed values: `0`, `1`.
    """

    track_read: Optional[int] = None
    """1 = read tracking is on (default), 0=read tracking is off. To use track_read = 0, you need to ask
    support to enable this feature.
    Allowed values: `0`, `1`.
    """

    headers: Optional[HeadersObject] = None
    """Contains email headers, maximum 50. Only headers with “X-” name prefix are accepted, all other are
    ignored, for example X-UNIONE-Global-Language, X-UNIONE-Template-Engine. Standard headers "To,"
    "CC," and "BCC" are passed without the "X-." Yet, they are processed in a particular way and, as a
    result, have a number of restrictions. You can find more details about it [here](/cc-and-bcc). If
    our support have approved omitting standard unsubscription block for you, you can also pass
    List-Unsubscribe, List-Subscribe, List-Help, List-Owner, List-Archive, In-Reply-To and References
    headers.
    """

    attachments: Optional[List[AttachmentsArrayItem]] = None
    """Optional array of attachments"""

    inline_attachments: Optional[List[InlineAttachmentsArrayItem]] = None
    """Optional array of inline attachments, e.g. for including images in email instead of loading them
    from external URL.
    """

    created: Optional[str] = None
    """Template creation date and time in UTC timezone in format "YYYY-MM-DD hh:mm:ss\""""

    user_id: Optional[int] = None
    """Unique user identifier."""

    project_id: Optional[str] = None
    """Unqiue project identifier, ASCII string up to 36 characters long."""

    project_name: Optional[str] = None
    """Project name, unique for user account."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateListObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            editor_type=to_enum(EditorType, data.get("editor_type")),
            template_engine=to_enum(TemplateEngine, data.get("template_engine")),
            global_substitutions=map_of(data.get("global_substitutions")),
            global_metadata=map_of(data.get("global_metadata")),
            body=model_of(BodyObject, data.get("body")),
            subject=data.get("subject"),
            from_email=data.get("from_email"),
            from_name=data.get("from_name"),
            reply_to=data.get("reply_to"),
            reply_to_name=data.get("reply_to_name"),
            track_links=data.get("track_links"),
            track_read=data.get("track_read"),
            headers=model_of(HeadersObject, data.get("headers")),
            attachments=list_of(data.get("attachments"), lambda item0: model_of(AttachmentsArrayItem, item0)),
            inline_attachments=list_of(data.get("inline_attachments"), lambda item0: model_of(InlineAttachmentsArrayItem, item0)),
            created=data.get("created"),
            user_id=data.get("user_id"),
            project_id=data.get("project_id"),
            project_name=data.get("project_name"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "id": self.id,
            "name": self.name,
            "editor_type": self.editor_type,
            "template_engine": self.template_engine,
            "global_substitutions": self.global_substitutions,
            "global_metadata": self.global_metadata,
            "body": self.body.to_dict() if self.body is not None else None,
            "subject": self.subject,
            "from_email": self.from_email,
            "from_name": self.from_name,
            "reply_to": self.reply_to,
            "reply_to_name": self.reply_to_name,
            "track_links": self.track_links,
            "track_read": self.track_read,
            "headers": self.headers.to_dict() if self.headers is not None else None,
            "attachments": [item0.to_dict() for item0 in self.attachments] if self.attachments is not None else None,
            "inline_attachments": [item0.to_dict() for item0 in self.inline_attachments] if self.inline_attachments is not None else None,
            "created": self.created,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "project_name": self.project_name,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TemplateDeleteRequest:
    """TemplateDeleteRequest"""

    id: str
    """Template id."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateDeleteRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            id=data.get("id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "id": self.id,
        }
        return {k: v for k, v in result.items() if v is not None}
