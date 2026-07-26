"""Compatibility re-export layer for startup kernel constants.

This module preserves the public import surface after Train Car 3 moved
large literal text blocks and default source-map data into focused helper
modules. Importers should continue to use startup_kernel.constants.
"""

from __future__ import annotations

from startup_kernel.startup_literal_texts import *
from startup_kernel.startup_names import *
from startup_kernel.startup_source_map import *

__all__ = []

