# project-path: kanda_reasoner_app/reasoner_context_bundle/source_archive_exporter.py
"""Compatibility shim for the canonical source-tree exporter.

The implementation moved to source_tree_exporter because this filename is
classified as stale/reference-looking by architecture validation.  Keep this
module as a thin import-compatible facade for older tests or external scripts.
New active code must import kanda_reasoner_app.reasoner_context_bundle.source_tree_exporter.
"""

from __future__ import annotations

