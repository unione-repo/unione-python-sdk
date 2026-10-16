"""ConfirmedEmail section: ConfirmedEmailApi and its models."""
from .api import ConfirmedEmailApi
from .models import *  # noqa: F401,F403
from .models import __all__ as _models

__all__ = ["ConfirmedEmailApi", *_models]
