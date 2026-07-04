# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/file_retrieval.py
r"""
MODULE ORIGIN: kanda_reasoner_app/reasoner_engine\reasoner_retriever.py
MANIFEST: kanda_reasoner_app/reasoner_engine\reasoner_retriever_help.json
HELP FOLDER: kanda_reasoner_app/reasoner_engine\reasoner_retriever_help
PURPOSE: Public compatibility facade for file-level retrieval and compact evidence.
EXPORTS: retrieve_files, build_compact_file_evidence
DEPENDS ON: file_retrieval_core.py, file_retrieval_evidence.py
REFACTOR DATE: 2026-06-30
"""

# Canonical readable source. Deprecated private base64 source shards are history only.
from __future__ import annotations

from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_core import (
    retrieve_files as _public_retrieve_files,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_evidence import (
    build_compact_file_evidence as _public_build_compact_file_evidence,
)

retrieve_files = _public_retrieve_files
build_compact_file_evidence = _public_build_compact_file_evidence

__all__ = ["retrieve_files", "build_compact_file_evidence"]
