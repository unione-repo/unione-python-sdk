"""Models of the Email section."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, map_of, model_of, to_enum

from unione.common import AttachmentsArrayItem, BodyObject, HeadersObject, InlineAttachmentsArrayItem, TemplateEngine

__all__ = ["EmailSendRequest", "MessageObject", "MessageObjectRecipientsItem", "MessageObjectOptions", "EmailSendResponse", "EmailSubscribeRequest"]


@dataclass
class EmailSendRequest:
    """EmailSendRequest"""

    message: MessageObject
    """Object containing all message properties."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EmailSendRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            message=model_of(MessageObject, data.get("message")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "message": self.message.to_dict() if self.message is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class MessageObject:
    """Object containing all message properties."""

    recipients: List[MessageObjectRecipientsItem]
    """Contains recipient emails, substitutions(merge tags) and metadata."""

    body: BodyObject
    """Contains HTML/plaintext/AMP parts of the email. Either html or plaintext part is required."""

    subject: str
    """Email subject."""

    template_id: Optional[str] = None
    """Optional identifier of the template that had been created by
    [template/set](https://docs.unione.io/en/web-api-ref#template-set) method. If template_id is passed
    then fields from the template are used instead of missed email/send parameters. E.g. if "body"
    parameter in email/send is omitted, "body" from template will be used. If "subject" in email/send is
    omitted, "subject" from template will be used.
    """

    tags: Optional[List[str]] = None
    """An array of strings. The maximum string length is 100 characters. You can include up to 4 strings
    which must be unique. No more than 10 000 tags are allowed per project; if you try to add more,
    email/send will return an error. You may use tags to categorize emails by your own criteria, and
    they will be passed along by event-dump methods.
    """

    skip_unsubscribe: Optional[int] = None
    """Whether to skip or not appending default unsubscribe footer. 1=skip, 0=append, default is 0. You
    should [ask support](https://cp.unione.io/en/support) to approve
    usage of skip_unsubscribe=1. [Read more](https://docs.unione.io/en/unsubscribe-link).
    Allowed values: `0`, `1`.
    """

    global_language: Optional[str] = None
    """The language of the unsubscribe footer and unsubscribe page. Languages supported are: "be", "de",
    "en", "es", "fr", "it", "pl", "pt", "ru", "ua", "kz".
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

    from_email: Optional[str] = None
    """Sender's email. Required only if template_id parameter is empty."""

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

    bypass_global: Optional[int] = None
    """(allowed values 0 or 1, default 0) If set to 1, the global unavailability list will be ignored. Even
    if the address was found to be unreachable while sending other UniOne users' emails, or its owner
    has issued complaints, the message will still be sent. The setting may be ignored for certain
    addresses.
    Allowed values: `0`, `1`.
    """

    bypass_unavailable: Optional[int] = None
    """(allowed values 0 or 1, default 0) If set to 1, the current user's or project's unavailability list
    will be ignored. Works only if bypass_global is set to 1.
    Allowed values: `0`, `1`.
    """

    bypass_unsubscribed: Optional[int] = None
    """(allowed values 0 or 1, default 0) If set to 1, the current list of unsubscribed addresses for this
    account or project will be ignored. Works only if bypass_global is set to 1. The setting is
    available only for users that have been granted the right to omit the unsubscribe link (to request,
    please contact [support](https://cp.unione.io/en/support)).
    Allowed values: `0`, `1`.
    """

    bypass_complained: Optional[int] = None
    """(allowed values 0 or 1, default 0) If set to 1, the user's or project's complaint list will be
    ignored. Works only if bypass_global is set to 1. The setting is available only for users that have
    been granted the right to omit the unsubscribe link (to request, please contact
    [support](https://cp.unione.io/en/support)).
    Allowed values: `0`, `1`.
    """

    idempotence_key: Optional[str] = None
    """A string of up to 64 characters containing a unique message key. This can be used to prevent
    occasional message duplicates. If you send another API request with the same message key within the
    next minute, it will be declined. We can generate a message key for each letter automatically; to
    enable this option, please contact our [tech support](https://cp.unione.io/en/support).
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

    options: Optional[MessageObjectOptions] = None
    """Additional message options."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MessageObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            recipients=list_of(data.get("recipients"), lambda item0: model_of(MessageObjectRecipientsItem, item0)),
            body=model_of(BodyObject, data.get("body")),
            subject=data.get("subject"),
            template_id=data.get("template_id"),
            tags=list_of(data.get("tags")),
            skip_unsubscribe=data.get("skip_unsubscribe"),
            global_language=data.get("global_language"),
            template_engine=to_enum(TemplateEngine, data.get("template_engine")),
            global_substitutions=map_of(data.get("global_substitutions")),
            global_metadata=map_of(data.get("global_metadata")),
            from_email=data.get("from_email"),
            from_name=data.get("from_name"),
            reply_to=data.get("reply_to"),
            reply_to_name=data.get("reply_to_name"),
            track_links=data.get("track_links"),
            track_read=data.get("track_read"),
            bypass_global=data.get("bypass_global"),
            bypass_unavailable=data.get("bypass_unavailable"),
            bypass_unsubscribed=data.get("bypass_unsubscribed"),
            bypass_complained=data.get("bypass_complained"),
            idempotence_key=data.get("idempotence_key"),
            headers=model_of(HeadersObject, data.get("headers")),
            attachments=list_of(data.get("attachments"), lambda item0: model_of(AttachmentsArrayItem, item0)),
            inline_attachments=list_of(data.get("inline_attachments"), lambda item0: model_of(InlineAttachmentsArrayItem, item0)),
            options=model_of(MessageObjectOptions, data.get("options")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "recipients": [item0.to_dict() for item0 in self.recipients] if self.recipients is not None else None,
            "template_id": self.template_id,
            "tags": self.tags,
            "skip_unsubscribe": self.skip_unsubscribe,
            "global_language": self.global_language,
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
            "bypass_global": self.bypass_global,
            "bypass_unavailable": self.bypass_unavailable,
            "bypass_unsubscribed": self.bypass_unsubscribed,
            "bypass_complained": self.bypass_complained,
            "idempotence_key": self.idempotence_key,
            "headers": self.headers.to_dict() if self.headers is not None else None,
            "attachments": [item0.to_dict() for item0 in self.attachments] if self.attachments is not None else None,
            "inline_attachments": [item0.to_dict() for item0 in self.inline_attachments] if self.inline_attachments is not None else None,
            "options": self.options.to_dict() if self.options is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class MessageObjectRecipientsItem:
    """MessageObjectRecipientsItem"""

    email: str
    """Recipient email"""

    substitutions: Optional[Dict[str, str]] = None
    """Object to pass the substitutions(merge tags) for the recipient (e.g. recipient name, discount code,
    password change link, etc. See [Template engines](https://docs.unione.io/en/template-engines)). The
    substitutions can be used in the following parameters:

    - body.html
    - body.plaintext
    - body.amp
    - subject
    - from_name
    - headers["List-Unsubscribe"]
    - options.unsubscribe_url
    A substitution name can consist from latin characters, numbers and "_" symbol, and should start with
    the letter. There's a special substitution "to_name" which is used to put recipent's name like "Name
    Surname" to include it to SMTP header "To" in the form "Name Surname <email@example.com>". The
    "to_name" length is limited to 78 symbols.
    """

    metadata: Optional[Dict[str, str]] = None
    """Object for passing the metadata, such as "key": "value". Max key quantity: 10. Max key length: 64
    symbols. Max value length: 1024 symbols. The metadata is returned by
    [webhook](https://docs.unione.io/en/web-api-ref#webhook) and
    [event-dump](https://docs.unione.io/en/web-api-ref#event-dump) methods. If you pass strign up to 128
    bit with "campaign_id" field name (name is configurable thru support), it will be considered as
    campaign identifier in statistics.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MessageObjectRecipientsItem:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            email=data.get("email"),
            substitutions=map_of(data.get("substitutions")),
            metadata=map_of(data.get("metadata")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "email": self.email,
            "substitutions": self.substitutions,
            "metadata": self.metadata,
        }
        return {k: v for k, v in result.items() if v is not None}

    @classmethod
    def from_address(cls, address: str, substitutions: Optional[Dict[str, str]] = None) -> MessageObjectRecipientsItem:
        """A recipient from "email" or "Name <email>": the name goes to the to_name substitution (the name in the
        "To" header); substitutions: more substitutions of the recipient."""
        email, name = address.strip(), ""
        match = re.match(r"^(.*)<([^>]+)>$", email, re.S)
        if match:
            email, name = match.group(2).strip(), match.group(1).strip().strip('"')
        if name:
            substitutions = {"to_name": name, **(substitutions or {})}
        return cls(email=email, substitutions=substitutions)

    def with_metadata(self, metadata: Dict[str, str]) -> MessageObjectRecipientsItem:
        """Sets the metadata of the recipient (returned in its webhook events); returns the recipient."""
        self.metadata = metadata
        return self


@dataclass
class MessageObjectOptions:
    """Additional message options."""

    send_at: Optional[str] = None
    """Date and time in "YYYY-MM-DD hh:mm:ss" format in the UTC timezone. Allows schedule sending up to 24
    hours in advance.
    """

    unsubscribe_url: Optional[str] = None
    """Custom unsubscribe link. Read more [here](https://docs.unione.io/en/unsubscribe-link)."""

    custom_backend_id: Optional[int] = None
    """Backend-domain identifier to send message with. If custom_backend_id is not set, default one for
    your account/project will be used. You can pay for one or more dedicated IPs and use this option.
    """

    smtp_pool_id: Optional[str] = None
    """SMTP pool identifier to send message with. Usually you don't need to pass this parameter because
    correct smtp_pool_id is selected automatically based on the default one for your account/project or
    according to custom_backend_id parameter.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MessageObjectOptions:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            send_at=data.get("send_at"),
            unsubscribe_url=data.get("unsubscribe_url"),
            custom_backend_id=data.get("custom_backend_id"),
            smtp_pool_id=data.get("smtp_pool_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "send_at": self.send_at,
            "unsubscribe_url": self.unsubscribe_url,
            "custom_backend_id": self.custom_backend_id,
            "smtp_pool_id": self.smtp_pool_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EmailSendResponse:
    """EmailSendResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    job_id: Optional[str] = None
    """Job identifier, might be useful for investigating errors."""

    emails: Optional[List[str]] = None
    """Array of recipients emails successfully accepted for sending."""

    failed_emails: Optional[Dict[str, str]] = None
    """Object with emails rejected for sending as property names and their statuses as property values,
    e.g.: {"email1@gmail.com": "temporary_unavailable"}. Possible statuses:

    - __unsubscribed__ - specified email is unsubscribed;
    - __invalid__ - the email does not exist or has been entered incorrectly;
    - __duplicate__ - the email already exists in the request, email duplicating is prevented;
    - __temporary_unavailable__ - the email address is unavailable. This means that over the next three days sending to this address will return an error. Email may be temporarily unavailable due to several reasons, e.g.:

    - a previous email has been rejected by the recipient's server for spam;
    - the recipient's mailbox is full or is not used;
    - recipient's domain does not accept mail;
    - sending server was rejected due to blacklisting;

    - __permanent_unavailable__ - the email address is permanently unavailable or unsubscribed globally.
    - __complained__ -  the recipient reported spam in the previous emails;
    - __blocked__ -  sending to the email is prohibited by administration of UniOne.
    We may added new statuses in the future.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EmailSendResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            job_id=data.get("job_id"),
            emails=list_of(data.get("emails")),
            failed_emails=map_of(data.get("failed_emails")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "job_id": self.job_id,
            "emails": self.emails,
            "failed_emails": self.failed_emails,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EmailSubscribeRequest:
    """EmailSubscribeRequest"""

    from_email: str
    """Sender’s email on a confirmed domain. (Field alias "email_address_from" is supported, too)."""

    from_name: str
    """Sender’s name. (Field alias "name_from" is supported, too)."""

    to_email: str
    """Recipient’s email. (Field alias "email_address_to" is supported, too)."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EmailSubscribeRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            from_email=data.get("from_email"),
            from_name=data.get("from_name"),
            to_email=data.get("to_email"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "from_email": self.from_email,
            "from_name": self.from_name,
            "to_email": self.to_email,
        }
        return {k: v for k, v in result.items() if v is not None}
