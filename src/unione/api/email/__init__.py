"""Email section: EmailApi and its models."""
from .api import EmailApi
from .models import *  # noqa: F401,F403
from .models import __all__ as _models

__all__ = ["EmailApi", *_models]
