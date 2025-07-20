"""
Alfred AI File Butler

An intelligent file organization system that runs quietly in the background,
automatically organizing your digital mess into a perfectly structured file system.
"""

__version__ = "0.1.0"
__author__ = "Alfred Team"

# Make key modules easily accessible
from . import utils
from .config import config

__all__ = ["utils", "config", "__version__"]
