"""Models of the Project section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, model_of, to_enum

from unione.common import EmailCounterMode

__all__ = ["ProjectCreateRequest", "ProjectObject", "ProjectCreateResponse", "ProjectUpdateRequest", "ProjectUpdateObject", "ProjectUpdateResponse", "ProjectListRequest", "ProjectListResponse", "ProjectListObject", "ProjectDeleteRequest"]


@dataclass
class ProjectCreateRequest:
    """ProjectCreateRequest"""

    project: ProjectObject
    """Object with project properties."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectCreateRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            project=model_of(ProjectObject, data.get("project")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "project": self.project.to_dict() if self.project is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectObject:
    """Object with project properties."""

    name: str
    """Project name, unique for user account."""

    country: Optional[str] = None
    """ISO-3166 alpha-2 country code. If set, UniOne treats project personal data according to country
    laws, e.g. GDPR for european countries.
    """

    send_enabled: Optional[bool] = None
    """Whether email sending is enabled for this project or not.
    Default: `True`.
    """

    custom_unsubscribe_url_enabled: Optional[bool] = None
    """If it's false then UniOne adds default unsubscribe footer to each email sent with API key of the
    project. If it's true then appending default unsubscribe footer for this project is avoided and
    sending with custom unsubscribe url or even without unsubscribe url is permitted for the project.
    Please note that custom_unsubscribe_url_enabled=true is available only if removing unsubscribe link
    is approved for the user account by support. More on this
    [here](https://docs.unione.io/en/unsubscribe-link). When custom_unsubscribe_url_enabled is skipped
    on creating a project, it's value is taken from user
    """

    backend_domain_id: Optional[int] = None
    """A unique domain identifier which will determine the [tracking
    domain](https://docs.unione.io/en/tracking-domains) or [dedicated IP](/dedicated-ip) pool to be used
    by default. If the value is not specified, a default backend domain will be assigned for your
    account or project instead.
    """

    unsubscribe_page_id: Optional[int] = None
    """A unique identifier that defines the default unsubscribe page. If absent, the account/project will
    be assigned the system default unsubscribe page.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            name=data.get("name"),
            country=data.get("country"),
            send_enabled=data.get("send_enabled"),
            custom_unsubscribe_url_enabled=data.get("custom_unsubscribe_url_enabled"),
            backend_domain_id=data.get("backend_domain_id"),
            unsubscribe_page_id=data.get("unsubscribe_page_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "name": self.name,
            "country": self.country,
            "send_enabled": self.send_enabled,
            "custom_unsubscribe_url_enabled": self.custom_unsubscribe_url_enabled,
            "backend_domain_id": self.backend_domain_id,
            "unsubscribe_page_id": self.unsubscribe_page_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectCreateResponse:
    """ProjectCreateResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    project_id: Optional[str] = None
    """Unqiue project identifier, ASCII string up to 36 characters long."""

    project_api_key: Optional[str] = None
    """API key of the project. You can use it instead of the user API key parameter in all methods except
    project/* methods.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectCreateResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            project_id=data.get("project_id"),
            project_api_key=data.get("project_api_key"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "project_id": self.project_id,
            "project_api_key": self.project_api_key,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectUpdateRequest:
    """ProjectUpdateRequest"""

    project: ProjectUpdateObject
    """Object with project properties."""

    project_id: Optional[str] = None
    """Unique project identifier. You should identify project to update either with project_id or with
    project_api_key field. But we recommend usage of project_id as a more secure option.
    """

    project_api_key: Optional[str] = None
    """Optional project API key. You should identify project to update either with project_id or with
    project_api_key field. But we recommend usage of project_id as a more secure option.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectUpdateRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            project=model_of(ProjectUpdateObject, data.get("project")),
            project_id=data.get("project_id"),
            project_api_key=data.get("project_api_key"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "project_id": self.project_id,
            "project_api_key": self.project_api_key,
            "project": self.project.to_dict() if self.project is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectUpdateObject:
    """Object with project properties."""

    name: str
    """Project name, unique for user account."""

    country: Optional[str] = None
    """ISO-3166 alpha-2 country code. If set, UniOne treats project personal data according to country
    laws, e.g. GDPR for european countries.
    """

    send_enabled: Optional[bool] = None
    """Whether email sending is enabled for this project or not.
    Default: `True`.
    """

    custom_unsubscribe_url_enabled: Optional[bool] = None
    """If it's false then UniOne adds default unsubscribe footer to each email sent with API key of the
    project. If it's true then appending default unsubscribe footer for this project is avoided and
    sending with custom unsubscribe url or even without unsubscribe url is permitted for the project.
    Please note that custom_unsubscribe_url_enabled=true is available only if removing unsubscribe link
    is approved for the user account by support. More on this
    [here](https://docs.unione.io/en/unsubscribe-link). When custom_unsubscribe_url_enabled is skipped
    on creating a project, it's value is taken from user
    """

    backend_domain_id: Optional[int] = None
    """A unique domain identifier which will determine the [tracking
    domain](https://docs.unione.io/en/tracking-domains) or [dedicated IP](/dedicated-ip) pool to be used
    by default. If the value is not specified, a default backend domain will be assigned for your
    account or project instead.
    """

    unsubscribe_page_id: Optional[int] = None
    """A unique identifier that defines the default unsubscribe page. If absent, the account/project will
    be assigned the system default unsubscribe page.
    """

    email_counter: Optional[int] = None
    """Project's email counter value. 0 value only is accepted (which means resetting the counter to zero),
    or refreshes automatically depending on the counter mode set with the 'email_counter_mode'
    parameter. If the request doesn't contain the field or contains null, the limit value doesn't
    change.
    """

    email_counter_limit: Optional[int] = None
    """Allows you to limit the number of emails sent by the project. The sending stops when the limit is
    reached. Any non-negative 64-bit integer is acceptable. Setting to 0 means no limit. If the request
    doesn't contain the field or contains null, the limit value doesn't change.
    Default: `0`.
    """

    email_counter_mode: Optional[EmailCounterMode] = None
    """Sets the email counter mode. It allows you to choose whether the counter should reset automatically,
    or remain permanent. The following values are acceptable: 'default' - the counter resets to zero
    automatically at the beginning of each accounting period, 'permanent' - the counter never resets
    automatically. The reset can be done only manually by the user in the request with the passes 0
    value in the email_counter field. If the request doesn't contain the field or contains a null value,
    the limit value doesn't change.
    Default: `default`.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectUpdateObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            name=data.get("name"),
            country=data.get("country"),
            send_enabled=data.get("send_enabled"),
            custom_unsubscribe_url_enabled=data.get("custom_unsubscribe_url_enabled"),
            backend_domain_id=data.get("backend_domain_id"),
            unsubscribe_page_id=data.get("unsubscribe_page_id"),
            email_counter=data.get("email_counter"),
            email_counter_limit=data.get("email_counter_limit"),
            email_counter_mode=to_enum(EmailCounterMode, data.get("email_counter_mode")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "name": self.name,
            "country": self.country,
            "send_enabled": self.send_enabled,
            "custom_unsubscribe_url_enabled": self.custom_unsubscribe_url_enabled,
            "backend_domain_id": self.backend_domain_id,
            "unsubscribe_page_id": self.unsubscribe_page_id,
            "email_counter": self.email_counter,
            "email_counter_limit": self.email_counter_limit,
            "email_counter_mode": self.email_counter_mode,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectUpdateResponse:
    """ProjectUpdateResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    project_api_key: Optional[str] = None
    """API key of the project. Returned only if the project to update was identified by project_api_key.
    Not returned in case of updating by project_id.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectUpdateResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            project_api_key=data.get("project_api_key"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "project_api_key": self.project_api_key,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectListRequest:
    """ProjectListRequest"""

    project_id: Optional[str] = None
    """Optional possibility to specify project_id to include only this project to list."""

    project_api_key: Optional[str] = None
    """Optional possibility to specify project_api_key to include only this project to list."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectListRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            project_id=data.get("project_id"),
            project_api_key=data.get("project_api_key"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "project_id": self.project_id,
            "project_api_key": self.project_api_key,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectListResponse:
    """ProjectListResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    projects: Optional[List[ProjectListObject]] = None
    """Array of objects where each object represents one project."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            projects=list_of(data.get("projects"), lambda item0: model_of(ProjectListObject, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "projects": [item0.to_dict() for item0 in self.projects] if self.projects is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectListObject:
    """ProjectListObject"""

    id: Optional[str] = None
    """Unqiue project identifier, ASCII string up to 36 characters long."""

    api_key: Optional[str] = None
    """API key of the project. You can use it instead of the user API key parameter in all methods except
    project/* methods.
    """

    name: Optional[str] = None
    """Project name, unique for user account."""

    country: Optional[str] = None
    """ISO-3166 alpha-2 country code. If set, UniOne treats project personal data according to country
    laws, e.g. GDPR for european countries.
    """

    reg_time: Optional[str] = None
    """Date and time of project creation in UTC timezone in "YYYY-MM-DD hh:mm:ss" format."""

    send_enabled: Optional[bool] = None
    """Whether email sending is enabled for this project or not.
    Default: `True`.
    """

    custom_unsubscribe_url_enabled: Optional[bool] = None
    """If it's false then UniOne adds default unsubscribe footer to each email sent with API key of the
    project. If it's true then appending default unsubscribe footer for this project is avoided and
    sending with custom unsubscribe url or even without unsubscribe url is permitted for the project.
    Please note that custom_unsubscribe_url_enabled=true is available only if removing unsubscribe link
    is approved for the user account by support. More on this
    [here](https://docs.unione.io/en/unsubscribe-link). When custom_unsubscribe_url_enabled is skipped
    on creating a project, it's value is taken from user
    """

    backend_domain_id: Optional[int] = None
    """A unique domain identifier which will determine the [tracking
    domain](https://docs.unione.io/en/tracking-domains) or [dedicated IP](/dedicated-ip) pool to be used
    by default. If the value is not specified, a default backend domain will be assigned for your
    account or project instead.
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

    unsubscribe_page_id: Optional[int] = None
    """A unique identifier that defines the default unsubscribe page. If absent, the account/project will
    be assigned the system default unsubscribe page.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectListObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            id=data.get("id"),
            api_key=data.get("api_key"),
            name=data.get("name"),
            country=data.get("country"),
            reg_time=data.get("reg_time"),
            send_enabled=data.get("send_enabled"),
            custom_unsubscribe_url_enabled=data.get("custom_unsubscribe_url_enabled"),
            backend_domain_id=data.get("backend_domain_id"),
            email_counter=data.get("email_counter"),
            email_counter_limit=data.get("email_counter_limit"),
            email_counter_mode=to_enum(EmailCounterMode, data.get("email_counter_mode")),
            unsubscribe_page_id=data.get("unsubscribe_page_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "id": self.id,
            "api_key": self.api_key,
            "name": self.name,
            "country": self.country,
            "reg_time": self.reg_time,
            "send_enabled": self.send_enabled,
            "custom_unsubscribe_url_enabled": self.custom_unsubscribe_url_enabled,
            "backend_domain_id": self.backend_domain_id,
            "email_counter": self.email_counter,
            "email_counter_limit": self.email_counter_limit,
            "email_counter_mode": self.email_counter_mode,
            "unsubscribe_page_id": self.unsubscribe_page_id,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ProjectDeleteRequest:
    """ProjectDeleteRequest"""

    project_id: Optional[str] = None
    """Unique project identifier. You should identify project to delete either with project_id or with
    project_api_key field. We recommend usage of project_id as a more secure option.
    """

    project_api_key: Optional[str] = None
    """Optional project API key. You should identify project to delete either with project_id or with
    project_api_key field. We recommend usage of project_id as a more secure option.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProjectDeleteRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            project_id=data.get("project_id"),
            project_api_key=data.get("project_api_key"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "project_id": self.project_id,
            "project_api_key": self.project_api_key,
        }
        return {k: v for k, v in result.items() if v is not None}
