"""
QA Framework - Data Quality Assurance for Databricks
"""

__version__ = "0.1.0"

from .validators import DataValidator
from .utils import setup_logger, read_config

try:
    from .ge_validator import GreatExpectationsValidator
except Exception as exc:
    # Keep core package imports usable even if GE has runtime compatibility issues.
    class GreatExpectationsValidator:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "GreatExpectationsValidator is unavailable in this environment. "
                "Install compatible Great Expectations dependencies and Python version."
            ) from exc

__all__ = [
    "DataValidator", 
    "setup_logger", 
    "read_config",
    "GreatExpectationsValidator"
]
