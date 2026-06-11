"""Private source-preserving loader for file_retrieval implementation."""

from __future__ import annotations

import base64
from pathlib import Path

from . import file_retrieval_source_part_1_private_impl as _part_1
from . import file_retrieval_source_part_2_private_impl as _part_2
from . import file_retrieval_source_part_3_private_impl as _part_3

_PART_MODULES = (
    _part_1,
    _part_2,
    _part_3,
)


def _load_original_namespace() -> dict[str, object]:
    source_bytes = b"".join(
        base64.b64decode(part._SOURCE_PART_BASE64)
        for part in _PART_MODULES
    )
    source = source_bytes.decode("utf-8-sig")
    original_file = str(Path(__file__).resolve().parents[1] / "file_retrieval.py")
    namespace: dict[str, object] = {
        "__name__": "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval",
        "__package__": "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help",
        "__file__": original_file,
        "__builtins__": __builtins__,
    }
    exec(compile(source, original_file, "exec"), namespace)
    return namespace


_ORIGINAL_NAMESPACE = _load_original_namespace()
_retrieve_files_impl = _ORIGINAL_NAMESPACE["retrieve_files"]
_build_compact_file_evidence_impl = _ORIGINAL_NAMESPACE["build_compact_file_evidence"]

__all__: list[str] = []
