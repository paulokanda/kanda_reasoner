"""
Public help index facade for Reasoner Engine.

This module keeps the public HELP_INDEX contract stable while moving the large
static payload into the help_index_help package.
"""

from __future__ import annotations

from .help_index_help.help_index_data import HELP_INDEX

__all__ = ["HELP_INDEX"]



