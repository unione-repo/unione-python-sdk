"""Tag section: TagApi and its models."""
from .api import TagApi
from .models import *  # noqa: F401,F403
from .models import __all__ as _models

__all__ = ["TagApi", *_models]
