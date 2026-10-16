"""Template section: TemplateApi and its models."""
from .api import TemplateApi
from .models import *  # noqa: F401,F403
from .models import __all__ as _models

__all__ = ["TemplateApi", *_models]
