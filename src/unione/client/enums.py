"""Helpers of the models: enums and lenient decoding of responses.

A response that lacks a field, has null in it or a value of another type does not break from_dict: the field is None
(a model is built only from an object, a list only from an array).
"""
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

E = TypeVar("E", bound=Enum)
T = TypeVar("T")


def to_enum(enum_cls: Type[E], value: Any) -> Union[E, Any]:
    """Enum member for a decoded value; unknown values (added to the API later) are kept as is."""
    if value is None:
        return None
    try:
        return enum_cls(value)
    except (ValueError, TypeError):
        return value


def as_dict(data: Any) -> Dict[str, Any]:
    """The decoded object, {} for anything else (null, an array, a string)."""
    return data if isinstance(data, dict) else {}


def model_of(cls: Any, value: Any) -> Any:
    """cls.from_dict(value) for an object, None for anything else."""
    return cls.from_dict(value) if isinstance(value, dict) else None


def list_of(value: Any, item: Optional[Callable[[Any], T]] = None) -> Optional[List[Any]]:
    """[item(v) for v in value] for an array, None for anything else."""
    if not isinstance(value, list):
        return None
    return [item(v) for v in value] if item is not None else value


def map_of(value: Any, item: Optional[Callable[[Any], T]] = None) -> Optional[Dict[str, Any]]:
    """{k: item(v)} for an object ([] - an empty object encoded as an array - gives {}), None for anything else."""
    if isinstance(value, list) and not value:
        return {}
    if not isinstance(value, dict):
        return None
    return {k: item(v) for k, v in value.items()} if item is not None else value
