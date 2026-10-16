"""Obsolete section: ObsoleteApi and its models."""
from .api import ObsoleteApi
from .models import *  # noqa: F401,F403
from .models import __all__ as _models

__all__ = ["ObsoleteApi", *_models]
