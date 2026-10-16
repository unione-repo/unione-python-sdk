"""Models of the Tag section."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ...client.enums import as_dict, list_of, model_of

__all__ = ["TagListResponse", "TagsResponseObject", "TagDeleteRequest"]


@dataclass
class TagListResponse:
    """TagListResponse"""

    status: Optional[str] = None
    """"success" string
    Allowed values: `success`.
    """

    tags: Optional[List[TagsResponseObject]] = None
    """An array of objects containing data for user-defined tags."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TagListResponse:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            status=data.get("status"),
            tags=list_of(data.get("tags"), lambda item0: model_of(TagsResponseObject, item0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "status": self.status,
            "tags": [item0.to_dict() for item0 in self.tags] if self.tags is not None else None,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TagsResponseObject:
    """An object with the properties of the user tags."""

    tag_id: Optional[int] = None
    """Unique tag id."""

    tag: Optional[str] = None
    """Tag name."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TagsResponseObject:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            tag_id=data.get("tag_id"),
            tag=data.get("tag"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "tag_id": self.tag_id,
            "tag": self.tag,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class TagDeleteRequest:
    """TagDeleteRequest"""

    tag_id: int
    """Unique tag id."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TagDeleteRequest:
        """Build the object from decoded JSON. Lenient: a missing field, null or a value of another type gives
        None (a non-dict data gives an empty object).
        """
        data = as_dict(data)
        return cls(
            tag_id=data.get("tag_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """JSON-ready dict, None fields are omitted."""
        result = {
            "tag_id": self.tag_id,
        }
        return {k: v for k, v in result.items() if v is not None}
