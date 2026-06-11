"""Private data shard for help_index_raw.py."""

from __future__ import annotations

import ast
import base64

_RAW_LITERAL_B64 = (
    'eyd3aW5kb3dfdGl0bGUnOiAnUHJvamVjdCBSZWFzb25lciBWMTAgLSBIZWxwJ30='
)

RAW_HELP_INDEX_PART_1 = ast.literal_eval(
    base64.b64decode(_RAW_LITERAL_B64).decode("utf-8")
)

__all__: list[str] = []
