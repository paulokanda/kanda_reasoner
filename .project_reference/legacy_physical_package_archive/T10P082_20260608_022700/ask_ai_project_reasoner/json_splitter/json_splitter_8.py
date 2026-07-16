"""Public facade for the JSON splitter implementation."""

from __future__ import annotations

from .json_splitter_8_help.source_loader_private_impl import (
    load_json_splitter_8_source as _load_json_splitter_8_source,
)

_load_json_splitter_8_source(globals())

if "__all__" not in globals():
    __all__ = ['SplitPlan', 'LeafSlot', 'PartSpec', 'json_bytes_indented', 'stable_hash', 'build_document_for_spec', 'SplitterWorker', 'JsonSplitterPanel', 'JsonSplitterWindow', 'main', 'RECOMMENDED_FILE_BYTES', 'MIN_PART_BYTES', 'CHATGPT_HARD_FILE_BYTES', 'CHATGPT_HARD_TOKENS', 'CHATGPT_RECOMMENDED_FILE_BYTES', 'CHATGPT_RECOMMENDED_TOKENS', 'CHATGPT_MAX_FILES_PER_MESSAGE', 'MAX_FILE_BYTES', 'CHUNK_SCHEMA', 'UPLOAD_INDEX_SCHEMA', 'dumps_compact', 'json_bytes_compact', 'estimate_tokens_text', 'estimate_tokens_value', 'upload_stats', 'chunked', 'parse_target_path', 'get_nested_value', 'set_nested_value', 'collect_container_paths', 'get_entries', 'rebuild_container', 'get_wrapper', 'expand_to_slots', 'pack_slots', 'format_path_label', 'build_upload_chunk', 'split_spec_until_upload_safe']
